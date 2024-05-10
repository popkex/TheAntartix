import pygame, sys, os, time
from inventory import *
from quest import Quest
from map import MapManager
from dialog import DialogBox
from screen import Screen
from data_player import Data_Player
from player import Player
from fight import Fight
from fight_player import Fight_Player
from tutorial import Tutorial
from saves import Saves
from pause_menu import Pause_Menu

class Game():

    def __init__(self):
        self.defaut_language = "fr"
        self.load_language(self.defaut_language)

        self.can_modifie_quest = False

        self.quest = Quest(self)
        self.active_quests = []

        self.pause_menu = Pause_Menu(self)
        self.inventory = Inventory(self)
        self.saves = Saves(self)
        self.data_player = Data_Player(self)
        self.data_player.load_attributes() # charge les attrbutes du joueur
        self.player = Player()
        self.screen = Screen(self)
        self.map_manager = MapManager(self, self.screen.screen, self.player)
        self.dialog_box = DialogBox(self)
        self.tutorial = Tutorial(self)

        self.object_name_inventory = [] # met l'inventaire vide (avant de le charger et de le remplir)
        self.active_fight = False   # n'active pas de combat
        self.messages_system = [] # met aucun message systeme
        self.current_direction = 'up' #défini la direction par defaut
        #
        #
        # faire le chargement des quests
        #
        #

        self.saves.load_all()

        self.can_modifie_quest = True


    def load_txt(self, page, txt):
        return self.current_language.translations[page][txt]

    def load_language(self, lang):
        if lang == 'en':
            import translation.english as new_language
            str_new_language = "en"
        elif lang == 'fr':
            import translation.french as new_language
            str_new_language = "fr"
        elif lang == 'es':
            import translation.spanish as new_language
            str_new_language = "es"

        self.current_language, self.str_language = new_language, str_new_language

    def check_quest_completion(self):
        # Vérifier si une quête est terminée
        for quest in self.active_quests:
            if quest.is_completed():
                # Récompenser le joueur
                self.player.receive_rewards(quest.rewards)
                # Marquer la quête comme terminée
                quest.complete()

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
        self.dialog_box.render(self.screen.screen)
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

    def add_message(self, message, max_time=2):
        # Ajoute un message à la file d'attente
        self.messages_system.append((message, time.time(), max_time))

    def run(self):
        self.clock = pygame.time.Clock()
        self.running = True

        self.player.change_image('up')
        pygame.display.flip()

        while self.running:

            self.launch_fight()
            self.update_game()

            # Mettre à jour l'animation du joueur en fonction de la touche pressée
            if self.player.is_moving():
                self.player.change_animation(self.handle_input(), self.player.is_moving())
            else:
                self.player.change_image(self.current_direction)

            self.update_screen()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.inventory.open_inventory(self, "game")

                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npcs_collisions(self.dialog_box)


                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu.running()

                if event.type == pygame.QUIT:
                    self.running = False

        self.saves.save_and_quit()