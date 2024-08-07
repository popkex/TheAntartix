import pygame, sys, os, random, math
from utils import Utils


utils = Utils()

class Entity(pygame.sprite.Sprite):

    def __init__(self, name, x, y):
        super().__init__()

        #recupere les sprites du joueur si l'image n'est pas en .png 
        if not "." in name:
            path = self.get_path_assets(f'npc\{name}.png')
        else:
            path = self.get_path_assets(name)

        self.sprite_sheet = pygame.image.load(path)

        #recupere l'image du joueur par defaut
        self.image = self.get_image(0, 0)
        self.settings_img_player(self.image)
        self.rect = self.image.get_rect()

        #determine la postiton du joueur
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width / 2, 1)
        self.old_position = self.position.copy()
        self.frame_speed = 1.5 # défini la vitesse a 1.5px par frame
        self.calculate_speed()
        self.velocity = [0, 0]
        self.actualy_move_back = False
        self.dic_collide_walls = {
            "top": False,
            'bottom': False,
            "left": False,
            "right": False,
            "stop": False,
        }

        self.image_animation_down = [
            self.get_image(2, 0), # L'image numéro 1
            self.get_image(33, 0), # L'image numéro 2
            self.get_image(65, 0), # L'image numéro 3
        ]
        self.image_animation_left = [
            self.get_image(4, 32), # L'image numéro 1
            self.get_image(36, 32), # L'image numéro 2
            self.get_image(68, 32), # L'image numéro 3
        ]
        self.image_animation_right = [
            self.get_image(3, 64), # L'image numéro 1
            self.get_image(35, 64), # L'image numéro 2
            self.get_image(65, 64), # L'image numéro 3
        ]
        self.image_animation_up = [
            self.get_image(1, 96), # L'image numéro 1
            self.get_image(34, 96), # L'image numéro 2
            self.get_image(66, 96), # L'image numéro 3
        ]

        #stock les differentes images animées du joueur
        self.images_animations = {
            'down' : self.get_animation('down'),
            'left' : self.get_animation('left'),
            'right' : self.get_animation('right'),
            'up' : self.get_animation('up')
        }

        # stock les differentes images statique du joueur
        self.images = {
            'down' : self.get_image(0, 0),
            'left' : self.get_image(0, 32),
            'right' : self.get_image(0, 64),
            'up' : self.get_image(0, 96)
        }

# gere l'animation du joueur
    def get_animation(self, name_sprite):
        animations = []
        for i in range(0, 3):
            animations.append(getattr(self, 'image_animation_' + name_sprite)[i])
        return animations

# permet de retrouver le chemin d'acces vers les assets lors de la compilation du jeu
    def get_path_assets(self, ressource):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, "assets") + "\\" + ressource

#sauvegarde lancienne position du joueur
    def save_location(self):
        self.old_position = self.position.copy()

#parametre l'image du joueur
    def settings_img_player(self, image, x_size=32, y_size=32):
        #change la taille du joueur
        self.image = pygame.transform.scale(image, (x_size, y_size))
        #retire la couleur noir du contour du joueur
        self.image.set_colorkey([0, 0, 0])

        return self.image

#change l'image du joueur
    def change_animation(self, name, mooving=True):
        if name and mooving:
            # Obtenir le temps actuel
            current_time = pygame.time.get_ticks()
            # Définir la vitesse d'animation (millisecondes par image)
            animation_speed = 250  # Réglage de la vitesse d'animation
            # Obtenir les images d'animation
            animation_images = self.images_animations[name]
            # Calculer l'indice de l'image actuelle en fonction du temps
            frame_index = (current_time // animation_speed) % len(animation_images)
            # Changer l'image du joueur
            self.image = animation_images[frame_index]
            self.settings_img_player(self.image)

#change l'image du joueur
    def change_image(self, name):
        self.image = self.images[name]
        self.settings_img_player(self.image)

#permet les deplacement du joueur
    def move_right(self):
        self.velocity[0] = 1
    def move_left(self):
        self.velocity[0] = -1
    def move_up(self):
        self.velocity[1] = -1
    def move_down(self):
        self.velocity[1] = 1
    def reset_move(self):
        self.velocity = [0, 0]

    def calculate_gravity(self):
        self.velocity[0] *= utils.gravity
        self.velocity[1] *= utils.gravity
        return self.velocity

    def calculate_speed(self):
        self.speed = (self.frame_speed * utils.fps_limite) / 2
        return self.speed

    def update_move(self):
        self.calculate_gravity() # permet de modifier la vitesse de tout les perso en fonction de la "gravité"
        self.calculate_speed()
        self.position[0] += self.velocity[0] * self.speed * utils.delta_time
        self.position[1] += self.velocity[1] * self.speed * utils.delta_time

    def reset_dic_collide_walls(self):
        self.dic_collide_walls = {
            "top": False,
            'bottom': False,
            "left": False,
            "right": False,
            "stop": False,
        }

#actualise la position du joeuur
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

#redonne lancienne position au joueur si jamais il entre en collision
    def move_back(self, direction):
        if direction:
            if direction["top"]:
                self.position[1] = self.old_position[1]
                self.velocity[1] -= 1

            if direction["bottom"]:
                self.position[1] = self.old_position[1]
                self.velocity[1] += 1

            if direction["left"]:
                self.position[0] = self.old_position[0]
                self.velocity[0] -= 1

            if direction["right"]:
                self.position[0] = self.old_position[0]
                self.velocity[0] += 1

            if direction["stop"]:
                self.velocity = [0, 0]

            self.update_move()
            self.actualy_move_back = True

#permet de recuperer l'image du joueur dans le sprite sheet
    def get_image(self, x, y):
        image = pygame.Surface([29, 31])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 29, 31))
        return image

    def get_coordonnes(self):
        return self.position

    def is_moving(self):
        return self.old_position != self.position



class Player(Entity):

    def __init__(self):
        super().__init__('player', 0, 0)



class NPC(Entity):

    def __init__(self, name, nb_points, key_txt, quest=None, quest_state=False, after_quest_txt=None):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.name = name
        self.key_txt = key_txt
        self.npc_collide = False
        self.current_position = 'up'
        self.points = []
        self.speed = 0.5
        self.current_point = 0
        self.quest = quest
        self.quest_state = quest_state
        self.after_quest_txt = after_quest_txt

    def move(self):
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0
        target_rect = self.points[target_point]

        current_direction = None
        moving = False  # Initialisation du drapeau de mouvement

        self.reset_move()

        if not self.npc_collide:
            if self.position[0] > target_rect.x + 10:
                self.move_left()
                current_direction = 'left'
                moving = True
            elif self.position[0] < target_rect.x - 10:
                self.move_right()
                current_direction = 'right'
                moving = True

            if self.position[1] < target_rect.y - 10:
                self.move_down()  # Déplacement vers le bas effectué ici
                current_direction = 'down'
                moving = True
            elif self.position[1] > target_rect.y + 10:
                self.move_up()  # Déplacement vers le haut effectué ici
                current_direction = 'up'
                moving = True

        self.update_move()

        # permet de faire en sorte qu'un npc peut rester a son target point un certain moment
        npc_can_move_luck = random.randint(0, 1000)
        npc_can_move = False
        if npc_can_move_luck <= 5:
            npc_can_move = True

        if self.rect.colliderect(target_rect) and npc_can_move:
            self.current_point = target_point

        self.save_location()

        return current_direction, moving

    def teleport_spawn(self):
        self.current_point = 0
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        self.points = []
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)

class Enemy(Entity):

    def __init__(self, classe, game, path, image, name, field_of_view=150):
        super().__init__(path, 0, 0)
        self.game = game
        self.classe = classe
        self.name = name
        self.field_of_view = field_of_view # défini le champ de vision de l'enemie
        self.enemy_collide = False
        self.enemy_player_collide = False
        self.current_position = 'up'
        self.speed = random.randint(100, 300) / 100 # permet une vitesse sous forme de : 1.31
        self.point_spawn = None

        self.enemy_killed = False
        self.player_proximity = False

        self.image = pygame.transform.scale(image, (32, 32))
        self.image_rect = self.image.get_rect(topleft=self.position)

    def teleport_spawn(self):
        location = self.point_spawn
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_point_spawn(self, tmx_data, number_enemy):
        self.number_enemy = number_enemy
        point = tmx_data.get_object_by_name(f"enemy_spawn_{number_enemy}")
        rect = pygame.Rect(point.x, point.y, point.width, point.height)
        self.point_spawn = rect

    def move_and_animate_up(self):
        self.move_up()  # Déplacement vers le haut effectué ici
        self.current_direction = 'up'
        self.moving = True

    def move_and_animate_down(self):
        self.move_down()  # Déplacement vers le bas effectué ici
        self.current_direction = 'down'
        self.moving = True

    def move_and_animate_right(self):
        self.move_right()
        self.current_direction = 'right'
        self.moving = True

    def move_and_animate_left(self):
        self.move_left()
        self.current_direction = 'left'
        self.moving = True

    def in_fight(self):
        return self.name

    def calculate_dist_player_enemy(self):
        # défini le x et y du joueur
        player_pos = self.game.player.position
        px, py = player_pos

        # défini le x et y de l'enemie
        enemy_pos = self.position
        ex, ey = enemy_pos

        # Calcul de la distance euclidienne
        distance = math.sqrt((ex - px) ** 2 + (ey - py) ** 2)
        return distance

    def detect_player_proximity(self) -> bool:
        if not self.game.map_manager.check_player_in_safe_zone() and self.calculate_dist_player_enemy() <= self.field_of_view:
            return True
        return False

    def move(self):
        self.save_location()

        target_rect = self.game.player.position

        self.current_direction = None
        self.moving = False  # Initialisation du drapeau de mouvement

        self.reset_move()

        # détécte si le joueur est a proximité 
        self.player_proximity = self.detect_player_proximity()

        # vérifie si le joueur est a proximité et si l'enemie ne touche pas un mur
        if not self.enemy_collide and self.player_proximity:
            if self.position[0] > target_rect[0]:
                self.move_and_animate_left()
            elif self.position[0] < target_rect[0]:
                self.move_and_animate_right()

            if self.position[1] < target_rect[1]:
                self.move_and_animate_down()
            elif self.position[1] > target_rect[1]:
                self.move_and_animate_up()

        self.update_move()

        return self.current_direction, self.moving

class EnemyA(Enemy):

    def __init__(self, game):
        self.game = game 

        path = self.game.utils.get_path_assets('enemy\enemyA.gif')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (32, 32))

        field_of_view = 150 # défini le champ de vision

        super().__init__(self, game, "enemy\enemyA.gif", image, "EnemyA", field_of_view)

class EnemyB(Enemy):

    def __init__(self, game):
        self.game = game 

        path = self.game.utils.get_path_assets('enemy\enemyB.webp')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (32, 32))

        field_of_view = 175 # défini le champ de vision

        super().__init__(self, game, "enemy\enemyB.webp", image, "EnemyB", field_of_view) 