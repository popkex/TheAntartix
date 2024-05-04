import pygame, sys, os

class Entity(pygame.sprite.Sprite):

    def __init__(self, name, x, y):
        super().__init__()

        #recupere les sprites du joueur
        path = self.get_path_assets(f'{name}.png')
        self.sprite_sheet = pygame.image.load(path)
        #recupere l'image du joueur par defaut
        self.image = self.get_image(0, 0)
        self.settings_img_player(self.image)
        self.rect = self.image.get_rect()
        #determine la postiton du joueur
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width / 2, 1)
        self.old_position = self.position.copy()
        self.speed = 1

        self.image_animation_down = [
            self.get_image(0, 0), # L'image numéro 1
            self.get_image(34, 0), # L'image numéro 2
            self.get_image(67, 0), # L'image numéro 3
        ]
        self.image_animation_left = [
            self.get_image(2, 32), # L'image numéro 1
            self.get_image(34, 32), # L'image numéro 2
            self.get_image(66, 32), # L'image numéro 3
        ]
        self.image_animation_right = [
            self.get_image(3, 64), # L'image numéro 1
            self.get_image(35, 64), # L'image numéro 2
            self.get_image(67, 64), # L'image numéro 3
        ]
        self.image_animation_up = [
            self.get_image(2, 96), # L'image numéro 1
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
    def change_animation(self, name):
        if name:
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
        self.position[0] += self.speed #le 0 correspond au x (de la liste self.position)
    def move_left(self):
        self.position[0] -= self.speed
    def move_up(self):
        self.position[1] -= self.speed #le 1 correspond au y (de la liste self.position)
    def move_down(self):
        self.position[1] += self.speed

#actualise la position du joeuur
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

#redonne lancienne position au joueur si jamais il entre en collision
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

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

    def __init__(self, name, nb_points):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.name = name
        self.npc_collide = False
        self.current_position = 'up'
        self.points = []
        self.speed = 0.5
        self.current_point = 0

    def move(self):
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        target_rect = self.points[target_point]

        current_direction = None

        if not self.npc_collide:
            if self.position[1] < target_rect.y:
                self.move_down()
                current_direction = 'down'
            elif self.position[1] > target_rect.y:
                self.move_up()
                current_direction = 'up'
            elif self.position[0] > target_rect.x:
                self.move_left()
                current_direction = 'left'
            elif self.position[0] < target_rect.x:
                self.move_right()
                current_direction = 'right'

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

        self.save_location()

        return current_direction

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, map):
        for num in range(1, self.nb_points + 1):
            point = map.get_obstect(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)