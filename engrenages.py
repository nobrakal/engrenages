#!/usr/bin/python3

import socket
import select
import threading
import datetime
import pickle
import time
import argparse

from tkinter import *

port_serveur = 6666
backlog = 10 # Nombre de connections maximum
size = 1024

def sendTimedMessage(msg, destinataire="",socket_list="DEFAULT"):
	"""Envoi un message avec son id, le temps, à la liste de socket. Ajoute l'id à la liste. Si destinataire est défini, le message ne sera lu que par la personne
	portant le pseudo mis dans destinataire"""
	if socket_list=="DEFAULT":
		socket_list=client.socket_list[1:]
	time = str(datetime.datetime.now())
	client.id_list.append(time) # Ajoute notre propre message à la liste des messages envoyés
	if destinataire == "": # N'affiche pas messages privés
		messages_prec=client.msg.get()
		client.msg.set(messages_prec+client.pseudo+": "+msg+"\n") # Affiche le message
	for sock in socket_list:
		sock.send(pickle.dumps([time,msg,client.pseudo,destinataire])) # Envoi le temps afin d'éviter les boucles d'envoi infinies (=id du message), plus le message

def sendMessage(msg, socket_list):
	"""Envoi un message à la liste de socket"""
	for sock in socket_list:
		sock.send(pickle.dumps(msg)) # Envoi du message.

def shutdown():
	sendTimedMessage("DISCONNECT","SYSTEM") # Envoi le message de déconnection
	for sock in client.socket_list:
		client.socket_list.remove(sock)
		sock.close()
	for sock in serveur.socket_list:
		serveur.socket_list.remove(sock)
		sock.close()

def diff_pseudo(liste1, liste2):
	"""
	Compare et fusionne deux listes de pseudos
	"""
	print("TODO")
	if liste1 != liste2:
		isNew=True
	else:
		isNew=False
	nouv_liste=liste1
	for i in range(len(liste2)):
		OK=1
		for j in range(len(liste1)):
			if liste1[j]==liste2[i]:
				OK=0
		
		if OK==1:
			nouv_liste=nouv_liste+[liste2[i]]
	
	return (isNew,nouv_liste)

def choix_ip_et_destroy(client, Authentification):
	"""
	Fonction écran permettant d'éxécuter deux sous fonctions pour un seul boutton.
	"""
	Authentification.destroy()
	choisir_ip(client)

	
def MP():
	Message_prive=Tk()
	Message_prive.title('Engrenages')
	Message_prive.geometry('450x180')
	Message_prive['bg']='bisque'

	Frame1 = Frame(Message_prive,borderwidth=3,relief=GROOVE)
	Frame1.pack(padx=10,pady=10)
	
	Label1 = Label(Frame1, text = "Quel est le pseudo de l'utilisateur à qui vous souhaitez envoyer un message?", fg = 'black')
	Label1.pack(padx=5,pady=5)

	Pseudo= StringVar()
	Champ = Entry(Frame1, textvariable= Pseudo, bg ='white', fg='lightgrey')
	Champ.focus_set()
	Champ.pack(padx=5, pady=5)
	
	Label2 = Label(Frame1, text = "Quel est votre message?", fg = 'black')
	Label2.pack(padx=5,pady=5)
	
	Message=StringVar()
	Champ1 = Entry(Frame1, textvariable= Message, bg ='white', fg='lightgrey')
	Champ1.focus_set()
	Champ1.pack(padx=5, pady=5)

	Bouton1 = Button(Frame1, text = 'Valider', command = Message_prive.destroy)
	Bouton1.pack(padx = 5, pady=5)

	Message_prive.mainloop()
	
def identification(client):
	"""
	Fenêtre d'identification qui permet à l'utilisateur de choisir son pseudo et de créer ou rejoindre un serveur
	"""
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

	Bouton1 = Button(Frame2, text = 'Rejoindre un serveur existant', command = lambda: choix_ip_et_destroy(client, Authentification)) #***********
	Bouton1.pack(side=LEFT, padx = 5, pady=5)

	Bouton2 = Button(Frame2, text = 'Créer un nouveau serveur', command = Authentification.destroy) #************
	Bouton2.pack(side=LEFT, padx = 5, pady=5)

	# Création d'un bouton quitter
	Bouton3 = Button(Frame2, text = 'Quitter', command = Authentification.destroy)
	Bouton3.pack(side=LEFT, padx = 5, pady=5)

	# Lancement du gestionnaire d'événements
	Authentification.mainloop()

	return Pseudo.get()

def connect_and_destroy(client,ip,fenetre):
	"""
	Fonction écran permettant d'éxécuter deux sous fonctions pour un seul boutton.
	"""
	client.ConnectNewServer(ip)
	fenetre.destroy()

def choisir_ip(client):
	Choix_IP=Tk()
	Choix_IP.title('Engrenages')
	Choix_IP.geometry('300x150')
	Choix_IP['bg']='bisque'

	Frame1 = Frame(Choix_IP,borderwidth=3,relief=GROOVE)
	Frame1.pack(padx=10,pady=10)

	Label1 = Label(Frame1, text = "Quelle est l'adresse IP du serveur à rejoindre?", fg = 'black')
	Label1.pack(padx=5,pady=5)

	IP= StringVar()
	Champ = Entry(Frame1, textvariable= IP, bg ='white', fg='grey')
	Champ.focus_set()
	Champ.pack(padx=5, pady=5)

	Bouton1 = Button(Frame1, text = 'Valider', command = lambda: connect_and_destroy(client,IP.get(),Choix_IP)) #***********
	Bouton1.pack(padx = 5, pady=5)

	Choix_IP.mainloop()

def fenetre_princ(pseudo, client):
	Engrenages = Tk()
	Engrenages.title('Engrenages:'+ pseudo)
	Engrenages.geometry('700x400')
	Engrenages['bg']='bisque' # couleur de fond

	Frame1 = Frame(Engrenages,borderwidth=3,relief=GROOVE)
	Frame1.pack(padx=10,pady=10)

	Label1 = Label(Frame1, text = 'Engrenages', fg = 'black') # augmenter la taille!!
	Label1.pack(padx=5,pady=5)

	Frame2 = LabelFrame(Engrenages,borderwidth=2,relief=GROOVE, bg="lightgrey", text="Messages précédents")
	Frame2.place(x=15,y=75)

	client.msg = StringVar()
	Label3 = Label(Frame2, textvariable = client.msg, fg = 'black', bg="white",height=15,width=70) #affiche les messages précédents
	Label3.pack(padx=5,pady=5, side=TOP)

	Frame3 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame3.place(x=550,y=75)

	Label4 = Label(Frame3, text = 'Utilisateurs connectés', fg = 'black', bg="lightgrey")
	Label4.pack(padx=5,pady=5, side=TOP)

	client.StringVar_pseudo_list = StringVar()
	Label5 = Label(Frame3, textvariable = client.StringVar_pseudo_list, fg = 'black', bg="lightgrey") #liste des utilisateurs connectés
	Label5.pack(padx=5,pady=5)

	Frame4 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame4.pack(padx=10,pady=10, side=BOTTOM)

	Label6 = Label(Frame4, text = 'Votre message:', fg = 'black', bg="lightgrey")
	Label6.pack(padx=5,pady=5, side=LEFT)

	Message = StringVar()
	Champ = Entry(Frame4, textvariable= Message, bg ='white', fg='grey')
	Champ.focus_set()
	Champ.pack(padx=5, pady=5, side=LEFT)

	Bouton1 = Button(Frame4, text = 'Envoyer', command = lambda: sendTimedMessage(Message.get()))  #Remplacer la commande par celle d'envoi de message
	Bouton1.pack(padx=5,pady=5, side= LEFT)

	Frame5 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame5.place(x=575,y=360)

	Bouton2 = Button(Frame5, text = 'Déconnexion', command = shutdown)
	Bouton2.pack(padx=5,pady=5, side= LEFT)
	
	Frame6 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame6.place(x=50,y=360)
	
	Bouton3 = Button(Frame6, text = 'Message Privé', command = MP )
	Bouton3.pack(padx=5,pady=5)

	# Lancement du gestionnaire d'événements
	Engrenages.mainloop()

class Serveur(threading.Thread):
	"""Class chargée du serveur."""

	def __init__(self, pseudo=""):
		self.socket_list = []

		self.pseudo = pseudo

		self.ip_list = []

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind(('',port_serveur))
		self.s.listen(backlog)

		self.socket_list.append(self.s)

		threading.Thread.__init__(self)

	def run(self):
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
#					self.ip_list.append(addr[0])
					self.socket_list[1].send(pickle.dumps(addr)) # Envoi de l'ip à notre client local pour qu'il puisse se connecter
					print ("SERVEUR: Client connecté, d'adresse: "+str(addr[0]))

				# Un message d'un client existant
				else:
					# Reception des données...
					data = sock.recv(size)
					if data:
						self.socket_list[1].send(data) # Envoi du message à notre client local

					else:
					# Il n'y a rien, le client est sans doute déconnecté
						if sock in self.socket_list:
							self.ip_list.remove(sock.getpeername())
							self.socket_list.remove(sock)
							sock.close()
						print("SERVEUR: Client perdu")

			if len(self.socket_list) < 1: # Cas où il ne reste plus qu'un seul socket, le notre.
				print("SERVEUR: Fermeture, plus aucun client connecté")
				self.s.close()
				return 0

class Client(threading.Thread):
	"""Class chargée du client. Prend en argument le serveur local."""
	def __init__(self, serveur, pseudo="", ):
		self.pseudo = pseudo

		self.msg = None # Le type sera changé par fentere_princ()
		self.StringVar_pseudo_list = None

		self.socket_list = []
		self.id_list=[]
		self.pseudo_list = [] # Ajoute notre pseudo à la liste des pseudos (précédé du nom du premier socket, le notre)

		self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.socket_list.append(self.c)

		threading.Thread.__init__(self)

	def run(self):
		"""Code à exécuter pendant l'exécution du client."""
		#On se connecte au serveur local
		self.ConnectNewServer('')
		while 1:
			# Un message d'un client existant
			data = self.socket_list[1].recv(size) # Reception des données...

			if data:
	                	# Des données sont arrivées
				data = pickle.loads(data) # Décodage de ces données

				if type(data) is tuple:
					print("CC")
					self.ConnectNewServer(data[0]) # Reception de l'ip, on se connecte

				elif data[0] not in self.id_list: # data[0] correspond à l'id du message
					self.id_list.append(data[0]) # Ajoute l'id du message, il ne sera pas rééaffiché en cas de nouvelle récéption

					if data[3] == "": # Message non privé
						if isinstance(self.msg,StringVar): # Vérifie que la variable a bien été initialisée dans la fenêtre principale
							messages_prec=self.msg.get()
							self.msg.set(messages_prec+data[2]+": "+data[1]+"\n") # Affiche le message
						else:
							print(data[2]+": "+data[1]+"\n")
						sendMessage(data, self.socket_list[1:]) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

					else: #Il s'agit d'un message privé
						if data[3] == self.pseudo: # Qui nous est destiné
							if isinstance(self.msg,StringVar): # Vérifie que la variable a bien été initialisée dans la fenêtre principale
								messages_prec=self.msg.get()
								self.msg.set(messages_prec+data[2]+" vous chuchotte: "+data[1]+"\n") # Affiche le message
							else:
								print(data[2]+" vous chuchote: "+data[1]+"\n")

						elif data[3] == "SYSTEM": # Message système, reception d'un pseudo, ou d'une liste de pseudo
							if data[1] == "DISCONNECT":
								self.pseudo_list.remove(data[2])
								messages_prec=self.msg.get()
								self.msg.set(messages_prec+data[2]+" est déconnecté"+"\n") # Affiche le message de connection
								self.update_StringVar_pseudo_list()
							else:
								if isinstance(self.msg,StringVar) and data[2] not in self.pseudo_list: # Un nouveau connecté ?
									messages_prec=self.msg.get()
									self.msg.set(messages_prec+data[2]+" est maintenant connecté"+"\n") # Affiche le message de connection

								isNew, self.pseudo_list = diff_pseudo(data[1],self.pseudo_list)
								if isNew:
									sendTimedMessage(self.pseudo_list,"SYSTEM")
									self.update_StringVar_pseudo_list()

						sendMessage(data, self.socket_list[1:])

			if len(self.socket_list) < 1: # Cas où il ne reste plus qu'un seul socket, le notre.
				print("SERVEUR: Fermeture, plus aucun client connecté")
				self.s.close()
				return 0

	def ConnectNewServer(self, ip, port=port_serveur):
		"""
		Permet de se connecter à un nouveau serveur.
		"""
		# Création d'un socket pour la nouvelle connection
		ysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			if ip not in serveur.ip_list:
				ysock.connect((ip,port))# On se connecte au nouveau serveur.
				serveur.ip_list.append(ip)
				self.socket_list.append(ysock)
				if len(self.socket_list) > 2:
					print("CLIENT: Connecté au serveur distant d'ip "+str(ip)+".")
				else:
					print("CLIENT: Connecté au serveur local")
				if len(self.pseudo_list) == 0:
					self.pseudo_list.append(self.pseudo)
				sendTimedMessage(self.pseudo_list,"SYSTEM") # Envoi son pseudo à l'adresse du système
		except Exception as e:
				print("CLIENT: Quelque chose s'est mal passé avec %s:%d. l'exception est %s" % (ip,port_serveur, e))

	def update_StringVar_pseudo_list(self):
		"""
		Met à jour graphiquement la liste de pseudo
		"""
		if isinstance(self.StringVar_pseudo_list,StringVar): # Vérifie que la variable a bien été initialisée dans la fenêtre principale
			j = ""
			for i in self.pseudo_list:
				j += i+"\n"
			self.StringVar_pseudo_list.set(j) # Affiche la liste de pseudos	

parser = argparse.ArgumentParser() # Prend en compte les arguments
parser.add_argument("--serveur", help="Lance engrengages en mode serveur. Prends le pseudo en argument")
args = parser.parse_args()

serveur = Serveur()
serveur.start()
time.sleep(1)
client = Client(serveur)
client.start()
time.sleep(1)

if args.serveur == None:
	pseudo = identification(client)
else:
	pseudo = args.serveur

serveur.pseudo = pseudo
client.pseudo = pseudo

#client.ConnectNewServer("", 6667) #Connecte sur une autre instance s'executant sur le port 6667 du même ordinateur.
if args.serveur == None:
	fenetre_princ(pseudo, client) #Fenêtre principale
else:
	print("Entrée en mode serveur. Attends des connections.")
