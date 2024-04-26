import pygame, random
from dataclasses import dataclass
from inventory import *

@dataclass
class Entity:
    name: str
    loot: list
    image: pygame.Surface
    max_health: int
    health: int
    attack: int
    give_xp: int

class Enemy(Entity):
    def turn(self, game):
        self.choose_attack(game)
        return True

    def choose_attack(self, game):
        if game.data_player.health > self.attack:
            game.data_player.health -= self.attack
        else: 
            game.data_player.health = 0

    def is_alive(self):
        return self.health != 0

    def loot_enemy(self):
        random_loot = random.choice(self.loot) # recupere un objet aléatoire
        obj = random_loot[0]
        max_quantity = random_loot[1]
        number_loot = random.randint(1, max_quantity)
        return obj, number_loot # return la classe (non initer) de l'objet puis le nombre d'objet

class EnemyA(Enemy):
    def __init__(self):
        image = pygame.image.load('assets\enemy\enemyA.gif')
        image = pygame.transform.scale(image, (250, 250))
        loot = [(Life_Potion, 3), (Big_Life_Potion, 2)] # (L'objet, le nombre d'objet au max)

        super().__init__("enemy A", loot, image, max_health=50, health=50, attack=12, give_xp=2) # de base 100, 100, 10, 2

class EnemyB(Enemy):
    def __init__(self):
        image = pygame.image.load('assets\enemy\enemyB.webp')
        image = pygame.transform.scale(image, (250, 250))
        loot = [(Life_Potion, 6), (Big_Life_Potion, 3)] # (L'objet, le nombre d'objet au max)

        super().__init__("enemy B", loot, image, max_health=80, health=80, attack=15, give_xp=3) # de base 120, 120, 12, 5