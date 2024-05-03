import pygame, sys, os, time
from inventory import Inventory
from map import MapManager
from screen import Screen
from data_player import Data_Player
from player import Player
from fight import Fight
from fight_player import Fight_Player
from tutorial import Tutorial
from saves import Saves

class Game():

    def __init__(self):
        self.defaut_language = "fr"
        self.current_language, self.str_language = None, None

        self.inventory = Inventory(self)
        self.saves = Saves(self)
        self.data_player = Data_Player(self)
        self.data_player.load_attributes() # charge les attrbutes du joueur
        self.player = Player(0, 0)
        self.screen = Screen(self)
        self.map_manager = MapManager(self, self.screen.screen, self.player)
        self.tutorial = Tutorial(self)

        self.object_name_inventory = [] # met l'inventaire vide (avant de le charger et de le remplir)
        self.active_fight = False   # n'active pas de combat
        self.messages_system = [] # met aucun message systeme
        self.current_direction = 'up' #défini la direction par defaut

    def load_language(self, lang):
        if lang == 'en':
            import translation.english as new_language
            str_new_language = "en"
        elif lang == 'fr':
            import translation.french as new_language
            str_new_language = "fr"
        self.current_language, self.str_language = new_language, str_new_language

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
            self.player.move_left()
            self.current_direction = 'left'
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.player.move_right()
            self.current_direction = 'right'
        if pressed[pygame.K_UP] or pressed[pygame.K_z]:
            self.player.move_up()
            self.current_direction = 'up'
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.player.move_down()
            self.current_direction = 'down'
        return self.current_direction

    def update_screen(self):
        self.screen.display_messages()
        self.clock.tick(60)
        pygame.display.flip()

    def update(self):
        self.map_manager.update()

# permet de retrouver le chemin d'acces vers les assets lors de la compilation du jeu
    def get_path_assets(self, ressource):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, "assets") + "\\" + ressource

# permet de retrouver le chemin d'acces vers les saves lors de la compilation du jeu
    def get_path_saves(self, ressource):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, "saves") + "\\" + ressource

    def launch_fight(self):
        if self.active_fight and self.player.is_moving():
            self.fight = Fight(self)
            self.fight_player = Fight_Player(self)
            self.fight.run()
            self.active_fight = False

    def update_game(self):
        #sauvegarde la position du joueur
        self.player.save_location()
        #deplace le joueur
        self.handle_input()
        #met a jour l'emplacement du joueur
        self.update()
        #dessine le joueur et centre la cam
        self.map_manager.draw()
        #affiche le hud
        self.screen.hud()
        #detecte si un combat peut se lancer
        self.active_fight = self.map_manager.active_fight()

    def add_message(self, message):
        # Ajoute un message à la file d'attente
        self.messages_system.append((message, time.time()))

# vérifie si le joueur est en combat / actualise le jeu
    def update_zone(self):
        self.launch_fight()
        self.update_game()

    def run(self):
        self.clock = pygame.time.Clock()
        self.running = True

        self.player.change_image('up')
        pygame.display.flip()
        self.saves.load_all()

        while self.running:

            self.update_zone()

            # Mettre à jour l'animation du joueur en fonction de la touche pressée
            if self.player.is_moving():
                self.player.change_animation(self.handle_input())
            else:
                self.player.change_image(self.current_direction)

            self.update_screen()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.inventory.open_inventory(self, "game")

                if event.type == pygame.QUIT:
                    self.running = False

        self.saves.save_and_quit()