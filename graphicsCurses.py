#!/usr/bin/python3

import curses

def txt_princ(pseudo,rouage):
	running = True
	stdscr = curses.initscr() # Fenêtre principale
	curses.echo() # Désactive l'écho

	rouage.msg_text = curses.newwin(curses.LINES -2, 3*int((curses.COLS-1)/4), 0, 0)
	rouage.msg_text.addstr(0,0,"Bienvenue dans engrenages.\nAppuyez sur Entrée pour envoyer.\nTapez \help pour de l'aide\n\n")

	new_msg = curses.newwin(1, curses.COLS - 23, curses.LINES - 1, 0)
	new_msg.addstr(0,0,"Entrez votre message: ")

	pseudos = curses.newwin(2, int((curses.COLS-1)/4), 0, 3*int((curses.COLS-1)/4))
	pseudos.addstr(0,0,"Utilisateurs")

	rouage.StringVar_pseudo_list = curses.newwin(curses.LINES - 3-1, int((curses.COLS-1)/4), 2, 3*int((curses.COLS-1)/4))
	rouage.StringVar_pseudo_list.addstr(pseudo)
	rouage.StringVar_pseudo_list.refresh()
	rouage.msg_text.refresh()
	new_msg.refresh()
	pseudos.refresh()

	while running:
		editwin = curses.newwin(2, curses.COLS - 1, curses.LINES - 1, 22)
		editwin.refresh()
		message=editwin.getstr(0,0).decode(encoding="utf-8")

		msg = message.split() # Transforme le message en tableau de string.

		if msg[0] == "\quit":
			running=False
		elif msg[0] == "\mp":
			content=""
			if len(msg) >= 3:
				if msg[1] != "SYSTEM":
						for x in range(len(msg[2:])):
							content += msg[2+x]+" " # Concatène
						rouage.sendTimedMessage(content,msg[1])
		elif msg[0] == "\connect":
			if len(msg) >= 3 and msg[2].isallnum(): # Vérifie que tous les arguments sont présetns et que le port est un nombre.
				rouage.ConnectNewServer(msg[1],int(msg[2]))

		elif msg[0] == "\help":
			rouage.update_msg_text("Aide:\n Tapez votre message puis entrée pour l'envoyer\n Tapez \quit pour quitter\n Tapez \mp destinataire votre message pour envoyer un message privé\n Tapez \connect ip port pour vous connecter")

		else:
			rouage.sendTimedMessage(message)
	curses.endwin()
	rouage.quit()
