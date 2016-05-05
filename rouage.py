#!/usr/bin/python3

import socket
import select
import threading
import pickle
import datetime
from random import randint

from tkinter import *

from graph import *
 
##########################################
#
# Création de la class Rouage et des ses dépendances
#
##########################################

class Rouage(threading.Thread):
	"""Class principale, héritée de Thread, permettant d'émettre et de recevoir des connections. En d'autres mots, elle regroupe client et serveur"""

	def __init__(self, port_serveur,backlog,size):
		self.pseudo = None

		self.port_serveur = port_serveur
		self.backlog=backlog
		self.size=size

		self.running = False

		self.graph = Graph() # Tableau à 2 dimensions représentant le réseau

		self.gui = False
		self.debug = False

		self.socket_list = []
		self.id_list=[]
		self.local_pseudo_list = []

		self.msg_text = None # Le type sera changé par fentere_princ()
		self.StringVar_pseudo_list = None

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind(('',self.port_serveur))
		self.s.listen(backlog)

		threading.Thread.__init__(self)

	def run(self):
		"""Code à exécuter pendant l'exécution du rouage."""
		self.running=True
		while self.running:
			# prend une liste des socket prêt à être lu.
			ready_to_read, ready_to_write, in_error = select.select([self.s]+self.socket_list,self.socket_list,[],0.1)
			for sock in ready_to_read:
				# Une nouvelle connection!
				if sock == self.s:
					newsocket, addr = self.s.accept()
					self.socket_list.append(newsocket)
					if self.debug == True:
						print("Client connecté, d'adresse: "+str(addr[0]))

				# Un message d'un client existant
				else:
					#print(str(self.socket_list)+str(sock.fileno()))
					# Reception des données...
					try: 
						data = sock.recv(self.size)
					except:
						if self.debug:
							print("Déconnexion brutale d'un serveur...")
					if data:
						data = pickle.loads(data) # Décodage de ces données	
						if self.debug == True:
							print(str(data))
						if data[0] not in self.id_list: # data[0] correspond à l'id du message
							#print(str(self.graph.pseudo_list)+str(self.graph.graphique))
							self.id_list.append(data[0]) # Ajoute l'id du message, il ne sera pas rééaffiché en cas de nouvelle récéption

							if data[4] == 1 and data[2] not in self.local_pseudo_list: # Si le message viens d'un client local, et que l'on ne le connait pas, on l'ajoute.
								self.local_pseudo_list.append(data[2])

							if data[3] == "": # Message non privé
								self.update_msg_text(data[2]+": "+data[1]) # Affiche le message
								self.sendMessage(data, sock.fileno()) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

							else: #Il s'agit d'un message privé
								if data[3] == self.pseudo: # Qui nous est destiné
									self.update_msg_text(data[2]+" vous chuchote: "+data[1]) # Affiche le message
									self.sendMessage(data, sock.fileno()) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

								elif data[3] == "SYSTEM": # Message système, reception d'un pseudo, ou d'une liste de pseudo

									if data[1] == "DISCONNECT_BAD_PSEUDO":
										self.update_msg_text("Déconnection générale, mauvais pseudo.") # Affiche le message de déconnection
										self.quit(forced=True)

									if data[1] == "DISCONNECT":
										self.update_msg_text(data[2]+" est déconnecté") # Affiche le message de déconnection
										self.graph.remove(data[2])
										self.update_StringVar_pseudo_list()
										self.sendMessage(data, sock.fileno()) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

									elif type(data[1]) is list:
										elif data[1][0] == "NEW_CONN": # Message système, reception d'un nouveau pseudo
											isNew, isGood, nouv_graph, diff = self.diff_graph(data[1][1])
											if isNew: # L'utilisateur n'est pas encore connecté au réseau
												if isGood:
													self.graph=nouv_graph
													self.graph.connect(data[2],self.pseudo) # On se connecte avec notre nouvel arrivant
													self.update_StringVar_pseudo_list()
													for x in diff:
														self.update_msg_text(x+" est maintenant connecté") # Affiche le message de connection
													self.sendTimedMessage(self.graph,"SYSTEM") # Envoi à tout le monde sa liste, mise à jour.
												else:
													self.sendTimedMessage("DISCONNECT_BAD_PSEUDO","SYSTEM", [sock]) # déconnecte de force, le nouvel arrivé à déjà un pseudo existant.
											else:
													self.update_msg_text(data[2]+" est maintenant directement connecté, le réseau est plus fort !") # Affiche le message de connection
													self.sendTimedMessage("Hi","SYSTEM",[sock])# Permet à sock de nous ajouter à sa liste de directement connectés.

									elif isinstance(data[1], Graph): # Récéption d'un graph
										isNew, isGood, self.graph, diff = self.diff_graph(data[1])
										for x in diff:
											self.update_msg_text(x+" est maintenant connecté") # Affiche le message de connection
										self.sendMessage(data, sock.fileno()) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale
										self.update_StringVar_pseudo_list()

								else: # Les message n'est pas pour nous, on fait tourner
									self.sendMessage(data, sock.fileno()) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

					else:
					# Il n'y a rien, le client est sans doute déconnecté
						if sock in self.socket_list:
							self.socket_list.remove(sock)
							sock.close()
						if self.debug == True:
							self.update_msg_text("Client perdu")

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

			self.sendTimedMessage(["NEW_CONN",self.graph],"SYSTEM",[ysock]) # Envoi son pseudo au serveur distant, pour vérification
		except Exception as e:
				self.update_msg_text("CLIENT: Quelque chose s'est mal passé avec %s:%d. L'exception est %s" % (ip,port, e))

	def sendTimedMessage(self, msg, destinataire="",socket_list="DEFAULT"):
		"""Envoi un message avec son id, le temps, à la liste de socket. Ajoute l'id à la liste. Si destinataire est défini, le message ne sera lu que par la personne
		portant le pseudo mis dans destinataire"""
		if self.debug == True:
			print(str(len(self.socket_list)))
		if socket_list == "DEFAULT":
			socket_list = self.socket_list.copy()
		time = str(datetime.datetime.now())+str(randint(10,99))
		self.id_list.append(time) # Ajoute notre propre message à la liste des messages envoyés
		if destinataire == "":
			self.update_msg_text(self.pseudo+": "+msg) # Affiche le message
		elif destinataire != "" and destinataire != "SYSTEM": # N'affiche pas messages privés
			self.update_msg_text("Vous chuchotez à "+destinataire+": "+msg) # Affiche le message
		for sock in socket_list:
			sock.send(pickle.dumps([time,msg,self.pseudo,destinataire,1])) # Envoi le temps afin d'éviter les boucles d'envoi infinies (=id du message), plus le message

	def sendMessage(self, msg, prec_sock,socket_list="DEFAULT"):
		"""Envoi un message à la liste de socket"""
		if socket_list == "DEFAULT":
			socket_list = self.socket_list.copy()
		msg[4] += 1 # Incrémente l'éloignement
		if self.debug:
			print(str(msg)+str(len(socket_list)))
		for sock in socket_list:
			if sock.fileno() != prec_sock:
				sock.send(pickle.dumps(msg)) # Envoi du message.

	def update_StringVar_pseudo_list(self):
		"""
		Met à jour graphiquement la liste de pseudo
		"""
		j = ""
		if self.gui == True:
			for i in self.graph.pseudo_list:
				j += i+"\n"
			self.StringVar_pseudo_list.set(j) # Affiche la liste de pseudos
		else:
			self.StringVar_pseudo_list.clear()
			for i in self.graph.pseudo_list:
				self.StringVar_pseudo_list.addstr(i+"\n") # Affiche la liste de pseudos
			self.StringVar_pseudo_list.refresh()

	def update_msg_text(self, new_message):
		"""
		Met à jour la liste des messages. Prend en argument new_message, un string.
		"""
		if self.gui == True:
			self.msg_text.config(state=NORMAL)
			self.msg_text.insert(END,new_message+"\n")
			self.msg_text.config(state=DISABLED)
			self.msg_text.see(END) # Autoscroll des messages
		else:
			if self.msg_text.getyx()[0] >= self.msg_text.getmaxyx()[0]-1: # Permet de scroller au bout de 15 lignes
				for x in range((len(new_message)/self.msg_text.getmaxyx()[1]).__trunc__() + 1): # Évite les messages trop long
					self.msg_text.move(0,0)
					self.msg_text.deleteln()
				self.msg_text.addstr(self.msg_text.getmaxyx()[0]-(((len(new_message)/self.msg_text.getmaxyx()[1])+1).__trunc__() + 1),0,new_message+"\n")			
				self.msg_text.move(self.msg_text.getmaxyx()[0]-1,0)

			else:
				self.msg_text.addstr(new_message+"\n")
			self.msg_text.refresh()

	def diff_graph(self,graph2):
		"""
		Compare et retourne la fusion des deux graph.
		"""
		print(str(self.graph.pseudo_list)+str(self.graph.graphique))
		newgraph=self.graph
		liste_new=[]
		if set(newgraph.pseudo_list)==set(graph2.pseudo_list): # Compare les deux listes, quelque soit leur ordre
			isNew=False
			isGood=False
		else:
			isNew=True
			if graph2.pseudo==self.pseudo:
				isGood=False
			else: 
				isGood=True
			for i in range(len(graph2.pseudo_list)):
				if graph2.pseudo_list[i] not in newgraph.pseudo_list:
					newgraph.add(graph2.pseudo_list[i])
					liste_new.append(graph2.pseudo_list[i])
			for i in range(len(graph2.pseudo_list)):
				for x in range(len(graph2.graphique[i])):
					if graph2.graphique[i][x] == True:
						newgraph.connect(graph2.pseudo_list[i],graph2.pseudo_list[x])
		print(str(newgraph.pseudo_list)+str(newgraph.graphique))
		return (isNew, isGood, newgraph, liste_new)

	def quit(self, forced=False):
		if forced != True:
			self.sendTimedMessage("DISCONNECT","SYSTEM") # Envoi le message de déconnection
		print("Fermeture...")
		self.running=False
		for sock in self.socket_list:
			self.socket_list.remove(sock)
			sock.close()
