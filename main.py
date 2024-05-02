import pygame, os
from game import Game

pygame.init()

'''
ajout d'un tutoriel (en cours) (faire celui du combat)
les enemies spawn uniquement dans des dj prevus a cette effet (a faire)
ajouter des png
'''

# vérifie si le dossier 'saves' existe (si le jeu est pas compiler)
if not os.path.exists(r'saves'):
    if not os.path.exists(r'_internal'):
        os.makedirs(r'saves')
    elif not os.path.exists(r'_internal\saves'):
        os.makedirs(r'_internal\saves')

game = Game()
game.run()