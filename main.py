import pygame, os
from main_menu import MainMenu

pygame.init()

'''
patch_note memo:
    ajout:
        ajout de differentes quetes
        amélioration des traductions
        afficher les questes ou non via le menu pause > quetes
        ajout de messages systemes quand le joueur entre en combat
        permet de skip les dialogs/tuto en appuyant sur 'return' (entrer)
        ajout d'un menu principal avant de lancer le jeu
        ajout d'un bouton pour revenir au menu principal depuis le menu pause
        modifications du déplacement des pnj michel

    patch beug: 
        correction du beug de traduction des dialoges des pnjs qui ne changaient pas de langue
        correction de quand on ouvre l'inventaire et qu'on le ferme le joueur passe son tour
        correction, quand le joueur fermait le tuto de l'inventaire, le dialog restait afficher sans pouvoir le retirer

beug:
    None

idées : 
    dans le dj ajouter un téléporteur vers une salle de boss et y mettre le pnj du boss
    creer un menu de demarrage (a faire)
    ajouter un bouton menu principal dans le menu pause
'''

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