#!/usr/bin/python3

""" 
A simple echo server 
""" 

import socket 
import select
import ssl

host = '' 
port = 80 
backlog = 10 # Nombre de connections maximum
size = 1024 
socket_list = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port)) 
s.listen(backlog) 

socket_list.append(s)
while 1: 
	# prend une liste des socket prêt à être lu.
	ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[])

	for sock in ready_to_read:
		# Une nouvelle connection!
		if sock == s: 
			newsocket, addr = s.accept()
			socket_list.append(newsocket)
			print ("Client connecté")

		# Un message d'un client existant
		else: 
			try:
			# Reception des données...
				data = sock.recv(size)
				if data:
                        	# Des données sont arrivées
					print(data) 
				else:
				# Il n'y a rien, le client est sans doute déconnecté
					if sock in socket_list:
						socket_list.remove(sock)
					print("Client perdu")

			# exception 
			except:
				if sock in socket_list:
					socket_list.remove(sock)
				print("Client perdu")
				continue
s.close()
