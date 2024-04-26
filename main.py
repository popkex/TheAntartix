import pygame, os
from game import Game
from inventory import *

pygame.init()

'''
memo patch note :
    correction d'un beug d'xp
    correction beug de l'inventaire
        les objets s'ajoutais en quantité de 1 à chaque fois
    modification rapide de la taille de la bar d'exp
    quand le joueur gagne un combat, il gagne un objet 
'''

if not os.path.exists(r'saves'):
    os.makedirs(r'saves')

game = Game()
# game.inventory.append_object(Life_Potion(game), 999)
# game.inventory.append_object(Big_Life_Potion(game), 999)
game.inventory.append_object(Bomb(game), 999)
game.run()