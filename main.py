import pygame, os
from main_menu import MainMenu

pygame.init()

# vérifie si le dossier 'saves' existe (si le jeu est pas compiler)
if not os.path.exists(r'saves'):
    if not os.path.exists(r'TA-datas'):
        os.makedirs(r'saves')
    elif not os.path.exists(r'TA-datas\saves'):
        os.makedirs(r'TA-datas\saves')

main_menu = MainMenu()

try:
    main_menu.running()
except pygame.error:
    pass