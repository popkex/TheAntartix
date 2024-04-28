import pygame, os
from game import Game

pygame.init()

game = Game()

'''
faire des animations : 
    - des combats
    - des déplacements

mettre des pngs
    - les faires déplacer

pour la sortie du jeu :
    - faire une map grande avec des secrets

pour l'eau : 
    - spirt1 : goute
    - spirt2 : pas goute
'''


# vérifie si le dossier 'saves' existe (si le jeu est pas compiler)
if not os.path.exists(r'saves'):
    if not os.path.exists(r'_internal'):
        os.makedirs(r'saves')
    elif not os.path.exists(r'_internal\saves'):
        os.makedirs(r'_internal\saves')

game.run()