import pygame, time

class Screen:

    def __init__(self, game):
        self.display_width = [1280, 720]
        self.screen = pygame.display.set_mode(self.display_width)
        pygame.display.set_caption('The Antartix')

        self.game = game

        #créez une instance de Life
        self.life = Life_screen(self)
        #créez une instance de fight
        self.fight_display = Fight_display(self)
        self.inventory_display = Inventory_display(self)
        self.death_display = Death(self)
        self.tutorial = Tutorial(self)
        self.pause_menu = Pause_menu(self)
        self.settings = Settings(self)
        self.settings_languages = Settings_Languages(self)

        #charge le hud
        self.hud()

# Affiche l'hud du joueur dans la partie open word du jeu
    def hud(self):
        self.show_life_player()
        self.show_inventory_asset()
        self.show_xp_player()

    def show_life_player(self):
        if self.game.data_player.health is not None and self.game.data_player.max_health is not None:
            self.life.show_hud_life(self.game.data_player.health, self.game.data_player.max_health, (20, 20), (50, 178, 50), (50, 50, 50))
            self.draw_txt("HP", 20, (300, 24), False, (255, 102, 0))

    def show_inventory_asset(self):
        path = self.game.get_path_assets('action_player/Item.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (75, 75))
        self.blit_ressource(image, (1200, 640))

    def show_xp_player(self):
        xp = self.game.data_player.xp
        max_xp = self.game.data_player.xp_max
        self.show_bar(xp, max_xp, (20, 43), (37, 31, 252), (50, 50, 50), 260)
        self.draw_txt("XP", 20, (260, 47), False, (255, 102, 0))
        self.draw_txt(f"lvl {self.game.data_player.lvl}", 25, (282,47), False, (0, 0, 139))

    def blit_ressource(self, ressource, position=(0,0)):
        self.screen.blit(ressource, position)

    def draw_color(self, surface, color, position=(0, 0)):
        pygame.draw.rect(surface, color, position)

    def draw_txt(self, txt, police=50, position=(0, 0), center=False, color=(255, 255, 255), render=False, can_blit=True):
        path = self.game.get_path_assets('font\Arialic Hollow.ttf')
        font = pygame.font.SysFont(path, police, True)
        txt_surface = font.render(txt, render, color)

        if center:
            position = txt_surface.get_rect(center=(self.screen.get_width()/2, position[1])) # position 1 signifie le y

        if can_blit:
            self.blit_ressource(txt_surface, position)
        return txt_surface, position


# Permet de changer facilement le changement de taille d'une image
    def transform_img(self, image, scale):
        return pygame.transform.scale(image, scale)

    def system_message(self, message, time=2000):
        self.draw_txt(message, 50, (0, 50), True, (0, 0, 0), True)
        pygame.display.flip()
        pygame.time.wait(time)

    def show_bar(self, valur, max_valur, position, color_bar, back_color_bar, max_w=300):
        x, y = position
        int_health = valur*max_w/max_valur
        bar_position = [x, y, (int_health), 20]
        back_bar_position = [x, y, max_w, 20]

        self.draw_color(self.screen, back_color_bar, back_bar_position)
        self.draw_color(self.screen, color_bar, bar_position)

        self.int(valur, max_valur, x, y)

    def int(self, valur, max_valur, x, y):
        valur, max_valur = int(valur), int(max_valur)
        txt = f"{valur} / {max_valur}"
        color = (255, 255, 255)
        position = (x, y + 3)
        self.draw_txt(txt, 20, position, False, color)

    def background_message(self, position, txt_width, txt_height):
        (x, y), w, h = position, txt_width+10, txt_height
        self.draw_color(self.screen, (0, 0, 0), (x-5, y-2, w, h+2))

    def display_messages(self):
        # Obtient l'heure actuelle
        now = time.time()
        font = pygame.font.Font(None, 20)

        # Affiche tous les messages
        for i, (message, message_time) in enumerate(self.game.messages_system):
            message, message_time = self.game.messages_system[i]

            # Si le message a plus de 2 secondes, le supprime de la file d'attente
            if now - message_time > 2:
                self.game.messages_system.pop(i)
            else:
                # Prépare le texte
                text = font.render(message, True, (255, 255, 255))
                text_width, text_height = text.get_size()
                x, y = 20, (135 + i * 15)

                # Dessine le fond
                self.background_message((x, y), text_width, text_height)

                # Puis dessine le texte
                self.screen.blit(text, (x, y))



class Life_screen:

    def __init__(self, screen):
        self.screen = screen

    def update_life_bar(self, health, max_health, position, color_bar, back_color_bar):
        self.screen.show_bar(health, max_health, position, color_bar, back_color_bar)

# Affiche la vie sous forme de barre
    def show_hud_life(self, health, max_health, position, color_bar, back_color_bar):
        self.update_life_bar(health, max_health , position, color_bar, back_color_bar)



class Fight_display:

    def __init__(self, screen):
        self.screen = screen

# regroupe tout se qui a à afficher durant un combat (normalement)
    def screen_fight(self, action):
        path = self.screen.game.get_path_assets('bg_fight.jpeg')
        background = pygame.image.load(path)
        self.screen.blit_ressource(background)
        self.show_entity()
        self.show_hud_fight(action)

                                            #affiche le hud du combat

    def ia_hud_fight(self):
        enemy_health = self.screen.game.fight.current_enemy.health
        enemy_max_health = self.screen.game.fight.current_enemy.max_health

        self.screen.life.show_hud_life(enemy_health, enemy_max_health, (960, 20), (255, 0, 0), (50, 50, 50))

    def append_txt_surface_rect(self, txt_surface_rect):
            if txt_surface_rect not in self.screen.game.fight_player.player_action_rects:
                self.screen.game.fight_player.player_action_rects.append(txt_surface_rect)

    def draw_player_action(self, action):
        x, y = 1040, 640
        for txt in action:
            path = self.screen.game.get_path_assets(f'action_player/{txt}.png')
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (75, 75))
            image_rect = image.get_rect()
            image_rect.topleft = (x, y)

            self.screen.blit_ressource(image, (x, y))
            x += 80

            self.append_txt_surface_rect(image_rect)

    def player_hud_fight(self, action):
        player_health = self.screen.game.data_player.health
        player_max_health = self.screen.game.data_player.max_health
        xp = self.screen.game.data_player.xp
        xp_max = self.screen.game.data_player.xp_max

        self.screen.life.show_hud_life(player_health, player_max_health, (20, 667), (50, 178, 50), (50, 50, 50))
        self.screen.draw_txt("HP", 20, (300, 671), False, (255, 102, 0))
        self.screen.show_bar(xp, xp_max, (20, 690), (37, 31, 252), (50, 50, 50), 260)
        self.screen.draw_txt("XP", 20, (260, 694), False, (255, 102, 0))
        self.screen.draw_txt(f"lvl {self.screen.game.data_player.lvl}", 25, (282,694), False, (0, 0, 139))
        self.draw_player_action(action)

    def show_hud_fight(self, action):
        self.ia_hud_fight()
        self.player_hud_fight(action)

                                            # Affiche les entités en combats

    def draw_player(self):
        #modifie l'image du joueur
        fight_player_image = self.screen.game.player.images['up']
        fight_player_image = self.screen.game.player.settings_img_player(fight_player_image, 250, 250)

        #affiche l'image du joueur
        self.screen.blit_ressource(fight_player_image, (160, 355))

    def draw_enemy(self):
        enemy_image = self.screen.game.fight.current_enemy.image
        self.screen.blit_ressource(enemy_image, (900, 250))

    def show_entity(self):
        self.draw_player()
        self.draw_enemy()



class Inventory_display:
    def __init__(self, screen):
        self.screen = screen

                                            # Dessine l'inventaire

    def draw_inventory_display(self, origin):
        self.draw_inventory_background(origin)

        position = (0, 0)
        self.draw_object(position)

    def draw_inventory_background(self, origin):
        path = self.screen.game.get_path_assets('inventory\inventory_background.png')
        img = pygame.image.load(path)

        # Défini ou le background de l'inventaire s'arrete (en hauteur)
        if origin == "fight":
            h = 612
        else:
            h = 720

        img = pygame.transform.scale(img, (426, h))
        self.background_inventaire_position = (0, 0, 426, h)
        self.screen.blit_ressource(img, self.background_inventaire_position)

                                            # Dessine les objets dans l'inventaire

    def blit_img_object(self, objet, position):
        self.screen.blit_ressource(objet[0].image, position)

    def number_object(self, objet, position):
        number = str(objet[1])
        x, y = position
        position_number = (x + objet[0].image.get_width() - 10, y + objet[0].image.get_height() - 10)
        color = (255, 255, 255)
        self.screen.draw_txt(number, 20, position_number, False, color, True)

    def determinate_img_object_postion(self, i, position):
        y = position[1]
        return (i*60, y)

    def draw_object(self, position):
        for i, objet in enumerate(self.screen.game.inventory.objet_inventory):
            position = self.determinate_img_object_postion(i, position)
            self.blit_img_object(objet, position)
            self.number_object(objet, position)

            if not objet[0].name in self.screen.game.inventory.objet_inventory_rects:
                self.append_object_rect((position, objet))

                                            # Intération avec l'inventaire
    # Permet de détécter (dans le 'open_inventory()' du data_player.py) que le joueur clique dans/dehors de l'inventaire
    def enter_zone_inventory(self) -> pygame.Rect:
        position = pygame.Rect(self.background_inventaire_position)
        return position

    def append_object_rect(self, objet_inventory_rect):
        if objet_inventory_rect not in self.screen.game.inventory.objet_inventory_rects:
            self.screen.game.inventory.objet_inventory_rects.append(objet_inventory_rect)





class Death:

    def __init__(self, screen):
        self.screen = screen

    def show_death(self, cause, number_image):
        self.blit_background()
        self.show_txt(cause, number_image)

    def blit_background(self):
        path = self.screen.game.get_path_assets(f"Game_Over.png")
        image = pygame.image.load(path)
        self.screen.blit_ressource(image)

    def show_txt(self, cause, number_image):
        self.show_txt_death(cause, number_image)
        self.show_exit_txt()

    def show_txt_death(self, cause, number_image):
        txt_key = f"{cause}_{number_image}"
        txt = self.screen.game.load_txt("game_over", txt_key)
        self.screen.draw_txt(txt, 60, (0, 200), True, (255, 255, 255), True) # affiche le txt a l'écran avec une police de 30 et en x=centre, y=200

    def show_exit_txt(self):
        txt_key_button = "press_space"
        txt_key_exit = 'exit'
        txt = f"{self.screen.game.load_txt('button_press', txt_key_button)} {self.screen.game.load_txt('message_system', txt_key_exit)}"
        self.screen.draw_txt(txt, 50, (0, 650), True, (255, 255, 255), True) # affiche le txt a l'écran avec une police de 50 et en x=centre, y=650




class Tutorial:
    def __init__(self, screen):
        self.screen = screen

    def show_tutorial(self, message):
        self.show_message(message)

    def background(self, txt_surface, margin, image=None):
        background = pygame.Surface((2000, 1000))
        if image:  # Si une image est fournie
            image_surface = pygame.image.load(image)  # Chargez l'image en tant que surface Pygame
            background.blit(image_surface, (0, 0))  # Affichez le fond aux coordonnées
        return background

    def show_message(self, message):
        lines = message.split('\n')  # Divisez le message en lignes
        for i, line in enumerate(lines):
            txt_surface, position = self.screen.draw_txt(line, 30, (0, i*10), True, (255, 255, 255), True, False)  # Rendez chaque ligne séparément
            background = self.background(txt_surface, 10)  # Ajoutez 10px de marge
            background.blit(txt_surface, (5, 5))  # Dessinez le texte sur le fond avec une marge de 5px
            self.screen.blit_ressource(background, (0, i*30))

    def clear_tutorial(self):
        self.screen.game.map_manager.draw()





class Pause_menu:

    def __init__(self, screen):
        self.screen = screen
        self.dic_buttons = {}  # stock les coordonnées des bouttons

    def show_pause(self):
        self.show_background()
        self.show_title()
        self.show_buttons()

    def show_background(self):
        background_path = self.screen.game.get_path_assets("pause_menu\pause_menu_bg.jpg")
        background = pygame.image.load(background_path)
        background = self.screen.transform_img(background, self.screen.display_width)
        self.screen.blit_ressource(background, (0, 0))

    def show_title(self):
        title = self.screen.game.load_txt('pause_menu', 'title')
        self.screen.draw_txt(title, 100, (0, 50), True, (255, 255, 255), True)

    def show_buttons(self):
        self.show_button_settings()

    def buttons(self, txt_key, txt, button_number, dic):
        y = 100+50*button_number
        txt_surface, position = self.screen.draw_txt(txt, 50, (0, y), True, (255, 255, 255), True)
        x, y, w, h = position
        button_position = x -10, y-10, w + 10, h + 10
        dic[txt_key] = button_position  # Stockez les coordonnées du bouton

    def show_button_settings(self):
        txt_key = 'settings_button'
        txt = self.screen.game.load_txt('pause_menu', txt_key)
        self.buttons(txt_key, txt, 1, self.dic_buttons)





class Settings:

    def __init__(self, screen):
        self.screen = screen
        self.dic_buttons = {}  # stock les coordonnées des bouttons

    def show_settings(self):
        self.show_background()
        self.show_title()
        self.show_buttons()

    def show_background(self):
        self.screen.pause_menu.show_background()

    def show_title(self):
        title = self.screen.game.load_txt('settings_menu', 'title')
        self.screen.draw_txt(title, 100, (0, 50), True, (255, 255, 255), True)

    def show_buttons(self):
        self.show_button_language()

    def show_button_language(self):
        txt_key = 'language'
        txt = self.screen.game.load_txt('settings_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 1, self.dic_buttons)




class Settings_Languages:
    def __init__(self, screen):
        self.screen = screen
        self.dic_buttons = {}  # stock les coordonnées des bouttons

    def show_settings_languages(self):
        self.show_background()
        self.show_title()
        self.show_buttons()

    def show_background(self):
        self.screen.pause_menu.show_background()

    def show_title(self):
        title = self.screen.game.load_txt('settings_languages_menu', 'title')
        self.screen.draw_txt(title, 100, (0, 50), True, (255, 255, 255), True)

    def show_buttons(self):
        self.show_button_language_french()
        self.show_button_language_english()

    def show_button_language_french(self):
        txt_key = 'french'
        txt = self.screen.game.load_txt('languages', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 1, self.dic_buttons)

    def show_button_language_english(self):
        txt_key = 'english'
        txt = self.screen.game.load_txt('languages', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 2, self.dic_buttons)