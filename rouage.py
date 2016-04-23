#!/usr/bin/python3

import socket
import select
import threading
import pickle
import datetime

from tkinter import *

##########################################
#
# Création de la class Rouage et des ses dépendances
#
##########################################

def diff_pseudo(liste1, liste2):
	"""
	Compare et fusionne deux listes de pseudos
	"""
	nouv_liste=liste1
	if liste1 == liste2: # Compare les deux listes, quelque soit leur ordre.
		isNew=False

	else:
		isNew=True
		for i in range(len(liste2)):
			OK=1
			for j in range(len(liste1)):
				if liste1[j]==liste2[i]:
					OK=0
		
			if OK==1:
				nouv_liste=nouv_liste+[liste2[i]]
				
	
	return (isNew,nouv_liste)

class Rouage(threading.Thread):
	"""Class principale, héritée de Thread, permettant d'émettre et de recevoir des connections. En d'autres mots, elle regroupe client et serveur"""

	def __init__(self, port_serveur,backlog,size):

		self.pseudo = None

		self.port_serveur = port_serveur
		self.backlog=backlog
		self.size=size

		self.running=False

		self.socket_list = []
		self.id_list=[]
		self.pseudo_list = []
		self.local_pseudo_list = []

		self.msg_text = None # Le type sera changé par fentere_princ()
		self.StringVar_pseudo_list = None

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind(('',self.port_serveur))
		self.s.listen(backlog)

		self.socket_list.append(self.s)

		threading.Thread.__init__(self)

	def run(self):
		"""Code à exécuter pendant l'exécution du rouage."""
		self.running=True
		while self.running:
			# prend une liste des socket prêt à être lu.
			ready_to_read, ready_to_write, in_error = select.select(self.socket_list,self.socket_list,[],0.1)
			for sock in ready_to_read:
				# Une nouvelle connection!
				if sock == self.s:
					newsocket, addr = self.s.accept()
					self.socket_list.append(newsocket)
					print("Client connecté, d'adresse: "+str(addr[0]))

				# Un message d'un client existant
				else:
					# Reception des données...
					data = sock.recv(self.size)
					if data:
						data = pickle.loads(data) # Décodage de ces données
						print(str(data))
						if data[0] not in self.id_list: # data[0] correspond à l'id du message
							self.id_list.append(data[0]) # Ajoute l'id du message, il ne sera pas rééaffiché en cas de nouvelle récéption

							if data[3] == "": # Message non privé
								self.update_msg_text(data[2]+": "+data[1]) # Affiche le message
								self.sendMessage(data, self.socket_list[1:]) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

							else: #Il s'agit d'un message privé
								if data[3] == self.pseudo: # Qui nous est destiné
									self.update_msg_text(data[2]+" vous chuchotte: "+data[1]) # Affiche le message
									self.sendMessage(data, self.socket_list[1:]) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

								elif data[3] == "SYSTEM": # Message système, reception d'un pseudo, ou d'une liste de pseudo

									if data[1] == "DISCONNECT_BAD_PSEUDO":
										self.update_msg_text("Déconnection générale, mauvais pseudo.") # Affiche le message de déconnection
										self.quit()

									elif type(data[1]) is list:
										if data[1][0] == "DISCONNECT":
											if data[4] == 1: # un client directement connecté
												self.socket_list.remove(sock)
												sock.close
											print(str(data[1][1]))
											for x in data[1][1]:
												if x != self.pseudo:
													self.pseudo_list.remove(x)
													self.update_msg_text(x+" est maintenant déconnecté") # Affiche le message de connection
											self.local_pseudo_list.remove(data[2])
											self.update_StringVar_pseudo_list()
											self.sendMessage(data, self.socket_list[1:]) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

										elif data[1][0] == "NEW_CONN": # Message système, reception d'un nouveau pseudo
											isNew, diff = diff_pseudo(data[1][1],self.pseudo_list)
											if isNew == True: # L'utilisateur n'est pas encore connecté au réseau
												if data[2] not in self.pseudo_list:
													self.pseudo_list.append(data[2])
													self.update_StringVar_pseudo_list()
													self.update_msg_text(data[2]+" est maintenant connecté") # Affiche le message de connection
													self.sendTimedMessage(self.pseudo_list,"SYSTEM") # Envoi à tout le monde sa liste, mise à jour.
												else:
													self.sendTimedMessage("DISCONNECT_BAD_PSEUDO","SYSTEM", [sock]) # déconnecte de force, le nouvel arrivé à déjà un pseudo existant.
											else:
													self.update_msg_text(data[2]+" est maintenant directement connecté, le réseau est plus fort !") # Affiche le message de connection

										else: # Récéption d'une liste de pseudo unique
											isNew, self.pseudo_list = diff_pseudo(data[1],self.pseudo_list)
											if isNew:
												self.sendTimedMessage(self.pseudo_list,"SYSTEM")
											self.update_StringVar_pseudo_list()

									if data[4] == 1 and data[2] not in self.local_pseudo_list: # Si le message viens d'un client local, et que l'on ne le connait pas, on l'ajoute.
										self.local_pseudo_list.append(data[2])

								else: # Les message n'est pas pour nous, on fait tourner
									self.sendMessage(data, self.socket_list[1:]) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

					else:
					# Il n'y a rien, le client est sans doute déconnecté
						if sock in self.socket_list:
							self.socket_list.remove(sock)
							sock.close()
						print("Client perdu")

	def ConnectNewServer(self, ip, port):
		"""
		Permet de se connecter à un nouveau serveur.
		"""
		# Création d'un socket pour la nouvelle connection
		ysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			ysock.connect((ip,port))# On se connecte au nouveau serveur.
			self.update_msg_text("Connecté au serveur distant d'ip "+str(ip)+".")
			self.socket_list.append(ysock) # On l'ajoute à la liste de socket

			self.sendTimedMessage(["NEW_CONN",self.pseudo_list],"SYSTEM",[ysock]) # Envoi son pseudo au serveur distant, pour vérification
		except Exception as e:
				print("CLIENT: Quelque chose s'est mal passé avec %s:%d. l'exception est %s" % (ip,port, e))

	def sendTimedMessage(self, msg, destinataire="",socket_list="DEFAULT"):
		"""Envoi un message avec son id, le temps, à la liste de socket. Ajoute l'id à la liste. Si destinataire est défini, le message ne sera lu que par la personne
		portant le pseudo mis dans destinataire"""
		print(str(msg))
		if socket_list == "DEFAULT":
			socket_list = self.socket_list[1:]
		time = str(datetime.datetime.now())
		self.id_list.append(time) # Ajoute notre propre message à la liste des messages envoyés
		if destinataire == "":
			self.update_msg_text(self.pseudo+": "+msg) # Affiche le message
		elif destinataire != "" and destinataire != "SYSTEM": # N'affiche pas messages privés
			self.update_msg_text("Vous chuchotez à "+destinataire+": "+msg) # Affiche le message
		for sock in socket_list:
			sock.send(pickle.dumps([time,msg,self.pseudo,destinataire,1])) # Envoi le temps afin d'éviter les boucles d'envoi infinies (=id du message), plus le message

	def sendMessage(self, msg, socket_list):
		"""Envoi un message à la liste de socket"""
		msg[4] += 1 # Incrémente l'éloignement
		for sock in socket_list:
			sock.send(pickle.dumps(msg)) # Envoi du message.

	def update_StringVar_pseudo_list(self):
		"""
		Met à jour graphiquement la liste de pseudo
		"""
		while isinstance(self.StringVar_pseudo_list,StringVar) == False: # Attends l'initialisation de la fenêtre graphique
			pass
		if isinstance(self.StringVar_pseudo_list,StringVar): # Vérifie que la variable a bien été initialisée dans la fenêtre principale
			j = ""
			for i in self.pseudo_list:
				j += i+"\n"
			self.StringVar_pseudo_list.set(j) # Affiche la liste de pseudos

	def update_msg_text(self, new_message):
		"""
		Met à jour la liste des messages. Prend en argument new_message, un string.
		"""
		while isinstance(self.msg_text,Text) == False: # Attends l'initialisation de la fenêtre graphique
			pass
		if isinstance(self.msg_text,Text): # Vérifie que la variable a bien été initialisée dans la fenêtre principale
			self.msg_text.config(state=NORMAL)
			self.msg_text.insert(END,new_message+"\n")
			self.msg_text.config(state=DISABLED)

	def quit(self):
		self.sendTimedMessage(["DISCONNECT", [self.pseudo] + self.local_pseudo_list],"SYSTEM") # Envoi le message de déconnection
		print("Fermeture...")
		self.running=False
		for sock in self.socket_list:
			self.socket_list.remove(sock)
			sock.close()
