import pygame, os
from game import Game
from inventory import *

pygame.init()

if not os.path.exists(r'saves'):
    os.makedirs(r'saves')

game = Game()
# game.inventory.append_object(Life_Potion(game), 999)
# game.inventory.append_object(Big_Life_Potion(game), 999)
game.inventory.append_object(Bomb(game), 999)
game.run()