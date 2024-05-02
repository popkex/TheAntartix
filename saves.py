import pygame, pickle

class Saves:

    def __init__(self, game):
        self.game = game

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
        path = self.game.get_path_saves('player_attribut.bin')
        health = self.game.data_player.health
        max_health = self.game.data_player.max_health
        attack = self.game.data_player.attack
        xp = self.game.data_player.xp
        xp_max = self.game.data_player.xp_max
        lvl = self.game.data_player.lvl
        data = (health, max_health, attack, xp, xp_max, lvl)

        with open(path, 'wb') as fichier:
            pickle.dump(data, fichier, pickle.HIGHEST_PROTOCOL)

    def load_attribut_player(self):
        path = self.game.get_path_saves('player_attribut.bin')
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
        path = self.game.get_path_saves('player_position.bin')
        coordonates = self.game.player.get_coordonnes()
        map = self.game.map_manager.current_map
        data = (coordonates, map)

        with open(path, 'wb') as fichier:
            pickle.dump(data, fichier, pickle.HIGHEST_PROTOCOL)

    def load_position(self):
        path = self.game.get_path_saves('player_position.bin')

        try:
            with open(path, 'rb') as fichier:
                (x, y), map  = pickle.load(fichier)
                self.game.map_manager.current_map = map
                self.game.map_manager.teleport_player_with_position(x, y)
        except:
            pass

    def save_inventory(self):
        path = self.game.get_path_saves('inventory.bin')

        for objet in self.game.inventory.objet_inventory:
            self.game.object_name_inventory.append((objet[0].name, objet[1]))
        objects = self.game.object_name_inventory

        with open(path, 'wb') as fichier:
            pickle.dump(objects, fichier, pickle.HIGHEST_PROTOCOL)

    def load_inventory(self):
        path = self.game.get_path_saves('inventory.bin')

        try:
            objects, new_instance = [], []
            with open(path, 'rb') as fichier:
                for objet in pickle.load(fichier):
                    objects.append((objet[0], objet[1]))

                for objet, number in objects:
                    new_instance = self.class_in_str(self.game.inventory, objet)
                    self.game.inventory.append_object(new_instance(self.game), number)
        except:
            self.save_inventory()