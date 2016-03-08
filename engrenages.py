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

def sendTimedMessage(msg, socket_list,client, destinataire=""):
	"""Envoi un message avec son id, le temps, à la liste de socket. Ajoute l'id à la liste. Si destinataire est défini, le message ne sera lu que par la personne
	portant le pseudo mis dans destinataire"""
	time = str(datetime.datetime.now())
	client.id_list.append(time) # Ajoute notre propre message à la liste des messages envoyés
	for sock in socket_list:
		sock.send(pickle.dumps([time,msg,client.pseudo,destinataire])) # Envoi le temps afin d'éviter les boucles d'envoi infinies (=id du message), plus le message

def sendMessage(msg, socket_list):
	"""Envoi un message à la liste de socket"""
	for sock in socket_list:
		sock.send(pickle.dumps(msg)) # Envoi du message.

def graphical():
	Authentification = Tk()
	# Création de la fenêtre principale
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

	fenetre_princ()
	return Pseudo

fenetre_princ():
	Engrenages = Tk()
	Engrenages.title('Engrenages')
	Engrenages.geometry('700x400')
	Engrenages['bg']='bisque' # couleur de fond

	Frame1 = Frame(Engrenages,borderwidth=3,relief=GROOVE)
	Frame1.pack(padx=10,pady=10)

	Label1 = Label(Frame1, text = 'Engrenages', fg = 'black') # augmenter la taille!!
	Label1.pack(padx=5,pady=5)

	Frame2 = LabelFrame(Engrenages,borderwidth=2,relief=GROOVE, bg="lightgrey", text="Messages précédents")
	Frame2.place(x=15,y=75)

	Label3 = Label(Frame2, text = '**********', fg = 'black', bg="white") #affiche les messages précédents
	Label3.pack(padx=5,pady=5, side=TOP)

	Frame3 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame3.place(x=550,y=75)

	Label4 = Label(Frame3, text = 'Utilisateurs connectés', fg = 'black', bg="lightgrey")
	Label4.pack(padx=5,pady=5, side=TOP)

	Label5 = Label(Frame3, text = '********', fg = 'black', bg="lightgrey") #liste des utilisateurs connectés
	Label5.pack(padx=5,pady=5)

	Frame4 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame4.pack(padx=10,pady=10, side=BOTTOM)

	Label6 = Label(Frame4, text = 'Votre message:', fg = 'black', bg="lightgrey")
	Label6.pack(padx=5,pady=5, side=LEFT)

	Message= StringVar()
	Champ = Entry(Frame4, textvariable= Message, bg ='white', fg='grey')
	Champ.focus_set()
	Champ.pack(padx=5, pady=5, side=LEFT)

	Bouton1 = Button(Frame4, text = 'Envoyer', command = Engrenages.destroy)  #Remplacer la commande par celle d'envoi de message
	Bouton1.pack(padx=5,pady=5, side= LEFT)

	Frame5 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame5.place(x=575,y=360)

	Bouton2 = Button(Frame5, text = 'Déconnexion', command = Engrenages.destroy)
	Bouton2.pack(padx=5,pady=5, side= LEFT)

	# Lancement du gestionnaire d'événements
	Engrenages.mainloop()

class Serveur():
	"""Class chargée du serveur."""

	def __init__(self, pseudo):
		self.socket_list = []
		
		self.pseudo = pseudo

		self.ip_list = []

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
					self.socket_list.append(newsocket)
					if addr[0] not in self.ip_list:
						self.ip_list.append(addr[0])
						self.socket_list[1].send(pickle.dumps(addr)) # Envoi de l'ip à notre client local pour qu'il puisse se connecter

					data = self.socket_list[-1].recv(size) # Attends l'envoi du pseudo du dernier socket ajouté à la liste
					if data:
						self.socket_list[1].send(data) # Envoi le pseudo à notre client
						print ("SERVEUR: Client connecté, d'adresse: "+str(addr[0]))
					else:
						print ("SERVEUR: Client connecté, d'adresse: "+str(addr[0])+"mais pseudo non reçu. SUPRESSION DE LA CONNECTION")
						self.socket_list[-1].close()
	
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
						print("SERVEUR: Client perdu")
	
				if len(self.socket_list) == 1: # Cas où il ne reste plus qu'un seul socket, le notre.
					print("SERVEUR: Fermeture, plus aucun client connecté")
					self.s.close()
					return 0

class Client():
	"""Class chargée du client. Prend en argument le serveur local."""

	def __init__(self, pseudo, serveur):
		self.pseudo = pseudo
	
		self.socket_list = []
		self.id_list=[]
		self.pseudo_list = ["LOCAL",self.pseudo] # Ajoute notre pseudo à la liste des pseudos (précédé du nom du premier socket, le notre)

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

				if type(data) is str:
					self.pseudo_list.append(data) # Reception du pseudo, on l'ajoute à la liste
					print(pseudo)

				elif data[0] not in self.id_list: # data[0] correspond à l'id du message
					self.id_list.append(data[0]) # Ajoute l'id du message, il ne sera pas rééaffiché en cas de nouvelle récéption
					if type(data) is tuple:
						self.ConnectNewServer(data[0]) # Reception de l'ip, on se connecte

					elif data[3] == "": # Message non privé
						print(data[2]+": "+data[1]) # Affiche le message
						sendMessage(data, self.socket_list[1:]) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

					else: #Il s'agit d'un message privé
						if data[3] == pseudo: # Qui nous est destiné
							print(data[2]+" vous chuchote: "+data[1]) # Affiche le message
						else: # Pas pour nous, on le fait tourner
							sendMessage(data, self.socket_list[1:])

	def ConnectNewServer(self, ip, port=port_serveur):
		# Création d'un socket pour la nouvelle connection
		ysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			if ip not in serveur.ip_list:
				ysock.connect((ip,port))# On se connecte au nouveau serveur.
				self.socket_list.append(ysock)
				if ip != '':
					print("CLIENT: Connecté au serveur distant d'ip "+str(ip)+". Envoi du pseudo")
					ysock.send(pickle.dumps(self.pseudo)) # Envoi du pseudo
				else:
					print("CLIENT: Connecté au serveur local")
		except Exception as e: 
				print("CLIENT: Quelque chose s'est mal passé avec %s:%d. l'exception est %s" % (ip,port_serveur, e))

pseudo = graphical()

serveur = Serveur(pseudo)
time.sleep(2)
client = Client(pseudo, serveur)
time.sleep(2)

client.ConnectNewServer("192.168.1.43")
msg = input("Entrez votre message : ")
sendTimedMessage(msg,client.socket_list[1:],client) # Message public

msg = input("Entrez votre message : ")
sendTimedMessage(msg,client.socket_list[1:],client, "Moi") # Message privé
