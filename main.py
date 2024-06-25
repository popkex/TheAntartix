import pygame, os
from main_menu import MainMenu
from data_maps import DataMap

pygame.init()

# vérifie si le dossier 'saves' existe (si le jeu est pas compiler)
if not os.path.exists(r'saves'):
    if not os.path.exists(r'_internal'):
        os.makedirs(r'saves')
    elif not os.path.exists(r'_internal\saves'):
        os.makedirs(r'_internal\saves')

main_menu = MainMenu()

try:
    main_menu.running()
except pygame.error:
    pass