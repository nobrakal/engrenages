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

port_serveur = 6666
port_client = 6667
backlog = 10 # Nombre de connections maximum
size = 1024 

id_list = []

def sendTimedMessage(msg, socket_list):
	"""Envoi un message avec son id, le temps, à la liste de socke"""
	for sock in socket_list[1:]:
		time = datetime.datetime.now()
		id_list.append(time) # Ajoute notre propre message à la liste des messages envoyés
		sock.send(pickle.dumps((str(time)+msg))) # Envoi le temps afin d'éviter les boucles d'envoi infinies (=id du message), plus le message

def sendMessage(msg, socket_list):
	"""Envoi un message à la liste de socket"""
	for sock in socket_list[1:]:
		sock.send(pickle.dumps(msg)) # Envoi du message (réencodé).

class Serveur():
	"""Class chargée du serveur."""

	def __init__(self):
		self.socket_list = []
		self.active_sock_list = []

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind(('',port_serveur)) 
		self.s.listen(backlog) 

		self.socket_list.append(self.s)

		self.thread = threading.Thread(target=self.startServeur)
		self.thread.start()     

	def startServeur(self):
		"""Code à exécuter pendant l'exécution du serveur."""
		self.newsocket, self.addr = self.s.accept() # Attends la connection du client
		self.socket_list.append(self.newsocket)
		print("Client local connecté")
		while 1:
			# prend une liste des socket prêt à être lu.
			self.ready_to_read,self.ready_to_write,self.in_error = select.select(self.socket_list,[],[])
			for self.sock in self.ready_to_read:
				# Une nouvelle connection!
				if self.sock == self.s: 
					self.newsocket, self.addr = self.s.accept()
					print ("Client connecté")

					# On envoi l'adresse du client à notre client, pour qu'il puisse se connecter au serveur.
					self.socket_list[1].send(pickle.dumps(self.newsocket.getpeername()))


					if len(self.socket_list) != 0: # Cas où il ne reste plus qu'un seul socket, le notre, on n'envoit donc aucune adresse
						for self.active_sock in self.socket_list[1:]: # On envoi la liste des ip des connectés, sauf la notre
							self.active_sock_list.append(self.active_sock.getpeername())					
						self.newsocket.send(pickle.dumps(self.active_sock_list))
				
					self.socket_list.append(self.newsocket)
	
				# Un message d'un client existant
				else: 
					# Reception des données...
					self.data = self.sock.recv(size)
					if self.data:
       		                	# Des données sont arrivées
						self.data = pickle.loads(self.data)
						if self.data[:26] not in id_list: # Les 26 premiers charactères correspondent à la date
								print(self.data[26:])
								id_list.append(self.data[:26]) # Ajoute l'id du message, il ne sera pas rééaffiché en cas de nouvelle récéption
								sendMessage(self.data, self.socket_list) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

					else:
					# Il n'y a rien, le client est sans doute déconnecté
						if self.sock in self.socket_list:
							self.socket_list.remove(self.sock)
						print("Client perdu")
	
				if len(self.socket_list) == 1: # Cas où il ne reste plus qu'un seul socket, le notre.
					print("Fermeture, plus aucun client connecté")
					self.s.close()
					return 0
	def getSocketList(self):
		return self.socket_list

class Client():
	"""Class chargée du client"""

	def __init__(self):
		self.socket_list = []

		self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.socket_list.append(self.c)

		self.thread = threading.Thread(target=self.startClient)
		self.thread.start()     

	def startClient(self):
		"""Code à exécuter pendant l'exécution du client."""
		#On se connecte au serveur local
		self.ConnectNewServer('')
		while 1:
			# prend une liste des socket prêt à être lu.
			self.ready_to_read,self.ready_to_write,self.in_error = select.select([],self.socket_list,[])
			for self.sock in self.ready_to_read:
				# Un message d'un client existant
				# Reception des données...
				self.data = self.sock.recv(size)
				if self.data:
      		                	# Des données sont arrivées
					self.data = pickle.loads(self.data)
					if type(self.data) is list: #Premier message, liste d'ip
						print("Liste d'ip arrivées:" +str(pickle.loads(self.data)))
						self.ip_list = pickle.loads(self.data)
						for self.ip2connect in self.sock_list: # On s'y connecte
							self.c.connect((ip2connect,port_serveur))

					elif len(self.data) < 26: # Cas de reception d'une ip
						self.ConnectNewServer(self.data) # On s'y connecte
						
					elif self.data[:26] not in id_list: # Les 26 premiers charactères correspondent à la date
							print(self.data[26:])
							id_list.append(self.data[:26]) # Ajoute l'id du message, il ne sera pas rééaffiché en cas de nouvelle récéption
							sendMessage(self.data, self.socket_list) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

				else:
				# Il n'y a rien, le client est sans doute déconnecté
					if self.sock in self.socket_list:
						self.socket_list.remove(self.sock)
					print("Client perdu")
	
			if len(self.socket_list) == 1: # Cas où il ne reste plus qu'un seul socket, le notre.
				print("Fermeture, plus aucun client connecté")
				self.c.close()
				return 0

	def ConnectNewServer(self, ip, port=port_serveur):
		self.ip = ip
		self.port = port

		# Création d'un socket pour la nouvelle connection

		ysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			ysock.connect((self.ip,port))# On se connecte au nouveau serveur.
			self.socket_list.append(ysock)
			if ip != '':
				print("Connecté au serveur distant d'ip "+str(ip))
		except Exception as e: 
			print("Quelque chose c'est mal passé avec %s:%d. l'exception est %s" % (self.ip,port_serveur, e))



serveur = Serveur()
time.sleep(2)
client = Client()
time.sleep(2)

client.ConnectNewServer("78.205.80.129")
msg = input("Entrez votre message : ")
sendTimedMessage(msg,client.socket_list)
