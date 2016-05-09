#!/usr/bin/python3

import socket
import select
import threading
import pickle
import argparse

from rouage import *
from graphicsTk import *
try:
	from graphicsCurses import *
	gui=-2
except:
	gui = False

parser = argparse.ArgumentParser() # Prend en compte les arguments
parser.add_argument("--pseudo", help="Lance engrengages avec un pseudo")
parser.add_argument("--port",default=6666, help="Lance engrengages sur le port précisé")
parser.add_argument("--nogui",action='store_true', help="Si spécifié, lance engrenages en mode text")
parser.add_argument("--debug",action='store_true', help="Si spécifié, lance engrenages en mode debug")
args = parser.parse_args()

rouage = Rouage(int(args.port), 10, 1024)

if gui == False:
	print("Support de curses désactivé: Problème lors de l'import.")
	raise SystemExit
elif gui == True:
	print("Support de Tkinter désactivé: Problème lors de l'import.")
	raise SystemExit	
elif args.nogui:
	gui = False
else:
	gui = True

pseudo=""

if args.pseudo == None:
	if gui == True:
		pseudo = identification(rouage)
	else:
		pseudo = input("Entrez votre pseudo: ")

else:
	if args.pseudo != "SYSTEM":
		pseudo = args.pseudo
	else:
		rouage.quit()
		raise SystemExit

if pseudo == "":
	raise SystemExit

rouage.pseudo = pseudo
rouage.graph.pseudo=pseudo
rouage.graph.pseudo_list.append(pseudo)

rouage.debug = args.debug

rouage.start()

if gui == True and pseudo != "":
	rouage.gui = True
	fenetre_princ(pseudo, rouage, int(args.port)) #Fenêtre principale
else:
	txt_princ(pseudo,rouage)

rouage.join()
print("See you soon")
