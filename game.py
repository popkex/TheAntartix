import pygame, sys, os, pickle, time
import inventory
from inventory import *
from map import MapManager
from screen import Screen
from data_player import Data_Player
from player import Player
from fight import Fight
from fight_player import Fight_Player

class Game():

    def __init__(self):
        self.data_player = Data_Player(self)
        self.player = Player(0, 0)
        self.screen = Screen(self)
        self.map_manager = MapManager(self, self.screen.screen, self.player)
        self.inventory = inventory.Inventory(self)
        self.object_name_inventory = []
        self.active_fight = False
        self.messages_system = []
        self.current_direction = 'up' #défini la direction par defaut

    def class_in_str(self, module, name):
        return getattr(module, name)

                                                    # partie sauvegarde et chargement du jeu
    def save_and_quit(self):
        self.save_all()
        pygame.quit()

    def save_all(self):
        self.save_attribut_player()
        self.save_position()
        self.save_inventory()

    def load_all(self):
        self.load_position()
        self.load_inventory()

    def save_attribut_player(self):
        path = self.get_path_saves('player_attribut.bin')
        health = self.data_player.health
        max_health = self.data_player.max_health
        attack = self.data_player.attack
        xp = self.data_player.xp
        xp_max = self.data_player.xp_max
        lvl = self.data_player.lvl
        data = (health, max_health, attack, xp, xp_max, lvl)

        with open(path, 'wb') as fichier:
            pickle.dump(data, fichier, pickle.HIGHEST_PROTOCOL)

    def load_attribut_player(self):
        path = self.get_path_saves('player_attribut.bin')
        try:
            with open(path, 'rb') as fichier:
                health, max_health, attack, xp, xp_max, lvl = pickle.load(fichier)
        except:
            max_health = 100
            health = 100
            attack = 10
            xp = 0
            xp_max = 25
            lvl = 1

        return health, max_health, attack, xp, xp_max ,lvl

    def save_position(self):
        path = self.get_path_saves('player_position.bin')
        coordonates = self.player.get_coordonnes()
        map = self.map_manager.current_map
        data = (coordonates, map)

        with open(path, 'wb') as fichier:
            pickle.dump(data, fichier, pickle.HIGHEST_PROTOCOL)

    def load_position(self):
        path = self.get_path_saves('player_position.bin')

        try:
            with open(path, 'rb') as fichier:
                (x, y), map  = pickle.load(fichier)
                self.map_manager.current_map = map
                self.map_manager.teleport_player_with_position(x, y)
        except:
            pass

    def save_inventory(self):
        path = self.get_path_saves('inventory.bin')

        for objet in self.inventory.objet_inventory:
            self.object_name_inventory.append((objet[0].name, objet[1]))
        objects = self.object_name_inventory

        with open(path, 'wb') as fichier:
            pickle.dump(objects, fichier, pickle.HIGHEST_PROTOCOL)

    def load_inventory(self):
        path = self.get_path_saves('inventory.bin')

        try:
            objects, new_instance = [], []
            with open(path, 'rb') as fichier:
                for objet in pickle.load(fichier):
                    objects.append((objet[0], objet[1]))

                for objet, number in objects:
                    new_instance = self.class_in_str(inventory, objet)
                    self.inventory.append_object(new_instance(self), number)
        except:
            self.save_inventory()

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
        pygame.display.flip()
        self.clock.tick(60)

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
        self.load_all()

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

        self.save_and_quit()