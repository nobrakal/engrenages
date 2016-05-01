#!/usr/bin/python3

import socket
import select
import threading
import pickle
import argparse

from rouage import *
from graphicsTk import *
from graphicsCurses import *

parser = argparse.ArgumentParser() # Prend en compte les arguments
parser.add_argument("--pseudo", help="Lance engrengages avec un pseudo")
parser.add_argument("--port",default=6666, help="Lance engrengages sur le port précisé")
parser.add_argument("--nogui",nargs="?",const=True,default=False, help="Si spécifié, lance engrenages en mode text")
parser.add_argument("--debug",nargs="?",const=True,default=False, help="Si spécifié, lance engrenages en mode debug")
args = parser.parse_args()

if args.nogui:
	gui = False
else:
	gui = True

rouage = Rouage(int(args.port), 10, 1024)
rouage.start()

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

rouage.pseudo = pseudo
rouage.pseudo_list.append(pseudo)

rouage.debug = args.debug

if gui == True and pseudo != "":
	rouage.gui = True
	fenetre_princ(pseudo, rouage, int(args.port)) #Fenêtre principale
else:
	txt_princ(pseudo,rouage)

rouage.join()
print("See you soon")
