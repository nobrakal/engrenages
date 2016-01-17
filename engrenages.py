#!/usr/bin/python3

""" 
A simple echo server 
""" 

import socket 

host = '' 
port = 80 
backlog = 5 
size = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog) 
client, address = s.accept() 
while 1: 
	data = client.recv(size) 
	if data.decode() == "exit\r\n":
		client.close()
		break
	elif data: 
		client.send(data)
