import pygame, pytmx, pyscroll
from player import *
from inventory import *
from data_maps import DataMap
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
    walls_name: dict
    portals: list[Portal]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    npcs: list[NPC]
    enemys: list[Enemy]

class MapManager:

    def __init__(self, game, screen, player, reset_tile=False, reset_entity=False):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.game = game
        self.current_map = "artixs_temple_first"
        self.tile_modified = {}
        if not reset_tile:
            self.tile_modified = self.game.saves.load_modified_map()
            '''
            {'word': {
                (x, y): gid,
                (x, y): gid,
            },
            'oser_map:{
                (x, y): gid,
                ...
            }
            }
            '''

        #permet le lancement des combats
        self.battle_running = False

        #map les enemys
        self.enemy_classes = {
            'EnemyA': EnemyA,
            'EnemyB': EnemyB,
        }

        self.init_all_maps(reset_entity)
        self.load_tiles()

    def init_all_maps(self, reset_entity):
        self.register_map('artixs_temple_first')
        self.register_map("world")
        self.register_map("house1")
        self.register_map("house2")
        self.register_map("donjon1")
        self.teleport_player_with_name('player_spawn')
        self.teleport_npcs()
        self.teleport_enemy()

        if not reset_entity:
            for map in self.maps:
                data_map = self.get_map(map)
                self.load_entity(data_map.npcs, data_map.enemys)

    def save_tiles(self):
        self.game.saves.save_tiles()

    def load_tiles(self):
        for map_name, modifications in self.tile_modified.items():
            for (x, y), gid in modifications.items():
                self.change_tuile(x, y, gid, map_name=map_name)

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
                    # modifie le texte du png en fonction de si ca quete a été complété ou non
                    if npc.quest_state:
                        key_txt = npc.after_quest_txt
                    else:
                        key_txt = npc.key_txt

                    reading = dialog_box.execute(key_txt, key_txt_name, npc.quest)

                    if npc.quest and not reading:
                        name_quest, type_quest, objectif_quest, rewards, rewards_quantity, key_description = npc.quest
                        self.game.quest.add_quest(name_quest, type_quest, objectif_quest, rewards, rewards_quantity, key_description)

    def check_enter_portal(self):
        #portal
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_obstect(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                for entity in self.get_group():
                    if entity.feet.colliderect(rect):
                        copy_portal = portal
                        self.current_map = portal.target_world
                        self.teleport_entity_with_name(copy_portal.teleport_point, entity)

    def detect_wall_collision_side(self, entity, wall):
        dx = (entity.feet.right - wall.left, wall.right - entity.feet.left)
        dy = (entity.feet.bottom - wall.top, wall.bottom - entity.feet.top)
        min_dx = min(dx)
        min_dy = min(dy)

        entity.reset_dic_collide_walls()

        if min_dx < min_dy:
            if dx[0] < dx[1]:
                entity.dic_collide_walls['left'] = True
            if dx[0] > dx[1]:
                entity.dic_collide_walls['right'] = True

        if min_dx > min_dy:
            if dy[0] < dy[1]:
                entity.dic_collide_walls['top'] = True
            if dy[0] > dy[1]:
                entity.dic_collide_walls['bottom'] = True

        return entity.dic_collide_walls

    def check_collisions_walls(self):
        # Détecte la collision avec les murs
        for sprite in self.get_group().sprites():
            side = None
            collided_walls = []
            for wall in self.get_walls():
                if sprite.feet.colliderect(wall):
                    collided_walls.append(wall)

            sprite.reset_dic_collide_walls()

            for wall in collided_walls:
                side = self.detect_wall_collision_side(sprite, wall)
                sprite.move_back(side)

            for npc in self.get_map().npcs:
                npc.npc_collide = False

                for wall in self.get_walls():
                    # si le npc touche un mur ou le joueur
                    if npc.feet.colliderect(wall) or npc.rect.colliderect(self.game.player.rect):
                        npc.npc_collide = True

            for enemy in self.get_map().enemys:
                enemy.enemy_collide = False
                # si l'ennemie touche le joueur
                if enemy.rect.colliderect(self.game.player.rect):
                    enemy.enemy_player_collide = True
                    enemy.dic_collide_walls['stop'] = True

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

#teleport nimporte qu'elle entity
    def teleport_entity_with_name(self, name, entity):
        point = self.get_obstect(name)
        entity.position[0] = point.x
        entity.position[1] = point.y
        entity.save_location()

    def teleport_entity_with_position(self, x, y, entity):
        entity.position[0] = x
        entity.position[1] = y
        entity.save_location()

#enregistre les maps
    def register_map(self, name):
        #charge la carte 
        path = self.game.utils.get_path_assets(f'map\{name}.tmx')
        tmx_data = pytmx.util_pygame.load_pygame(path)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        #définie la liste des collisions
        walls = []
        walls_name = {}

        #ajoute les positions de chaque objets de la classe collision dans la liste walls
        for object_ in tmx_data.objects:
            if object_.type == "collision":
                rect = pygame.Rect(object_.x, object_.y, object_.width, object_.height)
                walls.append(rect)
                walls_name[object_.name] = rect

        #dessine le groupe de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=7)
        group.add(self.player)

        data_map = DataMap(name)
        data_map = data_map.data

        portals = [Portal(**portal) for portal in data_map.get('portals', [])]

        npcs = self.load_npcs(data_map)
        enemys = self.load_enemy(data_map)

        # recupere les npc au groupe
        for npc in npcs:
            group.add(npc)

        # recupere les enemys au groupe
        for enemy in enemys:
            group.add(enemy)

        #creer un objet map
        self.maps[name] = Map(name, walls, walls_name, portals, group, tmx_data, npcs, enemys)

    def load_npcs(self, data_map):
        npcs = [NPC(**npc) for npc in data_map.get('npcs', [])]
        return npcs

    def load_enemy(self, data_map):
        enemys = []
        for enemy_data in data_map.get('enemys', []):
            quantity = enemy_data.get('quantity', 0)
            enemy_type = enemy_data.get('type', 0)
            enemy_type = self.enemy_classes[enemy_type]
            for _ in range(quantity):
                enemys.append(enemy_type(self.game))
        return enemys

#permet de charger apres une save les emplacements des enemies
    def load_entity(self, npcs, enemys):
        # charge les données existantes
        data = self.game.saves.load_npcs_enemys_position()
        if data:
            npcs_data, enemys_data = data[0], data[1]

            for npc_datas in npcs_data:
                npc_name = npc_datas[0]
                npc_position = npc_datas[1]
                npc_current_point = npc_datas[2]
                for npc in npcs:
                    if npc.name == npc_name:
                        npc.position = npc_position
                        npc.current_point = npc_current_point

            all_enemys = enemys.copy()

            for enemy_datas in enemys_data:
                number_enemy = enemy_datas[0]
                enemy_position = enemy_datas[1]
                for enemy in enemys:
                    if enemy.number_enemy == number_enemy:
                        enemy.position = enemy_position
                        all_enemys.remove(enemy)

            for enemy in all_enemys:
                self.remove_enemy(enemy)


#recupere les maps 
    def get_map(self, map=None):
        if map:
            return self.maps[map]
        else:
            return self.maps[self.current_map]

#recupere tout les groupes de la map
    def get_group(self):
        return self.get_map().group

#recupere tout les murs de la map
    def get_walls(self):
        return self.get_map().walls
    def get_wall_name(self):
        return self.get_map().walls_name
    def get_wall_rect_in_name(self, name):
        return self.get_map().walls_name[name]

#recupere tout les obstacles de la map
    def get_obstect(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

#supprime un mur choisi
    def remove_wall(self, wall_name):
        if wall_name in self.get_wall_name():
            self.get_walls().remove(self.get_wall_rect_in_name(wall_name))
            del self.get_wall_name()[wall_name]

        '''exemple d'utilisation : 
            if event.key == pygame.K_SPACE:
                self.map_manager.remove_wall("test")'''

#supprime une tuile choisi
    def change_tuile(self, tuile_position_x, tuile_position_y, gid, map_name=None):
        # si une map n'a pas été founis
        if not map_name:
            #obtiens les données actuelles de la map
            tmx_data = self.get_map().tmx_data
            map_name = self.current_map

            '''Exemple d'utilisation :
            Suppose que gid = 1 est l'identifiant de la nouvelle tuile.
            self.map_manager.change_tuile(5, 10, 1)'''
        # si une map a été fournis
        else:
            tmx_data = self.maps[map_name].tmx_data

        #accède a la couche de la tuile (le calque)
        layer = None
        for l in tmx_data.visible_layers:
            if isinstance(l, pytmx.TiledTileLayer):
                layer = l
                break
        if layer is None:
            raise ValueError("Aucune couche de tuiles trouvée")

        #modifie la tuile
        layer.data[tuile_position_y][tuile_position_x] = gid

        if map_name not in self.tile_modified:
            self.tile_modified[map_name] = {}
        self.tile_modified[map_name][(tuile_position_x, tuile_position_y)] = gid
        self.save_tiles()

        #reload la map si le joueur a fournis une map
        self.reload_map(reload_npcs=False, reload_enemys=False, reload_npcs_position=False, reload_player_position=False)

#actualise la map (les enemies ne réaparaisse pas et les status des npcs ne changent pas)
    def reload_map(self, reload_player_position=True, reload_group=True, reload_npcs=True, reload_npcs_position=True, reload_enemys=True, reload_enemys_position=True, map_name=None):
        # si le joueur n'a pas fournis de map, prendre la map en cours
        if not map_name:
            # recupere les données actuelles
            walls = self.get_walls()
            walls_name = self.get_wall_name()
            portals = self.get_map().portals
            group = self.get_group()
            tmx_data = self.get_map().tmx_data
            npcs = self.get_map().npcs
            enemys = self.get_map().enemys
            current_map = self.get_map()
            map_name = self.current_map
        else:
            data_map = self.maps[map_name]
            walls = data_map.walls
            walls_name = data_map.walls_name
            portals = data_map.portals
            group = data_map.group
            tmx_data = data_map.tmx_data
            npcs = data_map.npcs
            enemys = data_map.enemys
            current_map = data_map

        map_data = pyscroll.data.TiledMapData(current_map.tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        if reload_group:
            # Mettez à jour le groupe de calques
            group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=7)
            group.add(self.player)

        if reload_player_position:
            # téléporte le joueur au spawn de la map
            self.teleport_player_with_name('player_spawn')

        data_map = DataMap(map_name)
        data_map = data_map.data

        if reload_npcs:
            npcs = self.load_npcs(data_map)
            # recupere les npc au groupef
            for npc in npcs:
                group.add(npc)
        elif reload_group:
            for npc in npcs:
                group.add(npc)

        if reload_enemys:
            enemys = self.load_enemy(data_map) 
            # recupere les enemys au groupe
            for enemy in enemys:
                group.add(enemy)
        elif reload_group:
            for enemy in enemys:
                group.add_enemys

        self.maps[map_name] = Map(map_name, walls, walls_name, portals, group, tmx_data, npcs, enemys)

        if reload_npcs_position:
            self.teleport_npcs(current_map=True)
        if reload_enemys_position:
            self.teleport_enemy(current_map=True)

        self.game.stop_update = True

    def teleport_npcs(self, current_map=False):
        if current_map:
            map_data = self.get_map()
            for npc in self.get_map().npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()
        else:
            for map in self.maps:
                map_data = self.maps[map]
                npcs = map_data.npcs

                for npc in npcs:
                    npc.load_points(map_data.tmx_data)
                    npc.teleport_spawn()

    def teleport_enemy(self, current_map=False):
        # uniquement pour la map ou ce trouve le joueur
        if current_map:
            map_data = self.get_map()
            enemys = map_data.enemys

            for i, enemy in enumerate(enemys):
                enemy.load_point_spawn(map_data.tmx_data, i)
                enemy.teleport_spawn()
        # pour toute les maps
        else:
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
            for map in self.maps:
                map = self.get_map(map)
                if enemy in map.enemys:
                    map.group.remove(enemy)  # Supprimer l'ennemi du groupe de sprites
                    map.enemys.remove(enemy)  # Supprimer l'ennemi de la liste des ennemis actifs
                    break