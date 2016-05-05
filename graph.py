#!/usr/bin/python3

class Graph:
	"""
	Classe permettant de gérer le graphique représentant les connexions du réseau.
	"""
	def __init__(self):
		self.pseudo=None
		self.pseudo_list=[]
		self.graphique=[[True]]

	def add(self, pseudo):
		"""
		Ajoute un pseudo au graph
		"""
		self.pseudo_list.append(pseudo)
		for a in range(len(self.pseudo_list)-1): # On ajoute une colonne aux lignes existantes
			self.graphique[a].append(False)
		self.graphique.append([False]*len(self.pseudo_list)) # On ajoute une ligne "vide" que l'on modifiera après

	def connect(self, pseudo,pseudo2):
		"""
		Connecte deux pseudos entre eux
		"""
		index=self.pseudo_list.index(pseudo)
		index2=self.pseudo_list.index(pseudo2)
		if index != index2: # Empêche les connexions à soi-même
			self.graphique[index][index2]=True
			self.graphique[index2][index]=True

	def remove(self, pseudo):
		"""
		Supprime un pseudo du graph
		"""
		removed=[]
		pseudo_index=self.pseudo_list.index(pseudo)
		for a in range(len(self.pseudo_list)):
			self.graphique[a].pop(pseudo_index)
		self.graphique.pop(pseudo_index)
		self.pseudo_list.remove(pseudo)
		for x in range(len(self.pseudo_list)):
			if True not in self.graphique[x]:# Un utilisateur plus connecté à personne
				self.graphique.pop(x)
				removed.append(self.pseudo_list.pop(x))

		return removed
