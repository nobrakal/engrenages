#!/usr/bin/python3

import socket
import select
import threading
import pickle
import argparse

from rouage import *
from graphics import *

parser = argparse.ArgumentParser() # Prend en compte les arguments
parser.add_argument("--pseudo", help="Lance engrengages avec un pseudo")
parser.add_argument("--port", help="Lance engrengages sur le port précisé")
parser.add_argument("--gui", help="Si 1, lance engrenages en mode graphique (DEFAUT), si 0 lance engrenages en mode text")
parser.add_argument("--debug", help="Si 1, lance engrenages en mode debug, si 0 lance engrenages normalement (DEFAUT)")
args = parser.parse_args()

if args.gui == None:
	gui = True
else:
	gui = False

if args.port == None:
	args.port = 6666

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

if args.debug != None:
	rouage.debug = True

if gui == True and pseudo != "":
	rouage.gui = True
	fenetre_princ(pseudo, rouage, int(args.port)) #Fenêtre principale
else:
	txt_princ(pseudo,rouage)

rouage.join()
print("See you soon")
