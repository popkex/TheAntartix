import pygame, os
from game import Game

pygame.init()

'''
a faire impérativement
    creer une fonction (load_txt par exemple) qui va charger le txt fournis dans le current_language et que si il y a une erreur le charge
    dans la langue par defaut (fr)


    bloquer l'utilisation des poitions si le joueurs est full hp !!!!!!!!!!!!!!!!!!!!!!!!!!!
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