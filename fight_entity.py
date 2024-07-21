import pygame, random
from dataclasses import dataclass
from inventory import *

@dataclass
class Entity:
    key_name: str
    name: str
    lanch_fight_message: str # Le message qui s'affiche quand on join un combat
    loot: list
    image: pygame.Surface
    max_health: int
    health: int
    old_attack: int
    attack: int
    crit_luck: int
    crit_domage: float
    knock_out_luck: int
    luck_fail_attack: int
    give_xp: int

class Enemy(Entity):
    def turn(self, game):
        self.game = game
        self.language_manager = game.language_manager
        self.choose_action()
        return True

    def choose_action(self):
        self.action_attack()

    def calculate_crit_dommage(self):
        domage = self.attack*self.crit_domage

        # vérifie si le crit a bien augmenter l'attack 
        if domage == self.attack:
            domage += 1

        return domage

    def enemy_crit(self):
        crit_luck = random.randint(0, 100)

        domage = self.attack

        if crit_luck <= self.crit_luck:
            domage =  self.calculate_crit_dommage()
            txt1 = self.language_manager.load_txt('message_system', 'damage_crit_suffered1')
            txt_dommage = domage
            txt2 = self.language_manager.load_txt('message_system', 'damage_crit_suffered2')
            message = f"{txt1} {int(txt_dommage)} {txt2}"
        else:
            txt1 = self.language_manager.load_txt('message_system', 'damage_suffered1')
            txt_dommage = domage
            txt2 = self.language_manager.load_txt('message_system', 'damage_suffered2')
            message = f"{txt1} {txt_dommage} {txt2}"

        return domage, message

    def fail_attack(self):
        luck_fail = random.randint(0, 100)

        # si le joueur ne loupe pas ca défense
        if self.luck_fail_attack < luck_fail:
            return False
        # si le joueur loupe ca défense
        return True

    def action_attack(self):
        if not self.fail_attack(): 
            domage, message = self.enemy_crit()

            if self.game.data_player.health > domage:
                self.game.data_player.health -= domage
            else: 
                self.game.data_player.health = 0
        else:
            message = self.language_manager.load_txt('message_system', 'enemy_fail_attack')

        self.game.add_message(message)
        self.game.update_screen()

        # reset la stat de l'attack au cas ou le joueur a modifier cela 
        self.attack = self.old_attack

    def is_alive(self):
        return self.health != 0

    def loot_enemy(self):
        return self.loot

class EnemyA(Enemy):
    def __init__(self, game):
        utils = game.utils
        self.language_manager = game.language_manager

        max_health = 50
        health = 50
        old_attack = 10
        attack = old_attack
        crit_luck = 6
        crit_domage = 1.12
        knock_out_luck = 5
        luck_fail_attack = 15
        give_xp = 4

        key_name = "enemyA"
        key_txt = 'name'
        name = self.language_manager.load_txt(key_name, key_txt)

        key_txt = 'lanch_fight_message'
        lanch_fight_message = self.language_manager.load_txt(key_name, key_txt)

        path = utils.get_path_assets(r'enemy\enemyA.gif')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (250, 250))

        loot = [(Life_Potion, 3), (Big_Life_Potion, 2)] # (L'objet, le nombre d'objet au max)

        super().__init__(key_name, name, lanch_fight_message, loot, image, max_health, health, old_attack, attack, crit_luck, crit_domage, knock_out_luck, luck_fail_attack, give_xp)

class EnemyB(Enemy):
    def __init__(self, game):
        utils = game.utils
        self.language_manager = game.language_manager

        old_domage = None
        max_health = 60
        health = 60
        old_attack = 15
        attack = old_attack
        crit_luck = 10
        crit_domage = 1.15
        knock_out_luck = 10
        luck_fail_attack = 10
        give_xp = 6

        key_name = "enemyB"
        key_txt = 'name'
        name = self.language_manager.load_txt(key_name, key_txt)

        key_txt = 'lanch_fight_message'
        lanch_fight_message = self.language_manager.load_txt(key_name, key_txt)

        path = utils.get_path_assets(r'enemy\enemyB.webp')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (250, 250))
        loot = [(Big_Life_Potion, 3), (Bomb, 1)] # (L'objet, le nombre d'objet au max)

        super().__init__(key_name, name, lanch_fight_message, loot, image, max_health, health, old_attack, attack, crit_luck, crit_domage, knock_out_luck, luck_fail_attack, give_xp) # de base 120, 120, 12, 5