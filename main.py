import pygame, os
from game import Game

pygame.init()

'''
a faire impérativement
    changer le mode de fonctionnement du screen de mort et le traduire !!!!

ajouter des png (a faire)
'''

# vérifie si le dossier 'saves' existe (si le jeu est pas compiler)
if not os.path.exists(r'saves'):
    if not os.path.exists(r'_internal'):
        os.makedirs(r'saves')
    elif not os.path.exists(r'_internal\saves'):
        os.makedirs(r'_internal\saves')

game = Game()
game.run()