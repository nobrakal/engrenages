#!/usr/bin/python3

import socket
import select
import threading
import pickle
import time
import argparse

from rouage import *
from graphics import *

parser = argparse.ArgumentParser() # Prend en compte les arguments
parser.add_argument("--pseudo", help="Lance engrengages avec un pseudo")
parser.add_argument("--port", help="Lance engrengages sur le port précisé")
args = parser.parse_args()

if args.port == None:
	args.port = 6666

rouage = Rouage(int(args.port), 10, 1024)
rouage.start()
time.sleep(1)

pseudo=""

if args.pseudo == None:
	while pseudo == "":
		pseudo = identification(rouage)
			
else:
	pseudo = args.pseudo

if pseudo != "DESTROY":
	rouage.pseudo = pseudo
	rouage.pseudo_list.append(pseudo)

	fenetre_princ(pseudo, rouage, int(args.port)) #Fenêtre principale

rouage.join()
print("See you soon")
