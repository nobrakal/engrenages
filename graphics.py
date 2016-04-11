#!/usr/bin/python3

from tkinter import *
from tkinter.messagebox import *

def sendMPandDestroy(msg, pseudo, fenetre, rouage ):
	rouage.sendTimedMessage(msg,pseudo)
	fenetre.destroy()

def destroy_and_shutdown(rouage, fenetre):
	fenetre.destroy()
	rouage.quit()

def MP(rouage):
	"""
	Fonction ouvrant une fenêtre permettant d'envoyer un message privé à l'utilisateur choisi
	"""
	Message_prive=Tk() #définit Message_prive comme une fenêtre Tkinter
	Message_prive.title('Engrenages') #titre de la fenêtre
	Message_prive.geometry('450x180') #dimensions de la fenêtre
	Message_prive['bg']='bisque' # couleur de fond

	MainFrame = Frame(Message_prive,borderwidth=3,relief=GROOVE) #crée la sous-fenêtre principale
	MainFrame.pack(padx=10,pady=10) #instruction plaçant la sous-fenêtre principale dans la fenêtre
	
	Label1 = Label(MainFrame, text = "Quel est le pseudo de l'utilisateur à qui vous souhaitez envoyer un message?", fg = 'black') # crée une zone de texte dans la sous-fenêtre principale
	Label1.pack(padx=5,pady=5) #instruction plaçant la zone de texte dans la sous-fenêtre principale

	ChoixPseudo = Entry(MainFrame, bg ='white', fg='grey') #crée une zone de saisie de texte par l'utilisateur
	ChoixPseudo.focus_set()
	ChoixPseudo.pack(padx=5, pady=5) #instruction plaçant la zone de saisie de texte dans la sous-fenêtre principale
	
	Label2 = Label(MainFrame, text = "Quel est votre message?", fg = 'black') # crée une zone de texte dans la sous-fenêtre principale
	Label2.pack(padx=5,pady=5) #instruction plaçant la zone de texte dans la sous-fenêtre principale
	
	Message = Entry(MainFrame, bg ='white', fg='grey') #crée une zone de saisie de texte par l'utilisateur
	Message.pack(padx=5, pady=5) #instruction plaçant la zone de saisie de texte dans la sous-fenêtre principale

	Bouton1 = Button(MainFrame, text = 'Valider', command = lambda: sendMPandDestroy(Message.get(),ChoixPseudo.get(),Message_prive,rouage)) #crée un bouton permettant de détruire la fenêtre
	Bouton1.pack(padx = 5, pady=5) #instruction plaçant le bouton dans la sous-fenêtre principale

	Message_prive.mainloop() #permet de signifier que le programme de création de la fenêtre est fini

def check_pseudo(pseudo, fenetre):
	"""
	Fonction vérifiant si le pseudo entré par l'utilisateur est valide (c'est-à-dire pas vide ni "DESTROY")
	"""
	if pseudo == "" or pseudo == "DESTROY" :
		showwarning("Attention !", "Vous devez entrer un pseudo valide pour vous connecter !")
	else:
		fenetre.destroy()

def pre_shutdown(rouage,fenetre, Pseudo):
	Pseudo.set("DESTROY")
	fenetre.destroy()
	rouage.quit()

def identification(rouage):
	"""
	Fenêtre d'identification qui permet à l'utilisateur de choisir son pseudo
	"""
	Authentification = Tk()
	# Création de la fenêtre principale
	Authentification.title('Engrenages')
	Authentification.geometry('410x170')
	Authentification['bg']='bisque' # couleur de fond

	#crée le champ de saisie pour entrer le pseudo
	Pseudo = StringVar()

	Authentification.protocol("WM_DELETE_WINDOW",lambda: pre_shutdown(rouage, Authentification, Pseudo)) # Utilise une fonction maison pour quitter

	#Création de deux sous-fenêtres
	Frame1 = Frame(Authentification,borderwidth=2,relief=GROOVE)
	Frame1.pack(padx=10,pady=10)

	Frame2 = Frame(Authentification,borderwidth=2,relief=GROOVE)
	Frame2.pack(padx=10,pady=10)

	# Création d'un widget Label affichant le texte: "Veuillez entrer votre Pseudo !"
	Label1 = Label(Frame1, text = 'Veuillez entrer votre Pseudo', fg = 'black', bg='lightgrey')
	Label1.pack(padx=5,pady=5) #positionne le widget Label1

	Champ = Entry(Frame1, textvariable= Pseudo,bg ='white', fg='grey')
	Champ.focus_set()
	Champ.pack(padx=5, pady=5)

	Go = Button(Frame2, text = 'Lancer engrenages!', command = lambda: check_pseudo(Champ.get(), Authentification)) #************
	Go.pack(side=LEFT, padx = 5, pady=5)

	Authentification.mainloop() #permet de signifier que le programme de création de la fenêtre est fini

	return Pseudo.get()

def connect_and_destroy(ip,fenetre,rouage,port):
	"""
	Fonction écran permettant d'éxécuter deux sous fonctions pour un seul boutton.
	"""
	rouage.ConnectNewServer(ip, port)
	fenetre.destroy()

def choisir_ip(rouage, port_serveur):
	"""
	Fonction qui ouvre une fenêtre de connexion à un autre serveur. Elle demande à l'utilisateur d'entrer l'adresse et le port du serveur à rejoindre.
	"""
	Nouvelle_connection=Tk() #définit Nouvelle_connection comme une fenêtre Tkinter...
	Nouvelle_connection.title('Engrenages') #...de titre "Engrenages"...
	Nouvelle_connection.geometry('300x180') #...de dimensions 300x180...
	Nouvelle_connection['bg']='bisque' #...et de fond de couleur "bisque"

	Frame1 = Frame(Nouvelle_connection,borderwidth=3,relief=GROOVE)
	Frame1.pack(padx=10,pady=10)

	Label1 = Label(Frame1, text = "Quelle est l'adresse IP du serveur à rejoindre?", fg = 'black')
	Label1.pack(padx=5,pady=5)

	Champ = Entry(Frame1, bg ='white', fg='grey')
	Champ.focus_set()
	Champ.pack(padx=5, pady=5)
	
	Label2 = Label(Frame1, text = "Quel port souhaitez-vous utiliser?", fg = 'black')
	Label2.pack(padx=5,pady=5)
	
	Port = Entry(Frame1, bg ='white', fg='grey')
	Port.focus_set()
	Port.pack(padx=5, pady=5)

	Bouton1 = Button(Frame1, text = 'Valider', command = lambda: connect_and_destroy(Champ.get(),Nouvelle_connection,rouage, int(Port.get())))
	Bouton1.pack(padx = 5, pady=5)

	Nouvelle_connection.mainloop() #permet de signifier que le programme de création de la fenêtre est fini
	
def fenetre_princ(pseudo, rouage, port_serveur):
	Engrenages = Tk()
	Engrenages.title('Engrenages:'+ pseudo)
	Engrenages['bg']='bisque' # couleur de fond

	Engrenages.protocol("WM_DELETE_WINDOW",lambda: destroy_and_shutdown(rouage, Engrenages)) # Utilise une fonction maison pour quitter

	Label1 = Label(Engrenages, text = 'Engrenages', fg = 'black', justify='center', padx=5, pady=5)
	Label1.grid(row=0,column=2)

	Label2 = Label(Engrenages, text = 'Messages précédents', fg = 'black', anchor=SE)
	Label2.grid(row=0,column=0)

	FrameMessages=Frame()
	FrameMessages.grid(row=1,column=0, columnspan = 4, rowspan = 2, sticky = SE)

	scrollbary = Scrollbar(FrameMessages)
	scrollbary.grid(row=0, column=1)

	rouage.msg_text = Text(FrameMessages,yscrollcommand=scrollbary.set) # Affiche les messages précédents
	rouage.msg_text.configure(state=DISABLED)
	rouage.msg_text.grid(row=0,column=0)

	scrollbary.config(command=rouage.msg_text.yview)

	FrameConnected = Frame()
	FrameConnected.grid(row=0,column=5,rowspan = 2, sticky = S)

	Label4 = Label(FrameConnected, text = 'Utilisateurs connectés', fg = 'black', bg="lightgrey")
	Label4.pack(side=TOP,expand = 1,fill=BOTH)

	rouage.StringVar_pseudo_list = StringVar(value=pseudo)
	Label5 = Label(FrameConnected, textvariable = rouage.StringVar_pseudo_list, fg = 'black', bg="lightgrey", justify='left') #liste des utilisateurs connectés
	Label5.pack(side=TOP)

	Bouton4 = Button(FrameConnected, text = 'Nouvelle connexion', command =lambda: choisir_ip(rouage, port_serveur) )
	Bouton4.pack(side=TOP)

	Label6 = Label(Engrenages, text = 'Votre message:', fg = 'black', bg="lightgrey")
	Label6.grid(row=3,column=1)

	Message = StringVar()
	Champ = Entry(Engrenages, textvariable= Message, bg ='white', fg='grey')
	Champ.focus_set()
	Champ.grid(row=3,column=2)

	Bouton1 = Button(Engrenages, text = 'Envoyer', command = lambda: rouage.sendTimedMessage(Message.get()))  #Envoi un message
	Bouton1.grid(row=3,column=3)

	Bouton2 = Button(Engrenages, text = 'Quitter', command =lambda: destroy_and_shutdown(rouage, Engrenages))
	Bouton2.grid(row=3,column=4)
	
	Bouton3 = Button(Engrenages, text = 'Message Privé', command =lambda: MP(rouage) )
	Bouton3.grid(row=3,column=0)

	Engrenages.mainloop() #permet de signifier que le programme de création de la fenêtre est fini
