#!/usr/bin/python3

""" 
A simple echo server 
""" 

import socket 
import select
import threading
import datetime
import pickle
import time

from tkinter import *

port_serveur = 6666
port_client = 6667
backlog = 10 # Nombre de connections maximum
size = 1024 

def sendTimedMessage(msg, socket_list,client):
	"""Envoi un message avec son id, le temps, à la liste de socket. Ajoute l'id à la liste."""
	for sock in socket_list[1:]:
		time = str(datetime.datetime.now())
		client.id_list.append(time) # Ajoute notre propre message à la liste des messages envoyés
		sock.send(pickle.dumps((time+msg))) # Envoi le temps afin d'éviter les boucles d'envoi infinies (=id du message), plus le message

def sendMessage(msg, socket_list):
	"""Envoi un message à la liste de socket"""
	for sock in socket_list:
		sock.send(pickle.dumps(msg)) # Envoi du message (réencodé).

class Serveur():
	"""Class chargée du serveur."""

	def __init__(self):
		self.socket_list = []
		self.active_sock_list = []

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind(('',port_serveur)) 
		self.s.listen(backlog) 

		self.socket_list.append(self.s)

		self.thread = threading.Thread(target=self.startServeur)
		self.thread.start()

	def startServeur(self):
		"""Code à exécuter pendant l'exécution du serveur."""
		localsock, localaddr = self.s.accept() # Attends la connection du client local
		self.socket_list.append(localsock)
		print("SERVEUR: Client local connecté")
		while 1:
			# prend une liste des socket prêt à être lu.
			ready_to_read, ready_to_write, in_error = select.select(self.socket_list,[],[])
			for sock in ready_to_read:
				# Une nouvelle connection!
				if sock == self.s: 
					newsocket, addr = self.s.accept()
					print ("SERVEUR: Client connecté, d'adresse: "+str(addr))
					self.socket_list.append(newsocket)
	
				# Un message d'un client existant
				else: 
					# Reception des données...
					data = sock.recv(size)
					if data:
						self.socket_list[1].send(data) # Envoi du message à notre client local

					else:
					# Il n'y a rien, le client est sans doute déconnecté
						if sock in self.socket_list:
							self.socket_list.remove(sock)
						print("Client perdu")
	
				if len(self.socket_list) == 1: # Cas où il ne reste plus qu'un seul socket, le notre.
					print("Fermeture, plus aucun client connecté")
					self.s.close()
					return 0

class Client():
	"""Class chargée du client. Prend en argument le serveur local."""

	def __init__(self):
		self.socket_list = []
		self.id_list=[]  

		self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.socket_list.append(self.c)

		self.thread = threading.Thread(target=self.startClient)
		self.thread.start()   

	def startClient(self):
		"""Code à exécuter pendant l'exécution du client."""
		#On se connecte au serveur local
		self.ConnectNewServer('')
		while 1:
			# Un message d'un client existant
			data = self.socket_list[1].recv(size) # Reception des données...
			if data:
	                	# Des données sont arrivées
				data = pickle.loads(data) # Décodage de ces données
				if len(data) < 26: # Cas de reception d'une ip
					self.ConnectNewServer(data) # On s'y connecte
					
				elif data[:26] not in self.id_list: # Les 26 premiers charactères correspondent à la date
						print(data[26:]) # Affiche le message
						self.id_list.append(data[:26]) # Ajoute l'id du message, il ne sera pas rééaffiché en cas de nouvelle récéption
						sendMessage(data, self.socket_list[1:]) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

	def ConnectNewServer(self, ip, port=port_serveur):

		# Création d'un socket pour la nouvelle connection
		ysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			ysock.connect((ip,port))# On se connecte au nouveau serveur.
			self.socket_list.append(ysock)
			if ip != '':
				print("CLIENT: Connecté au serveur distant d'ip "+str(ip))
			else:
				print("CLIENT: Connecté au serveur local")
		except Exception as e: 
			print("CLIENT: Quelque chose s'est mal passé avec %s:%d. l'exception est %s" % (ip,port_serveur, e))

# Création de la fenêtre principale
Authentification = Tk()
Authentification.title('Engrenages')
Authentification.geometry('410x170')
Authentification['bg']='bisque' # couleur de fond


#Création de deux sous-fenêtres
Frame1 = Frame(Authentification,borderwidth=2,relief=GROOVE)
Frame1.pack(padx=10,pady=10)

Frame2 = Frame(Authentification,borderwidth=2,relief=GROOVE)
Frame2.pack(padx=10,pady=10)


# Création d'un widget Label (texte 'Veuillez entrer votre Pseudo !')
Label1 = Label(Frame1, text = 'Veuillez entrer votre Pseudo', fg = 'black', bg='lightgrey')
Label1.pack(padx=5,pady=5) #positionne le widget Label1


#crée le champ de saisie pour entrer le pseudo
Pseudo= StringVar()
Champ = Entry(Frame1, textvariable= Pseudo, bg ='white', fg='grey')
Champ.focus_set()
Champ.pack(padx=5, pady=5)


# Création d'un widget Label (texte 'Que souhaitez-vous faire?')
Label2 = Label(Frame2, text = 'Que souhaitez-vous faire?', fg = 'black', bg='lightgrey')
Label2.pack(pady=5)


Bouton1 = Button(Frame2, text = 'Rejoindre un serveur existant', command = Authentification.destroy) #***********
Bouton1.pack(side=LEFT, padx = 5, pady=5)


Bouton2 = Button(Frame2, text = 'Créer un nouveau serveur', command = Authentification.destroy) #************
Bouton2.pack(side=LEFT, padx = 5, pady=5)


# Création d'un bouton quitter
Bouton3 = Button(Frame2, text = 'Quitter', command = Authentification.destroy)
Bouton3.pack(side=LEFT, padx = 5, pady=5)

# Lancement du gestionnaire d'événements
Authentification.mainloop()


serveur = Serveur()
time.sleep(2)
client = Client()
time.sleep(2)

client.ConnectNewServer("78.205.80.129")
msg = input("Entrez votre message : ")
sendTimedMessage(msg,client.socket_list,client)
