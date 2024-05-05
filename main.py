import pygame, os
from game import Game

pygame.init()

'''
patch_note memo:
    correction du beug de traduction des dialoges des pnjs qui ne changaient pas de langue


    afficher les questes ou non via un parametre d'affichage


idées : 
    dans le dj ajouter un téléporteur vers une salle de boss et y mettre le pnj du boss
'''

# vérifie si le dossier 'saves' existe (si le jeu est pas compiler)
if not os.path.exists(r'saves'):
    if not os.path.exists(r'_internal'):
        os.makedirs(r'saves')
    elif not os.path.exists(r'_internal\saves'):
        os.makedirs(r'_internal\saves')

game = Game()

try:
    game.run()
except pygame.error:
    print('le joueur a quitter le jeu')