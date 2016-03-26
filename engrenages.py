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
		socket_list=serveur.socket_list[1:]
	time = str(datetime.datetime.now())
	client.id_list.append(time) # Ajoute notre propre message à la liste des messages envoyés
	if destinataire == "":
		client.update_StringVar_msg(client.pseudo+": "+msg) # Affiche le message
	elif destinataire != "" and destinataire != "SYSTEM": # N'affiche pas messages privés
		client.update_StringVar_msg("Vous chuchotez à "+destinataire+": "+msg) # Affiche le message
	for sock in socket_list:
		sock.send(pickle.dumps([time,msg,client.pseudo,destinataire])) # Envoi le temps afin d'éviter les boucles d'envoi infinies (=id du message), plus le message

def sendMessage(msg, socket_list):
	"""Envoi un message à la liste de socket"""
	for sock in socket_list:
		sock.send(pickle.dumps(msg)) # Envoi du message.

def shutdown(forced=False):
	if forced == False:
		sendTimedMessage("DISCONNECT","SYSTEM") # Envoi le message de déconnection
	for sock in serveur.socket_list:
		serveur.socket_list.remove(sock)
		sock.close()

def diff_pseudo(liste1, liste2):
	"""
	Compare et fusionne deux listes de pseudos
	"""
	nouv_liste=liste1
	if set(liste1) == set(liste2): # Compare les deux listes, quelques soit leur ordre.
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

def choix_ip_et_destroy(Authentification):
	"""
	Fonction écran permettant d'éxécuter deux sous fonctions pour un seul boutton.
	"""
	Authentification.destroy()
	choisir_ip()

def sendMPandDestroy(msg, pseudo,Message_prive ):
	print(msg)
	print(pseudo)
	sendTimedMessage(msg,pseudo)
	Message_prive.destroy()
	
def MP():
	Message_prive=Tk()
	Message_prive.title('Engrenages')
	Message_prive.geometry('450x180')
	Message_prive['bg']='bisque'

	Frame1 = Frame(Message_prive,borderwidth=3,relief=GROOVE)
	Frame1.pack(padx=10,pady=10)
	
	Label1 = Label(Frame1, text = "Quel est le pseudo de l'utilisateur à qui vous souhaitez envoyer un message?", fg = 'black')
	Label1.pack(padx=5,pady=5)

	Champ = Entry(Frame1, bg ='white', fg='grey')
	Champ.focus_set()
	Champ.pack(padx=5, pady=5)
	
	Label2 = Label(Frame1, text = "Quel est votre message?", fg = 'black')
	Label2.pack(padx=5,pady=5)
	
	Champ1 = Entry(Frame1, bg ='white', fg='grey')
	Champ1.pack(padx=5, pady=5)

	Bouton1 = Button(Frame1, text = 'Valider', command = lambda: sendMPandDestroy(Champ1.get(),Champ.get(),Message_prive))
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

	Bouton1 = Button(Frame2, text = 'Rejoindre un serveur existant', command = lambda: choix_ip_et_destroy(Authentification)) #***********
	Bouton1.pack(side=LEFT, padx = 5, pady=5)

	Bouton2 = Button(Frame2, text = 'Créer un nouveau serveur', command = Authentification.destroy) #************
	Bouton2.pack(side=LEFT, padx = 5, pady=5)

	# Création d'un bouton quitter
	Bouton3 = Button(Frame2, text = 'Quitter', command = Authentification.destroy)
	Bouton3.pack(side=LEFT, padx = 5, pady=5)

	# Lancement du gestionnaire d'événements
	Authentification.mainloop()

	return Pseudo.get()

def connect_and_destroy(ip,fenetre,port=port_serveur):
	"""
	Fonction écran permettant d'éxécuter deux sous fonctions pour un seul boutton.
	"""
	client.ConnectNewServer(ip, port)
	fenetre.destroy()

def choisir_ip():
	Nouvelle_connection=Tk()
	Nouvelle_connection.title('Engrenages')
	Nouvelle_connection.geometry('300x180')
	Nouvelle_connection['bg']='bisque'

	Frame1 = Frame(Nouvelle_connection,borderwidth=3,relief=GROOVE)
	Frame1.pack(padx=10,pady=10)

	Label1 = Label(Frame1, text = "Quelle est l'adresse IP du serveur à rejoindre?", fg = 'black')
	Label1.pack(padx=5,pady=5)

	Champ = Entry(Frame1, bg ='white', fg='grey')
	Champ.focus_set()
	Champ.pack(padx=5, pady=5)
	
	Label2 = Label(Frame1, text = "Quel port souhaitez-vous utiliser?", fg = 'black')
	Label2.pack(padx=5,pady=5)
	
	Port= StringVar()
	Port.set(port_serveur)
	Champ1 = Entry(Frame1, textvariable= Port, bg ='white', fg='grey')
	Champ1.focus_set()
	Champ1.pack(padx=5, pady=5)

	Bouton1 = Button(Frame1, text = 'Valider', command = lambda: connect_and_destroy(Champ.get(),Nouvelle_connection, int(Port.get())))
	Bouton1.pack(padx = 5, pady=5)

	Nouvelle_connection.mainloop()
	
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

	client.StringVar_pseudo_list = StringVar(value=pseudo)
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

	Bouton1 = Button(Frame4, text = 'Envoyer', command = lambda: sendTimedMessage(Message.get()))  #Envoi un message
	Bouton1.pack(padx=5,pady=5, side= LEFT)

	Frame5 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame5.place(x=575,y=360)

	Bouton2 = Button(Frame5, text = 'Déconnexion', command = shutdown)
	Bouton2.pack(padx=5,pady=5, side= LEFT)
	
	Frame6 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame6.place(x=50,y=350)
	
	Bouton3 = Button(Frame6, text = 'Message Privé', command = MP )
	Bouton3.pack(padx=5,pady=5)
	
	Frame7 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame7.place(x=550,y=310)
	
	Bouton4 = Button(Frame7, text = 'Connexion simultanée', command = choisir_ip )
	Bouton4.pack(padx=5,pady=5)

	# Lancement du gestionnaire d'événements
	Engrenages.mainloop()

class Serveur(threading.Thread):
	"""Class chargée du serveur."""

	def __init__(self):
		self.socket_list = []

		self.client = None # Sera défini après.

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
			ready_to_read, ready_to_write, in_error = select.select(self.socket_list,self.socket_list,[])
			for sock in ready_to_read:
				# Une nouvelle connection!
				if sock == self.s:
					newsocket, addr = self.s.accept()
					self.socket_list.append(newsocket)
					print ("SERVEUR: Client connecté, d'adresse: "+str(addr[0]))

				# Un message d'un client existant
				else:
					# Reception des données...
					data = sock.recv(size)
					if data:
						data = pickle.loads(data) # Décodage de ces données
						if data[3] == "SYSTEM" and data[1] == "NEW_CONN": # Message système, reception d'un nouveau pseudo
							if data[2] in client.pseudo_list:
								sendTimedMessage("DISCONNECT_BAD_PSEUDO","SYSTEM", [sock]) # déconnecte de force, le nouvel arrivé à déjà un pseudo existant.
							else:
								client.pseudo_list.append(data[2])
								client.update_StringVar_pseudo_list()
								client.update_StringVar_msg(data[2]+" est maintenant connecté") # Affiche le message de connection
								sendTimedMessage(client.pseudo_list,"SYSTEM") # Envoi à tout le monde sa liste, mise à jour.

						else:
							self.socket_list[1].send(pickle.dumps(data)) # Envoi du message à notre client local

					else:
					# Il n'y a rien, le client est sans doute déconnecté
						if sock in self.socket_list:
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

		self.pseudo=pseudo

		self.msg = None # Le type sera changé par fentere_princ()
		self.StringVar_pseudo_list = None

		self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.id_list=[]
		self.pseudo_list = [] # Ajoute notre pseudo à la liste des pseudos (précédé du nom du premier socket, le notre)

		threading.Thread.__init__(self)

	def run(self):
		"""Code à exécuter pendant l'exécution du client."""
		#On se connecte au serveur local
		self.server_sock.connect(('',port_serveur))
		while 1:
			# Un message d'un client existant
			data = self.server_sock.recv(size) # Reception des données...

			if data:
	                	# Des données sont arrivées
				data = pickle.loads(data) # Décodage de ces données

				if data[0] not in self.id_list: # data[0] correspond à l'id du message
					self.id_list.append(data[0]) # Ajoute l'id du message, il ne sera pas rééaffiché en cas de nouvelle récéption

					if data[3] == "": # Message non privé
						self.update_StringVar_msg(data[2]+": "+data[1]) # Affiche le message

					else: #Il s'agit d'un message privé
						if data[3] == self.pseudo: # Qui nous est destiné
							self.update_StringVar_msg(data[2]+" vous chuchotte: "+data[1]) # Affiche le message

						elif data[3] == "SYSTEM": # Message système, reception d'un pseudo, ou d'une liste de pseudo
							if data[1] == "DISCONNECT":
								self.pseudo_list.remove(data[2])
								self.update_StringVar_pseudo_list()
								self.update_StringVar_msg(data[2]+" est déconnecté") # Affiche le message de connection

							elif data[1] == "DISCONNECT_BAD_PSEUDO":
								self.update_StringVar_msg("Déconnection générale, mauvais pseudo.") # Affiche le message de déconnection
								shutdown(True)

							elif type(data[1]) is list:
								isNew, self.pseudo_list = diff_pseudo(data[1],self.pseudo_list)
								if isNew:
									sendTimedMessage(self.pseudo_list,"SYSTEM")
									self.update_StringVar_pseudo_list()

					sendMessage(data, serveur.socket_list[1:]) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

	def ConnectNewServer(self, ip, port=port_serveur):
		"""
		Permet de se connecter à un nouveau serveur.
		"""
		# Création d'un socket pour la nouvelle connection
		ysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			ysock.connect((ip,port))# On se connecte au nouveau serveur.
			print("CLIENT: Connecté au serveur distant d'ip "+str(ip)+".")
			serveur.socket_list.append(ysock) # On l'ajoute à la liste du serveur.

			sendTimedMessage("NEW_CONN","SYSTEM",[ysock]) # Envoi son pseudo au serveur distant, pour vérification
		except Exception as e:
				print("CLIENT: Quelque chose s'est mal passé avec %s:%d. l'exception est %s" % (ip,port, e))

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

	def update_StringVar_msg(self, new_message):
		"""
		Met à jour la liste des messages. Prend en argument new_message, un string.
		"""
		while isinstance(self.msg,StringVar) == False: # Attends l'initialisation de la fenêtre graphique
			pass
		if isinstance(self.msg,StringVar): # Vérifie que la variable a bien été initialisée dans la fenêtre principale
			messages_prec=self.msg.get()
			self.msg.set(messages_prec+new_message+"\n")

parser = argparse.ArgumentParser() # Prend en compte les arguments
parser.add_argument("--serveur", help="Lance engrengages en mode serveur. Prends le pseudo en argument")
args = parser.parse_args()

serveur = Serveur()
serveur.start()
time.sleep(1)
client = Client(serveur)
serveur.client=client
client.start()
time.sleep(1)

if args.serveur == None:
	pseudo = identification(client)
else:
	pseudo = args.serveur

serveur.pseudo = pseudo
client.pseudo=pseudo
client.pseudo_list.append(pseudo)

#client.ConnectNewServer("", 6667) #Connecte sur une autre instance s'executant sur le port 6667 du même ordinateur.
if args.serveur == None:
	fenetre_princ(pseudo, client) #Fenêtre principale
else:
	print("Entrée en mode serveur. Attends des connections.")
