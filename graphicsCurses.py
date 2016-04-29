#!/usr/bin/python3

import curses
from curses.textpad import Textbox, rectangle

def txt_princ(pseudo,rouage):
	running = True
	stdscr = curses.initscr() # Fenêtre principale
	curses.echo() # Désactive l'écho

	rouage.msg_text = curses.newwin(curses.LINES - 2-1, 3*int((curses.COLS-1)/4), 0, 0)
	rouage.msg_text.addstr(0,0,"Bienvenue dans engrenages.\nAppuyez sur CTRL-G pour envoyer.\nTapez \quit pour quitter\n")

	new_msg = curses.newwin(2, curses.COLS - 23, curses.LINES - 1, 0)
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

		if message == "\quit":
			running=False
		else:
			rouage.sendTimedMessage(message+"\n")
	curses.endwin()
	rouage.quit()
