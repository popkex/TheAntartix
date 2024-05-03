import pygame, pytmx, pyscroll, random
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

class MapManager:

    def __init__(self, game, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.game = game
        self.current_map = "world"

        #permet le lancement des combats
        self.battle_running = False

#défini les maps
#dans le monde normal
        #défini : le monde d'origine (le monde normal), le point d'entrée, le monde d'entrée, le lieu de spawn dans le monde d'entrée
        self.register_map("world", portals=[
            Portal(from_world="world", origin_point="enter_house1", target_world="house1", teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_house2", target_world="house2", teleport_point="spawn_house"),
            Portal(from_world="world", origin_point="enter_donjon1", target_world="donjon1", teleport_point="spawn_donjon"),
        ])

#depuis les maisons
        #defini le monde d'origine (la maison), le point de sortie, le monde de sortie, l'endroit du spawn dans le monde de sortie
        self.register_map("house1", portals=[
            Portal(from_world="house1", origin_point="exit_house", target_world="world", teleport_point="exit_house1")
        ])
        self.register_map("house2", portals=[
            Portal(from_world="house2", origin_point="exit_house", target_world="world", teleport_point="exit_house2")
        ])
        self.register_map("donjon1", portals=[ 
            Portal(from_world="donjon1", origin_point="exit_donjon", target_world="world", teleport_point="exit_donjon1")
        ])

        #défini le lieu de spawn qui s'appelle 'player_spawn'
        self.teleport_player_with_name('player_spawn')

    def check_enter_portal(self):
        #portal
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_obstact(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player_with_name(copy_portal.teleport_point)

    def active_fight(self):
        find_enemy = random.randint(0, 2000)
        for object_ in self.get_map().tmx_data.objects:
            if object_.type == "enemie" and find_enemy <= 2: # (de base 2)
                enemy_rect = pygame.Rect(object_.x, object_.y, object_.width, object_.height)
                if self.player.feet.colliderect(enemy_rect):
                    return True
        return False

    def check_collisions_walls(self):
        #detect la collision avec les mures
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

#verifie les collisions
    def check_collisions(self):
        self.check_enter_portal()
        self.check_collisions_walls()

#teleporte le joueur
    def teleport_player_with_name(self, name):
        point = self.get_obstact(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def teleport_player_with_position(self, x, y):
        self.player.position[0] = x
        self.player.position[1] = y
        self.player.save_location()

#enregistre les maps
    def register_map(self, name, portals=[]):
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
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)

        #creer un objet map
        self.maps[name] = Map(name, walls, portals, group, tmx_data)

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
    def get_obstact(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

#dessine le joueur et centre la cam
    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

#met a jour la map et les collisions
    def update(self):
        self.get_group().update()
        self.check_collisions()