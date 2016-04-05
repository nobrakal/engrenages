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
	
	Port= StringVar()
	Port.set(port_serveur)
	Champ1 = Entry(Frame1, textvariable= Port, bg ='white', fg='grey')
	Champ1.focus_set()
	Champ1.pack(padx=5, pady=5)

	Bouton1 = Button(Frame1, text = 'Valider', command = lambda: connect_and_destroy(Champ.get(),Nouvelle_connection,rouage, int(Port.get())))
	Bouton1.pack(padx = 5, pady=5)

	Nouvelle_connection.mainloop() #permet de signifier que le programme de création de la fenêtre est fini
	
def fenetre_princ(pseudo, rouage, port_serveur):
	Engrenages = Tk()
	Engrenages.title('Engrenages:'+ pseudo)
	Engrenages.geometry('770x420')
	Engrenages['bg']='bisque' # couleur de fond

	Engrenages.protocol("WM_DELETE_WINDOW",lambda: destroy_and_shutdown(rouage, Engrenages)) # Utilise une fonction maison pour quitter

	Frame1 = Frame(Engrenages,borderwidth=3,relief=GROOVE)
	Frame1.pack(padx=10,pady=10)

	Label1 = Label(Frame1, text = 'Engrenages', fg = 'black')
	Label1.pack(padx=5,pady=5)

	Frame2 = LabelFrame(Engrenages,borderwidth=2,relief=GROOVE, bg="lightgrey", text="Messages précédents")
	Frame2.place(x=15,y=75)

	rouage.msg = StringVar()
	Label3 = Label(Frame2, textvariable = rouage.msg, fg = 'black', bg="white",height=15,width=70) #affiche les messages précédents
	Label3.pack(padx=5,pady=5, side=TOP)

	Frame3 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame3.place(x=600,y=75)

	Label4 = Label(Frame3, text = 'Utilisateurs connectés', fg = 'black', bg="lightgrey")
	Label4.pack(padx=5,pady=5, side=TOP)

	rouage.StringVar_pseudo_list = StringVar(value=pseudo)
	Label5 = Label(Frame3, textvariable = rouage.StringVar_pseudo_list, fg = 'black', bg="lightgrey") #liste des utilisateurs connectés
	Label5.pack(padx=5,pady=5)

	Frame4 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame4.pack(padx=10,pady=10, side=BOTTOM)

	Label6 = Label(Frame4, text = 'Votre message:', fg = 'black', bg="lightgrey")
	Label6.pack(padx=5,pady=5, side=LEFT)

	Message = StringVar()
	Champ = Entry(Frame4, textvariable= Message, bg ='white', fg='grey')
	Champ.focus_set()
	Champ.pack(padx=5, pady=5, side=LEFT)

	Bouton1 = Button(Frame4, text = 'Envoyer', command = lambda: rouage.sendTimedMessage(Message.get()))  #Envoi un message
	Bouton1.pack(padx=5,pady=5, side= LEFT)

	Frame5 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame5.place(x=635,y=370)

	Bouton2 = Button(Frame5, text = 'Quitter', command =lambda: destroy_and_shutdown(rouage, Engrenages))
	Bouton2.pack(padx=5,pady=5)
	
	Frame6 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame6.place(x=30,y=370)
	
	Bouton3 = Button(Frame6, text = 'Message Privé', command =lambda: MP(rouage) )
	Bouton3.pack(padx=5,pady=5)
	
	Frame7 = Frame(Engrenages, borderwidth=2, relief=GROOVE, bg="lightgrey")
	Frame7.place(x=600,y=320)
	
	Bouton4 = Button(Frame7, text = 'Nouvelle connexion', command =lambda: choisir_ip(rouage, port_serveur) )
	Bouton4.pack(padx=5,pady=5)

	Engrenages.mainloop() #permet de signifier que le programme de création de la fenêtre est fini
