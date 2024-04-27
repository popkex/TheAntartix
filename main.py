import pygame, os
from game import Game

pygame.init()

'''
memo patch note :
    correction d'un beug d'xp
    correction beug de l'inventaire
        les objets s'ajoutais en quantité de 1 à chaque fois
    modification rapide de la taille de la bar d'exp
    quand le joueur gagne un combat, il gagne un objet 
'''

game = Game()

# vérifie si le dossier 'saves' existe (si le jeu est pas compiler)
if not os.path.exists(r'saves') and not os.path.exists(r'_internal'):
    os.makedirs(r'saves')
elif not os.path.exists(r'_internal\saves'):
    os.makedirs(r'_internal\saves')

game.run()