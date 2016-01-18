#!/usr/bin/python3

""" 
A simple echo server 
""" 

import socket 
import select
import threading
import datetime

port = 80 
backlog = 10 # Nombre de connections maximum
size = 1024 

class Serveur():
	"""Class chargée du serveur. Prend le host initial en argument (host='' si localhost)"""

	def __init__(self, host=''):
		self.host = host
		self.socket_list = []
		self.id_list = []
		self.stop = threading.Event()

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((host,port)) 
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
					self.socket_list.append(self.newsocket)
					print ("Client connecté")
	
				# Un message d'un client existant
				else: 
					# Reception des données...
					self.data = self.sock.recv(size)
					## print(self.data.decode())
					if self.data:
       		                	# Des données sont arrivées
						self.data = self.data.decode()
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
			self.sock.send((str(time)+self.msg).encode('utf-8')) # Envoi le temps afin d'éviter les boucles d'envoi infinies (=id du message), plus le message

	def sendMessage(self, msg):
		self.msg = msg
		for self.sock in self.socket_list[1:]:
			self.sock.send(self.msg.encode('utf-8')) # Envoi du message (réencodé).


serveur = Serveur()
