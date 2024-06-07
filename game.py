import pygame, sys, os, time
import fight_entity
import player
from language_manager import LanguageManager
from inventory import *
from quest import Quest
from map import MapManager
from dialog import DialogBox
from screen import Screen
from data_player import Data_Player
from fight import Fight
from fight_player import Fight_Player
from tutorial import Tutorial
from saves import Saves
from pause_menu import Pause_Menu

class Game():

    def __init__(self, main_menu):
        self.main_menu = main_menu

        #ajout d'une clock au jeu
        self.clock = pygame.time.Clock()

        self.can_modifie_quest = False

        self.quest = Quest(self)
        self.active_quests = []
        self.complete_quests = []

        self.language_manager = LanguageManager()
        self.pause_menu = Pause_Menu(self)
        self.inventory = Inventory(self)
        self.saves = Saves(self)
        self.data_player = Data_Player(self)
        self.data_player.load_attributes() # charge les attrbutes du joueur
        self.player = player.Player()
        self.fight = Fight(self, None)
        self.screen = Screen(self)
        self.map_manager = MapManager(self, self.screen.screen, self.player)
        self.dialog_box = DialogBox(self)
        self.tutorial = Tutorial(self)
        self.fight_entity = fight_entity

        self.object_name_inventory = [] # met l'inventaire vide (avant de le charger et de le remplir)
        self.active_fight = False   # n'active pas de combat
        self.messages_system = [] # met aucun message systeme
        self.current_direction = 'up' #défini la direction par defaut
        self.gravity = 1

        self.time_auto_save = 120 # défini la save auto à 2mins
        self.format_time = "2minutes"
        self.last_auto_save = time.time()

        self.saves.load_all()

        self.can_modifie_quest = True

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

        self.player.reset_move()

        if not self.player.actualy_move_back:
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

        self.player.update_move()
        self.player.actualy_move_back = False

        return self.current_direction

    def update_screen(self):
        self.screen.display_messages()
        self.saves.blit_auto_save()
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
    def get_path_saves(self, ressource=any, folder_path=False):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        if not folder_path:
            return os.path.join(base_path, "saves") + "\\" + ressource
        else:
            return os.path.join(base_path, "saves")

    def launch_fight(self, enemy_in_fight, enemy):
        if enemy_in_fight:
            self.map_manager.remove_enemy(enemy)
            enemy_class = getattr(self.fight_entity, enemy_in_fight)
            enemy_instance = enemy_class(self)  # Crée une instance de la classe ennemi

            if enemy_instance.health != 0:
                self.active_fight = True
                self.fight = Fight(self, enemy_instance)
                self.fight_player = Fight_Player(self)
                self.fight.run()
                self.active_fight = False

    def update_game(self):
        #sauvegarde la position du joueur
        self.player.save_location()
        # sauvegarde auto le jeu
        self.saves.auto_saves()
        #deplace le joueur
        self.handle_input()
        #met a jour l'emplacement du joueur
        self.update()
        #dessine le joueur et centre la cam
        self.map_manager.draw()
        #affiche le hud
        self.screen.hud()
        #detecte si un combat peut se lancer
        for enemy in self.map_manager.get_map().enemys:
            if enemy.enemy_player_collide:
                self.launch_fight(enemy.in_fight(), enemy)

    def add_message(self, message, max_time=2):
        # Ajoute un message à la file d'attente
        self.messages_system.append((message, time.time(), max_time))

    def update_player_animation(self):
        if self.player.is_moving():
            self.player.change_animation(self.handle_input(), self.player.is_moving())
        else:
            self.player.change_image(self.current_direction)

    def running(self):
        self.run = True

        self.player.change_image('up')
        pygame.display.flip()

        while self.run:
            self.update_game()
            self.update_player_animation()
            self.update_screen()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.inventory.open_inventory(self, "game")

                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npcs_collisions(self.dialog_box)

                    if event.key == pygame.K_RETURN:
                        self.dialog_box.close_dialog()

                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu.running()

                if event.type == pygame.QUIT:
                    self.run = False

        self.saves.save_and_quit()