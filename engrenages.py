#!/usr/bin/python3

import socket
import select
import threading
import pickle
import time
import argparse

from rouage import *
from graphics import *

port_serveur= 6666

parser = argparse.ArgumentParser() # Prend en compte les arguments
parser.add_argument("--pseudo", help="Lance engrengages avec un pseudo")
args = parser.parse_args()

rouage = Rouage(port_serveur, 10, 1024)
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

	fenetre_princ(pseudo, rouage, port_serveur) #Fenêtre principale

rouage.join()
print("See you soon")
