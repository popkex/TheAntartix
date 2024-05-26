import pygame, pytmx, pyscroll
from player import *
from inventory import *
from dataclasses import dataclass

@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str

@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    portals: list[Portal]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    npcs: list[NPC]
    enemys: list[Enemy]

class MapManager:

    def __init__(self, game, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.game = game
        self.current_map = "world"
        
        self.paul_quest = ('paul_quest', 'kill_enemy', 20, self.game.inventory.potion.life_potion, 10, 'descr')
        self.michel_quest = ('michel_quest', 'Life_Potion', 10, self.game.inventory.weapon.bomb, 10, 'descr')

        #permet le lancement des combats
        self.battle_running = False

#défini les maps
#dans le monde normal
        #défini : le monde d'origine (le monde normal), le point d'entrée, le monde d'entrée, le lieu de spawn dans le monde d'entrée
        self.register_map("world", portals=[
            Portal(from_world="world", origin_point="enter_house1", target_world="house1", teleport_point="player_spawn"),
            Portal(from_world="world", origin_point="enter_house2", target_world="house2", teleport_point="player_spawn"),
            Portal(from_world="world", origin_point="enter_donjon1", target_world="donjon1", teleport_point="player_spawn"),
        ], npcs=[
            NPC('paul', nb_points=2, key_txt=('npc', 'paul'), quest=self.paul_quest), # donne la liste pour pouvoir traduire apres*
            NPC('michel', nb_points=2, key_txt=('npc', 'michel'), quest=self.michel_quest),
            NPC('fleufleu', nb_points=7, key_txt=('npc', 'fleufleu'), quest=None)
        ], enemys=[
            # aucun ennemies
        ],
        )

#depuis les maisons
        #defini le monde d'origine (la maison), le point de sortie, le monde de sortie, l'endroit du spawn dans le monde de sortie
        self.register_map("house1", portals=[
            Portal(from_world="house1", origin_point="exit_house", target_world="world", teleport_point="exit_house1")
        ], npcs=[
            # aucun npcs
        ], enemys=[
            # aucun ennemies
        ])
        self.register_map("house2", portals=[
            Portal(from_world="house2", origin_point="exit_house", target_world="world", teleport_point="exit_house2")
        ], npcs=[
            # aucun npcs
        ], enemys=[
            # aucun ennemies
        ])
        self.register_map("donjon1", portals=[ 
            Portal(from_world="donjon1", origin_point="exit_donjon", target_world="world", teleport_point="exit_donjon1"),
        ], npcs=[
            # aucun npcs
        ], enemys=[
                # zone 0
                *[EnemyA(self.game) for _ in range(4)],
                *[EnemyB(self.game) for _ in range(2)],

                # zone 1
                *[EnemyA(self.game) for _ in range(3)],
                *[EnemyB(self.game) for _ in range(3)],

                # zone 2

                # zone 3

                # zone 4

                # zone 5

                # zone 6, boss

                # zone 7

                # zone 8

                # zone 9
        ])

        #défini le lieu de spawn qui s'appelle 'player_spawn'
        self.teleport_player_with_name('player_spawn')

        self.teleport_npcs()
        self.teleport_enemy()

    def check_player_far_npc(self):
        # Vérifie pour chaque npc si il est en contacte avec lui
        for npc in self.get_map().npcs:
            if self.game.player.rect.colliderect(npc.rect):
                return False

        return True

    def check_npcs_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            for npc in self.get_map().npcs:
                if npc.rect.colliderect(self.game.player.rect):
                    key_txt_name = (npc.name, "name")
                    reading = dialog_box.execute(npc.key_txt, key_txt_name, npc.quest)

                    if npc.quest and not reading:
                        name_quest, type_quest, objectif_quest, rewards, rewards_quantity, key_description = npc.quest
                        self.game.quest.add_quest(name_quest, type_quest, objectif_quest, rewards, rewards_quantity, key_description)

    def check_enter_portal(self):
        #portal
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_obstect(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player_with_name(copy_portal.teleport_point)

    def check_collisions_walls(self):
        # Détecte la collision avec les murs
        for sprite in self.get_group().sprites():
            # Vérifie la collision avec les murs
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

            for npc in self.get_map().npcs:
                npc.npc_collide = False

                for wall in self.get_walls():
                    # si le npc touche un mur ou le joueur
                    if npc.feet.colliderect(wall) or npc.rect.colliderect(self.game.player.rect):
                        npc.npc_collide = True

            for enemy in self.get_map().enemys:
                enemy.enemy_collide = False

                for wall in self.get_walls():
                    # si l'enemy touche un mur
                    if enemy.feet.colliderect(wall):
                        enemy.enemy_collide = True
                        enemy.move_back()

                    # si l'ennemie touche le joueur
                    elif enemy.rect.colliderect(self.game.player.rect):
                        enemy.enemy_player_collide = True
                        enemy.move_back()

    def check_player_in_safe_zone(self):
        for object_ in self.get_map().tmx_data.objects:
            if object_.type == "safe_zone":
                rect = object_.x, object_.y, object_.width, object_.height 
                if self.player.feet.colliderect(rect):
                    return True

#verifie les collisions
    def check_collisions(self):
        self.check_enter_portal()
        self.check_collisions_walls()

#teleporte le joueur
    def teleport_player_with_name(self, name):
        point = self.get_obstect(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def teleport_player_with_position(self, x, y):
        self.player.position[0] = x
        self.player.position[1] = y
        self.player.save_location()

#enregistre les maps
    def register_map(self, name, portals=[], npcs=[], enemys=[]):
        #charge la carte 
        path = self.game.get_path_assets(f'map\{name}.tmx')
        tmx_data = pytmx.util_pygame.load_pygame(path)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        #définie la liste des collisions
        walls = []

        #ajoute les positions de chaque objets de la classe collision dans la liste walls
        for object_ in tmx_data.objects:
            if object_.type == "collision":
                walls.append(pygame.Rect(object_.x, object_.y, object_.width, object_.height))

        #dessine le groupe de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        group.add(self.player)

        # recupere les npc au groupe
        for npc in npcs:
            group.add(npc)

        # recupere les enemys au groupe
        for enemy in enemys:
            group.add(enemy)

        #creer un objet map
        self.maps[name] = Map(name, walls, portals, group, tmx_data, npcs, enemys)

#recupere les maps 
    def get_map(self):
        return self.maps[self.current_map]

#recupere tout les groupes de la map
    def get_group(self):
        return self.get_map().group

#recupere tout les murs de la map
    def get_walls(self):
        return self.get_map().walls

#recupere tout les obstacles de la map
    def get_obstect(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def teleport_enemy(self):
        for map in self.maps:
            map_data = self.maps[map]
            enemys = map_data.enemys

            for i, enemy in enumerate(enemys):
                enemy.load_point_spawn(map_data.tmx_data, i)
                enemy.teleport_spawn()

#dessine le joueur et centre la cam
    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

#met a jour la map et les collisions
    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            current_direction, moving = npc.move()
            npc.change_animation(current_direction, moving)

        for enemy in self.get_map().enemys:
            enemy.move()

    def remove_enemy(self, enemy):
            current_map = self.get_map()  # Récupérer la carte actuelle
            current_map.group.remove(enemy)  # Supprimer l'ennemi du groupe de sprites
            current_map.enemys.remove(enemy)  # Supprimer l'ennemi de la liste des ennemis actifs