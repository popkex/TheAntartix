import pygame
from game import Game
from inventory import *

pygame.init()

''' beug !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        quand l'objet existe déjà dans l'inventaire, et qu'il y est ajouter cela remplace le premier de la list avec lui
'''


'''
memo patch note :
    correction d'un beug d'xp
    correction beug de l'inventaire
        les objets s'ajoutais en quantité de 1 à chaque fois
    modification rapide de la taille de la bar d'exp
'''

game = Game()
# game.inventory.append_object(Life_Potion(game), 999)
# game.inventory.append_object(Big_Life_Potion(game), 999)
game.inventory.append_object(Bomb(game), 999)
game.run()