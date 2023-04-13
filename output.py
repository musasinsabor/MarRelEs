from glob import glob
import re


liste_fichiers = glob("./*.txt")

for fichier in liste_fichiers:
	entree = open(fichier, mode='r')
	print(entree.read())
	entree.close()
