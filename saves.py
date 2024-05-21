import pygame, pickle
from inventory import *

class Saves:

    def __init__(self, game):
        self.game = game

    def class_in_str(self, class_name):
        class_dict = {
            'Life_Potion': Life_Potion,
            'Big_Life_Potion': Big_Life_Potion,
            'Bomb': Bomb,
        }
        return class_dict.get(class_name)

    def save_and_quit(self):
        self.save_all()
        pygame.quit()

    def save_and_main_menu(self):
        self.save_all()
        self.game.main_menu.running()

    def save_all(self):
        self.save_attribut_player()
        self.save_position()
        self.save_inventory()
        self.save_tutorial()
        self.save_settings()
        self.save_quests()

    def load_all(self):
        self.load_settings()
        self.load_position()
        self.load_inventory()
        self.load_tutorial()
        self.load_quests()

                                            # les saves

    def save_attribut_player(self, data_provided=None):
        path = self.game.get_path_saves('player_attribut.bin')

        health = self.game.data_player.health
        max_health = self.game.data_player.max_health
        attack = self.game.data_player.attack
        crit_luck = self.game.data_player.crit_luck
        crit_domage = self.game.data_player.crit_domage
        knock_out_luck = self.game.data_player.knock_out_luck
        xp = self.game.data_player.xp
        xp_max = self.game.data_player.xp_max
        lvl = self.game.data_player.lvl

        if not data_provided:
            data = (health, max_health, attack, crit_luck, crit_domage, knock_out_luck, xp, xp_max, lvl)
        else:
            data = data_provided

        with open(path, 'wb') as content:
            pickle.dump(data, content, pickle.HIGHEST_PROTOCOL)

    def save_position(self):
        path = self.game.get_path_saves('player_position.bin')
        coordonates = self.game.player.get_coordonnes()
        map = self.game.map_manager.current_map
        data = (coordonates, map)

        with open(path, 'wb') as content:
            pickle.dump(data, content, pickle.HIGHEST_PROTOCOL)

    def save_inventory(self):
        path = self.game.get_path_saves('inventory.bin')

        # Sauvegarder les noms des classes des objets
        self.game.object_name_inventory = [(type(objet[0]).__name__, objet[1]) for objet in self.game.inventory.objet_inventory]
        objects = self.game.object_name_inventory

        with open(path, 'wb') as content:
            pickle.dump(objects, content, pickle.HIGHEST_PROTOCOL)

    def save_tutorial(self):
        path = self.game.get_path_saves('tutorials.bin')
        data = self.game.tutorial.dic_tutorial

        with open(path, 'wb') as content:
            pickle.dump(data, content, pickle.HIGHEST_PROTOCOL)

    def save_settings(self):
        path = self.game.get_path_saves('settings.bin')
        data = self.game.str_language

        with open(path, 'wb') as content:
            pickle.dump(data, content, pickle.HIGHEST_PROTOCOL)

    def save_quests(self):
        path = self.game.get_path_saves('quest.bin')
        data = self.game.quest.all_quests_data()

        with open(path, 'wb') as content:
            pickle.dump(data, content, pickle.HIGHEST_PROTOCOL)

                                            # les loads
    def load_attribut_player(self):
        path = self.game.get_path_saves('player_attribut.bin')
        try:
            with open(path, 'rb') as content:
                health, max_health, attack, crit_luck, crit_domage, knock_out_luck, xp, xp_max, lvl = pickle.load(content)
        except:
            max_health = 100
            health = max_health
            attack = 10
            crit_luck = 5
            crit_domage = 1.12
            knock_out_luck = 5
            xp = 0
            xp_max = 25
            lvl = 1

            data = max_health, health, attack, crit_luck, crit_domage, knock_out_luck, xp, xp_max, lvl

            self.save_attribut_player(data)

        return health, max_health, attack, crit_luck, crit_domage, knock_out_luck, xp, xp_max ,lvl

    def load_position(self):
        path = self.game.get_path_saves('player_position.bin')

        try:
            with open(path, 'rb') as content:
                (x, y), map  = pickle.load(content)
                self.game.map_manager.current_map = map
                self.game.map_manager.teleport_player_with_position(x, y)
        except:
            pass

    def load_inventory(self):
        path = self.game.get_path_saves('inventory.bin')
        objects = []

        try:
            with open(path, 'rb') as content:
                for objet in pickle.load(content):
                    objects.append((objet[0], objet[1]))
                for objet, number in objects:
                    new_instance = self.class_in_str(objet)
                    self.game.inventory.append_object(new_instance(self.game), number)
        except Exception as e:
            self.save_inventory()

    def load_tutorial(self):
        path = self.game.get_path_saves('tutorials.bin')

        try:
            with open(path, 'rb') as content:
                self.game.tutorial.dic_tutorial = pickle.load(content)
        except:
            self.game.tutorial.dic_tutorial = {
                'inventory': False,
                'fight': False,
            }
            self.save_tutorial()

    def load_settings(self):
        path = self.game.get_path_saves('settings.bin')

        try:
            with open(path, 'rb') as content:
                data_str = pickle.load(content)
                self.game.load_language(data_str)
        except:
            self.game.load_language("en")
            self.save_settings()

    def load_quests(self):
        try:
            self.game.can_modifie_quest = True
            type_quests_progress = []
            path = self.game.get_path_saves('quest.bin')

            with open(path, 'rb') as content:
                data = pickle.load(content)
                for quest_data in data:
                    name, quest_type, objectif, rewards, rewards_quantity, key_description, progression = quest_data
                    self.game.quest.add_quest(name, quest_type, objectif, rewards, rewards_quantity, key_description)

                    # vérifie si le type de quete a deja ete traiter
                    if not quest_type in type_quests_progress:
                        self.game.quest.progress(quest_type, progression)
                    else:
                        type_quests_progress.append(quest_type)

            self.game.can_modifie_quest = False

        except:
            self.save_quests()