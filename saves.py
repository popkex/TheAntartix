import pygame, pickle, os, time
from inventory import *

class Saves:

    def __init__(self, game):
        self.game = game
        self.utils = game.utils
        self.language_manager = self.game.language_manager
        self.can_blit_image = False
        self.time_blit_save_auto = 5

    def class_in_str(self, class_name):
        class_dict = {
            'Life_Potion': Life_Potion,
            'Big_Life_Potion': Big_Life_Potion,
            'Bomb': Bomb,
        }
        return class_dict.get(class_name)

    def auto_saves(self):
        # vérifie si la save auto a été désactivé
        if self.game.time_auto_save:
            # Obtient l'heure actuelle
            now = time.time()

            # vérifie si la save auto peu se lancé
            if now - self.game.last_auto_save > self.game.time_auto_save:
                self.save_all()
                self.game.last_auto_save = now
                self.can_blit_image = True

            # désactive la save auto apres Xtemps
            if now - self.game.last_auto_save > self.time_blit_save_auto:
                self.can_blit_image = False

    def blit_auto_save(self):
        if self.can_blit_image:
            self.game.screen.auto_save_message()

    def save_and_quit(self):
        self.save_all()
        pygame.quit()

    def save_all(self):
        self.save_attribut_player()
        self.save_position()
        self.save_inventory()
        self.save_tutorial()
        self.save_settings()
        self.save_quests()
        self.save_tiles()
        self.save_npcs_enemys_position()

    def load_game(self):
        self.load_position()
        self.load_inventory()
        self.load_tutorial()
        self.load_quests()

    def reset_all(self):
        self.reset_attribut_player()
        self.reset_position()
        self.reset_inventory()
        self.reset_tutorial()
        self.reset_settings()
        self.reset_quests()
        self.reset_map()

    # identique a la reset_all mais ne reset pas les parametres
    def reset_game(self):
        self.reset_attribut_player()
        self.reset_position()
        self.reset_inventory()
        self.reset_tutorial()
        self.reset_quests()
        self.reset_map()

    def create_folder_saves(self):
        if not os.path.exists(r'saves'):
            if not os.path.exists(r'_internal'):
                os.makedirs(r'saves')
            elif not os.path.exists(r'_internal\saves'):
                os.makedirs(r'_internal\saves')

                                            # les saves

    def save_attribut_player(self, data_provided=None):
        path = self.utils.get_path_saves('player_attribut.bin')

        if not data_provided:
            data_player = self.game.data_player

            health = data_player.health
            max_health = data_player.max_health
            attack = data_player.attack
            defense = data_player.defense
            energy = data_player.energy
            energy_max = data_player.energy_max
            energy_consumed_attack = data_player.energy_consumed_attack
            energy_regain_defense = data_player.energy_regain_defense
            crit_luck = data_player.crit_luck
            crit_domage = data_player.crit_domage
            knock_out_luck = data_player.knock_out_luck
            luck_fail_attack = data_player.luck_fail_attack
            luck_fail_defense = data_player.luck_fail_defense
            xp = data_player.xp
            xp_max = data_player.xp_max
            lvl = data_player.lvl

            data = (health, max_health, attack, defense, energy, energy_max, energy_consumed_attack, energy_regain_defense, crit_luck, crit_domage, knock_out_luck, luck_fail_attack, luck_fail_defense, xp, xp_max, lvl)
        else:
            data = data_provided

        with open(path, 'wb') as content:
            pickle.dump(data, content, pickle.HIGHEST_PROTOCOL)

    def save_position(self):
        path = self.utils.get_path_saves('player_position.bin')
        coordonates = self.game.player.get_coordonnes()
        map = self.game.map_manager.current_map
        data = (coordonates, map)

        with open(path, 'wb') as content:
            pickle.dump(data, content, pickle.HIGHEST_PROTOCOL)

    def save_inventory(self):
        path = self.utils.get_path_saves('inventory.bin')

        # Sauvegarder les noms des classes des objets
        self.game.object_name_inventory = [(type(objet[0]).__name__, objet[1]) for objet in self.game.inventory.objet_inventory]
        objects = self.game.object_name_inventory

        with open(path, 'wb') as content:
            pickle.dump(objects, content, pickle.HIGHEST_PROTOCOL)

    def save_tutorial(self):
        path = self.utils.get_path_saves('tutorials.bin')
        data = self.game.tutorial.dic_tutorial

        with open(path, 'wb') as content:
            pickle.dump(data, content, pickle.HIGHEST_PROTOCOL)

    def save_settings(self):
        path = self.utils.get_path_saves('settings.bin')

        # save la langue
        data_language = self.language_manager.str_language

        # save le temps de l'auto_save
        data_auto_save_time = self.game.time_auto_save, self.game.format_time
        data = data_language, data_auto_save_time

        with open(path, 'wb') as content:
            pickle.dump(data, content, pickle.HIGHEST_PROTOCOL)

    def save_quests(self):
        path = self.utils.get_path_saves('quest.bin')
        data = self.game.quest.all_quests_data(), self.game.complete_quests

        with open(path, 'wb') as content:
            pickle.dump(data, content, pickle.HIGHEST_PROTOCOL)

    def save_tiles(self):
        path = self.utils.get_path_saves('modified_map.bin')
        # si la self.game.map_manager.tile_modified a bien été initier
        try:
            data = self.game.map_manager.tile_modified

            with open(path, 'wb') as content:
                pickle.dump(data, content, pickle.HIGHEST_PROTOCOL)
        except:
            self.reset_map(reset_entity=False)

    def save_npcs_enemys_position(self):
        path = self.utils.get_path_saves('npcs_enemys_position.bin')
        map_manager = self.game.map_manager
        npcs_data = []
        enemys_data = []
        data = []

        for map in map_manager.maps:
            map = map_manager.get_map(map)
            for npc in map.npcs:
                npcs_data.append((npc.name, npc.position, npc.current_point))

            for enemy in map.enemys:
                enemys_data.append((enemy.number_enemy, enemy.position))

        data.append(npcs_data)
        data.append(enemys_data)

        with open(path, 'wb') as content:
            pickle.dump(data, content, pickle.HIGHEST_PROTOCOL)

    def load_npcs_enemys_position(self):
        path = self.utils.get_path_saves('npcs_enemys_position.bin')
        try:
            with open(path, 'rb') as content:
                data = pickle.load(content)
            return data
        except:
            return []

                                            # les loads
    def load_attribut_player(self):
        path = self.utils.get_path_saves('player_attribut.bin')
        try:
            with open(path, 'rb') as content:
                data = pickle.load(content)
        except:
            data = self.reset_attribut_player()

        health, max_health, attack, defense, energy, energy_max, energy_consumed_attack, energy_regain_defense, crit_luck, crit_domage, knock_out_luck, luck_fail_attack, luck_fail_defense, xp, xp_max, lvl = data
        data_1 = health, max_health, attack, defense, energy, energy_max, energy_consumed_attack, energy_regain_defense
        data_2 = crit_luck, crit_domage, knock_out_luck, luck_fail_attack, luck_fail_defense
        data_3 = xp, xp_max, lvl

        return data_1, data_2, data_3

    def load_position(self):
        path = self.utils.get_path_saves('player_position.bin')

        try:
            with open(path, 'rb') as content:
                (x, y), map  = pickle.load(content)
                self.game.map_manager.current_map = map
                self.game.map_manager.teleport_player_with_position(x, y)
        except:
            pass

    def load_inventory(self):
        path = self.utils.get_path_saves('inventory.bin')
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
        path = self.utils.get_path_saves('tutorials.bin')

        try:
            with open(path, 'rb') as content:
                self.game.tutorial.dic_tutorial = pickle.load(content)
        except:
            self.reset_tutorial()

    def load_settings(self):
        path = self.utils.get_path_saves('settings.bin')

        try:
            with open(path, 'rb') as content:
                data = pickle.load(content)

                data_language_str = data[0]
                self.language_manager.load_language(data_language_str)

                data_auto_save_time = data[1]
                self.game.time_auto_save = data_auto_save_time[0]
                self.game.format_time = data_auto_save_time[1]
        except:
            self.reset_settings()

    def load_quests(self):
        try:
            self.game.can_modifie_quest = True
            type_quests_progress = []
            path = self.utils.get_path_saves('quest.bin')

            with open(path, 'rb') as content:
                data = pickle.load(content)

                # Charge la liste des quests en cours
                for quest_data in data[0]:
                    name, quest_type, objectif, rewards, rewards_quantity, key_description, progression = quest_data
                    self.game.quest.add_quest(name, quest_type, objectif, rewards, rewards_quantity, key_description)

                    # vérifie si le type de quete a deja ete traiter
                    if not quest_type in type_quests_progress:
                        self.game.quest.progress(quest_type, progression)
                    else:
                        type_quests_progress.append(quest_type)

                for quest_data in data[1]:
                    self.game.complete_quests.append(quest_data)

                # dit au npc de changer de dialog
                for npc in self.game.map_manager.get_map().npcs:
                    if npc.quest[0] in self.game.complete_quests:
                        npc.quest_state = True
                        break

            self.game.can_modifie_quest = False

        except:
            self.save_quests()

    def load_modified_map(self):
        try:
            path = self.utils.get_path_saves('modified_map.bin')
            with open(path, 'rb') as content:
                data = pickle.load(content)
                return data
        except:
            return {}

    def reset_attribut_player(self):
        max_health = 100
        health = max_health
        attack = 10
        defense = 15 # 15% de l'attack bloquer
        energy = 40
        energy_max = 20
        energy_consumed_attack = 15
        energy_regain_defense = 10
        crit_luck = 5
        crit_domage = 1.12
        knock_out_luck = 5
        luck_fail_attack = 15
        luck_fail_defense = 25 # 25% de chance de fail la defense
        xp = 0
        xp_max = 25
        lvl = 1

        data = max_health, health, attack, defense, energy, energy_max, energy_consumed_attack, energy_regain_defense, crit_luck, crit_domage, knock_out_luck, luck_fail_attack, luck_fail_defense, xp, xp_max, lvl
        self.save_attribut_player(data)
        return data

    def reset_position(self):
        self.game.map_manager.current_map = "artixs_temple_first"
        self.game.map_manager.teleport_player_with_name('player_spawn')
        self.save_position()

    def reset_inventory(self):
        self.game.inventory.reset_inventory()
        self.save_inventory()

    def reset_tutorial(self):
        self.game.tutorial.dic_tutorial = {
            'inventory': False,
            'fight': False,
        }
        self.save_tutorial()

    def reset_settings(self):
        self.language_manager.load_language("en")
        self.game.time_auto_save = 120
        self.game.format_time = "2 minutes"
        self.save_settings()

    def reset_quests(self):
        self.game.quest.reset_all_quests()
        self.game.complete_quests = []
        self.save_quests()

    def reset_map(self, reset_map=True, reset_entity=True):
        from map import MapManager
        self.game.map_manager = MapManager(self.game, self.game.screen.screen, self.game.player, reset_tile=reset_map, reset_entity=reset_entity)