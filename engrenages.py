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

port_serveur = 80 
port_client = 81
backlog = 10 # Nombre de connections maximum
size = 1024 

class Serveur():
	"""Class chargée du serveur. Prend le host initial en argument (host='' si localhost)"""

	def __init__(self, host=''):
		self.host = host
		self.socket_list = []
		self.id_list = []
		self.active_sock_list = []

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((host,port_serveur)) 
		self.s.listen(backlog) 

		self.socket_list.append(self.s)

		self.thread = threading.Thread(target=self.startServeur)
		self.thread.start()     

	def startServeur(self):
		"""Code à exécuter pendant l'exécution du serveur."""
		while 1:
			# prend une liste des socket prêt à être lu.
			self.ready_to_read,self.ready_to_write,self.in_error = select.select(self.socket_list,[],[])
			for self.sock in self.ready_to_read:
				# Une nouvelle connection!
				if self.sock == self.s: 
					self.newsocket, self.addr = self.s.accept()
					print ("Client connecté")

					if len(self.socket_list) != 1: # Cas où il ne reste plus qu'un seul socket, le notre, on n'envoi donc aucune adresse
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
						if self.data[:26] not in self.id_list: # Les 26 premiers charactères correspondent à la date
								print(self.data[26:])
								self.id_list.append(self.data[:26]) # Ajoute l'id du message, il ne sera pas rééaffiché en cas de nouvelle récéption
								self.sendMessage(self.data) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

					else:
					# Il n'y a rien, le client est sans doute déconnecté
						if self.sock in self.socket_list:
							self.socket_list.remove(self.sock)
						print("Client perdu")
	
				if len(self.socket_list) == 1: # Cas où il ne reste plus qu'un seul socket, le notre.
					print("Fermeture, plus aucun client connecté")
					self.s.close()
					return 0

	def sendTimedMessage(self, msg):
		self.msg = msg
		for self.sock in self.socket_list[1:]:
			time = datetime.datetime.now()
			self.id_list.append(time) # Ajoute notre propre message à la liste des messages envoyés
			self.sock.send(pickle.dumps((str(time)+self.msg))) # Envoi le temps afin d'éviter les boucles d'envoi infinies (=id du message), plus le message

	def sendMessage(self, msg):
		self.msg = msg
		for self.sock in self.socket_list[1:]:
			self.sock.send(pickle.dumps(self.msg)) # Envoi du message (réencodé).

class Client():
	"""Class chargée du client. Prend le host initial en argument (host='' si localhost)"""

	def __init__(self, host=''):
		self.host = host
		self.socket_list = []
		self.id_list = []

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.socket_list.append(self.s)

		self.thread = threading.Thread(target=self.startClient)
		self.thread.start()     

	def startClient(self):
		"""Code à exécuter pendant l'exécution du client."""
		#On se connecte au serveur local
		self.s.connect(('',port_serveur))
		while 1:
			# prend une liste des socket prêt à être lu.
			self.ready_to_read,self.ready_to_write,self.in_error = select.select(self.socket_list,[],[])
			for self.sock in self.ready_to_read:
				# On se connecte à un serveur
				if self.sock == self.s: 
					self.newsocket, self.addr = self.s.accept()
					self.socket_list.append(self.newsocket)
						
				# Un message d'un client existant
				else: 
					# Reception des données...
					self.data = self.sock.recv(size)
					if self.data:
       		                	# Des données sont arrivées
						self.data = pickle.loads(self.data)
						if type(self.data) is list: #Premier message, liste d'ip
							self.ip_list = pickle.loads(self.data)
							for self.ip2connect in self.sock_list: # On s'y connecte
								self.s.connect((ip2connect,port_serveur))
							
						elif self.data[:26] not in self.id_list: # Les 26 premiers charactères correspondent à la date
								print(self.data[26:])
								self.id_list.append(self.data[:26]) # Ajoute l'id du message, il ne sera pas rééaffiché en cas de nouvelle récéption
								self.sendMessage(self.data) # Renvoi le message aux autres serveurs, afin d'assurer une propagation optimale

					else:
					# Il n'y a rien, le client est sans doute déconnecté
						if self.sock in self.socket_list:
							self.socket_list.remove(self.sock)
						print("Client perdu")
	
				if len(self.socket_list) == 1: # Cas où il ne reste plus qu'un seul socket, le notre.
					print("Fermeture, plus aucun client connecté")
					self.s.close()
					return 0

	def ConnectNewServer(self, ip):
		self.ip = ip
		self.s.connect((self.ip,port_serveur))# On se connecte au nouveau serveur.



serveur = Serveur()
time.sleep(2)
client = Client()
