import pygame, time
import fight_entity
import player
from loading import Loading
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
        self.stop_update = True # désactive l'actualisation de l'écran a la premiere frame
        self.load_components()
        self.can_modifie_quest = True

    def load_components(self):
        self.load_settings()
        self.load_utils()
        self.load_screen()
        self.load_saves()
        self.load_system()

    def load_game(self, reset_game=False):
        paths_img_list = [r"enemy\enemyA.gif", r"mobilier.png", r"player.png"]
        self.loading = Loading(self, paths_img_list)
        self.loading.execut()
        self.loading.loading_screen.show_element('Loading player...')
        self.load_player()
        self.loading.loading_screen.show_element('Loading quest...')
        self.load_quests()
        self.loading.loading_screen.show_element('Loading screen...')
        self.screen.load_game()
        self.loading.loading_screen.show_element('Loading fight_settings...')
        self.load_fight()
        self.loading.loading_screen.show_element('Loading tutorials/dialogs...')
        self.load_tutorials_and_dialog()
        self.loading.loading_screen.show_element('Loading map...')
        self.load_map()
        self.loading.loading_screen.show_element('Loading saves...')
        self.saves.load_game()

        if reset_game:
            self.loading.loading_screen.show_element('Resetting the game...')
            self.saves.reset_game()

        self.loading.loading_screen.complete()

    def load_settings(self):
        self.language_manager = LanguageManager()
        self.time_auto_save = 120 # défini la save auto à 2mins
        self.format_time = "2minutes"
        self.last_auto_save = time.time()

    def load_saves(self):
        self.saves = Saves(self)

    def load_utils(self):
        self.utils = player.utils
        self.clock = pygame.time.Clock()

    def load_quests(self):
        self.can_modifie_quest = False
        self.quest = Quest(self)
        self.active_quests = []
        self.complete_quests = []

    def load_screen(self):
        self.screen = Screen(self)
        self.pause_menu = Pause_Menu(self)

    def load_player(self):
        self.inventory = Inventory(self)
        self.data_player = Data_Player(self)
        self.data_player.load_attributes() # charge les attrbutes du joueur
        self.player = player.Player()

    def load_fight(self):
        self.fight = Fight(self, None)
        self.fight_entity = fight_entity

    def load_map(self):
        self.map_manager = MapManager(self, self.screen.screen, self.player)

    def load_tutorials_and_dialog(self):
        self.dialog_box = DialogBox(self)
        self.tutorial = Tutorial(self)

    def load_system(self):
        self.object_name_inventory = [] # met l'inventaire vide (avant de le charger et de le remplir)
        self.active_fight = False   # n'active pas de combat
        self.messages_system = [] # met aucun message systeme
        self.current_direction = 'up' #défini la direction par defaut
        self.gravity = 1

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
        self.utils.delta_time = self.clock.tick(self.utils.fps_limite) /1000 # remplacer 60 par une var pour pouvoir modifier les fps dans les parametres
        if not self.stop_update:
            pygame.display.flip()
        else:
            self.stop_update = False

    def update(self):
        self.map_manager.update()

    def launch_fight(self, enemy_in_fight, enemy):
        if enemy_in_fight:
            enemy_class = getattr(self.fight_entity, enemy_in_fight)
            enemy_instance = enemy_class(self)  # Crée une instance de la classe ennemi
            print(enemy)
            self.map_manager.remove_enemy(enemy) #supprime l'enemie

            #si le joueur est encore en vie
            if enemy_instance.health >= 1:
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

    def updates(self):
        self.update_game()
        self.update_player_animation()
        self.update_screen()

    def running(self):
        self.run = True

        self.player.change_image('up')
        pygame.display.flip()

        while self.run:
            self.updates()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.inventory.open_inventory(self, "game")

                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.map_manager.check_npcs_collisions(self.dialog_box)

                    if event.key == pygame.K_ESCAPE:
                        self.dialog_box.close_dialog()

                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu.running()

                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()

                if event.type == pygame.QUIT:
                    self.run = False

        self.saves.save_and_quit()