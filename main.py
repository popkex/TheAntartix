import pygame, os
from game import Game

pygame.init()

game = Game()

# vérifie si le dossier 'saves' existe (si le jeu est pas compiler)
try:
    if not os.path.exists(r'saves'):
        os.makedirs(r'saves')
except: 
    pass

game.run()