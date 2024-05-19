import pygame, random
from dataclasses import dataclass
from inventory import *

@dataclass
class Entity:
    name: str
    lanch_fight_message: str # Le message qui s'affiche quand on join un combat
    loot: list
    image: pygame.Surface
    max_health: int
    health: int
    attack: int
    crit_luck: int
    crit_domage: float
    give_xp: int

class Enemy(Entity):
    def turn(self, game):
        self.game = game
        self.choose_action()
        return True

    def choose_action(self):
        self.action_attack()

    def calculate_crit_dommage(self):
        domage = self.player.attack*self.player.crit_domage

        # vérifie si le crit a bien augmenter l'attack 
        if domage == self.player.attack:
            domage += 1

        return domage

    def enemy_crit(self):
        crit_luck = random.randint(0, 100)

        domage = self.attack

        if crit_luck <= self.crit_luck:
            domage =  self.calculate_crit_dommage()
            txt1 = self.game.load_txt('message_system', 'damage_crit_suffered1')
            txt_dommage = domage
            txt2 = self.game.load_txt('message_system', 'damage_crit_suffered2')
            message = f"{txt1} {txt_dommage} {txt2}"
        else:
            txt1 = self.game.load_txt('message_system', 'damage_suffered1')
            txt_dommage = domage
            txt2 = self.game.load_txt('message_system', 'damage_suffered2')
            message = f"{txt1} {txt_dommage} {txt2}"

        return domage, message

    def action_attack(self):
        domage, message = self.enemy_crit()

        if self.game.data_player.health > domage:
            self.game.data_player.health -= domage
        else: 
            self.game.data_player.health = 0

        self.game.add_message(message)

    def is_alive(self):
        return self.health != 0

    def loot_enemy(self):
        random_loot = random.choice(self.loot) # recupere un objet aléatoire
        obj = random_loot[0]
        max_quantity = random_loot[1]
        number_loot = random.randint(1, max_quantity)
        return obj, number_loot # return la classe (non initer) de l'objet puis le nombre d'objet

class EnemyA(Enemy):
    def __init__(self, game):
        page = 'enemyA'
        key_txt = 'name'
        name = game.load_txt(page, key_txt)

        page = 'enemyA'
        key_txt = 'lanch_fight_message'
        lanch_fight_message = game.load_txt(page, key_txt)

        path = game.get_path_assets('enemy\enemyA.gif')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (250, 250))

        loot = [(Life_Potion, 3), (Big_Life_Potion, 2)] # (L'objet, le nombre d'objet au max)

        super().__init__(name, lanch_fight_message, loot, image, max_health=50, health=50, attack=12, crit_luck=6, crit_domage=1.12, give_xp=4) # de base 100, 100, 10, 2

class EnemyB(Enemy):
    def __init__(self, game):
        page = 'enemyB'
        key_txt = 'name'
        name = game.load_txt(page, key_txt)

        page = 'enemyB'
        key_txt = 'lanch_fight_message'
        lanch_fight_message = game.load_txt(page, key_txt)

        path = game.get_path_assets('enemy\enemyB.webp')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (250, 250))
        loot = [(Big_Life_Potion, 3), (Bomb, 1)] # (L'objet, le nombre d'objet au max)

        super().__init__(name, lanch_fight_message, loot, image, max_health=60, health=60, attack=12, crit_luck=10, crit_domage=1.15, give_xp=6) # de base 120, 120, 12, 5