import pygame, time, random

class Screen:

    def __init__(self, game):
        self.display_width = [1280, 720]
        self.screen = pygame.display.set_mode(self.display_width, pygame.RESIZABLE + pygame.SCALED)
        pygame.display.set_caption('The Antartix')

        self.language_manager = game.language_manager

        self.game = game
        self.utils = self.game.utils

        self.main_menu = MainMenu(self)
        self.play_chose = PlayChose(self)
        self.confirm_reset_game = ConfirmResetGame(self)
        self.pause_menu = Pause_menu(self)
        self.settings = Settings(self)
        self.settings_languages = Settings_Languages(self)
        self.game_settings_menu = GameSettingsMenu(self)
        self.auto_save_menu = AutoSaveMenu(self)


    def load_game(self):
        self.life = Life_screen(self)
        self.fight_display = Fight_display(self)
        self.death_display = Death(self)
        self.dialog = Dialog(self)
        self.tutorial = Tutorial(self)
        self.tutorial_menu = Tutorial_Menu(self)
        self.quest = Quest(self)
        self.inventory_display = Inventory_display(self)
        #charge le hud
        self.hud()

# Affiche l'hud du joueur dans la partie open word du jeu
    def hud(self):
        self.show_life_player()
        self.show_inventory_asset()
        self.show_xp_player()

    def get_life_color(self, life, max_life):
        # Défini les couleurs pour la vie maximale et minimale
        max_life_color = [50, 178, 50]  # Vert
        min_life_color = [255, 0, 0]  # Rouge

        # Calcule le ratio de la vie actuelle par rapport à la vie maximale
        life_ratio = life / max_life

        # Calcule la nouvelle couleur en fonction du ratio de la vie
        new_color = [
            int(max_color * life_ratio + min_color * (1 - life_ratio))
            for max_color, min_color in zip(max_life_color, min_life_color)
        ]

        return tuple(new_color)

    def show_life_player(self, position=(20, 20)):
        if self.game.data_player.health is not None and self.game.data_player.max_health is not None:
            health = self.game.data_player.health
            max_health = self.game.data_player.max_health
            color = self.get_life_color(health, max_health)

            self.life.show_hud_life(health, max_health, position, color, (50, 50, 50))
            self.draw_txt("HP", 20, (300, position[1]), False, (255, 102, 0))

    def show_xp_player(self, position=(20, 43)):
        xp = self.game.data_player.xp
        max_xp = self.game.data_player.xp_max

        self.show_bar(xp, max_xp, position, color_bar=(37, 31, 252), back_color_bar=(50, 50, 50), max_w=260)
        self.draw_txt("XP", 20, (260, position[1]), False, (255, 102, 0))
        self.draw_txt(f"lvl {self.game.data_player.lvl}", 25, (282, position[1]), False, (0, 0, 139))

    def show_energy_player(self, position=(20, 43)):
        energy = self.game.data_player.energy
        energy_max = self.game.data_player.energy_max

        self.show_bar(energy, energy_max, position, color_bar=(37, 31, 252), back_color_bar=(50, 50, 50))
        self.draw_txt("energy", 20, (274, position[1]), False, color=(255, 102, 0))

    def show_inventory_asset(self):
        path = self.utils.get_path_assets('action_player/Item.png')
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (75, 75))
        self.blit_ressource(image, (1200, 640))

    def blit_ressource(self, ressource, position=(0,0), center=False):
        if center:
            position = ressource.get_rect(center=(self.screen.get_width()/2, position[1]))

        self.screen.blit(ressource, position)

    def draw_color(self, surface, color, position=(0, 0)):
        pygame.draw.rect(surface, color, position)

    def draw_txt(self, txt, police=50, position=(0, 0), center=False, color=(255, 255, 255), render=False, can_blit=True):
        path = self.utils.get_path_assets('font\Arialic Hollow.ttf')
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
        for i, (message, message_time, message_max_time) in enumerate(self.game.messages_system):
            # Si le message a plus de 2 secondes, le supprime de la file d'attente
            if now - message_time > message_max_time:
                self.game.messages_system.pop(i)
            else:
                # Prépare le texte
                text = font.render(message, True, (255, 255, 255))
                text_width, text_height = text.get_size()
                x, y = 20, (135 + i * 15)

                # Dessine le fond
                self.background_message((x, y), text_width, text_height)

                # Puis dessine le texte
                self.blit_ressource(text, (x, y))

    def auto_save_message(self):
        # affiche le logo de la save auto
        position = (1220, 0)
        path = self.utils.get_path_assets("logos\\auto_save.png")
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (50, 50))
        self.blit_ressource(image, position)



class LoadingScreen:

    def __init__(self, screen, paths_img_list):
        self.screen = screen
        self.current_image = 0
        self.dic_img = {} # stock toute les images chargées du chargement
        self.load_imgs(paths_img_list)

    def show_element(self):
        self.show_video()

    def load_imgs(self, paths_img_list):
        # récupére tous les chemins d'acces et charge les images
        for i, path_img in enumerate(paths_img_list):
            self.dic_img[i] = pygame.image.load(path_img)
            self.max_image = i # permet de définir le nombre d'image max

    def show_video(self):
        position = (0, 0)
        self.screen.blit_ressource(self.dic_img[self.current_image], position)

        if self.current_image + 1 <= self.max_image:
            self.current_image += 1
        else:
            self.current_image = 0


class MainMenu:

    def __init__(self, screen):
        self.screen = screen
        self.dic_buttons = {}  # stock les coordonnées des bouttons

    def update_screen(self):
        self.show_background()
        self.show_title()
        self.show_buttons()

# affiche le logo du jeu au demarrage du jeu (possibilité de skip si la personne appuie sur une touche)
    def show_logo(self):
        stop = False
        img = pygame.image.load(self.screen.utils.get_path_assets("logos\\studio_logo.png"))
        self.clock = pygame.time.Clock()
        for alpha in range(0, (180)): # affiche pendant 3s (60*seconds)
            img.set_alpha(alpha/2)
            self.screen.blit_ressource(img, (0, 425), True)
            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    else:
                        stop = True

                if event.type == pygame.QUIT:
                    pygame.quit()

            if stop:
                break


    def show_background(self):
        background_path = self.screen.utils.get_path_assets("pause_menu\pause_menu_bg.jpg")
        background = pygame.image.load(background_path)
        background = self.screen.transform_img(background, self.screen.display_width)
        self.screen.blit_ressource(background, (0, 0))

    def show_title(self):
        title = self.screen.language_manager.load_txt('main_menu', 'title')
        self.screen.draw_txt(title, 70, (0, 50), True, (255, 255, 255), True)

    def show_buttons(self):
        self.show_button_play()
        self.show_button_settings()
        self.show_button_quit()

    def buttons(self, txt_key, txt, button_number, dic):
        y = 100+50*button_number
        txt_surface, position = self.screen.draw_txt(txt, 50, (0, y), True, (255, 255, 255), True)
        x, y, w, h = position
        button_position = x -10, y-10, w + 10, h + 10
        dic[txt_key] = button_position  # Stockez les coordonnées du bouton

    def show_button_play(self):
        txt_key = 'play_button'
        txt = self.screen.language_manager.load_txt('main_menu', txt_key)
        self.buttons(txt_key, txt, 1, self.dic_buttons)

    def show_button_settings(self):
        txt_key = 'settings_button'
        txt = self.screen.language_manager.load_txt('main_menu', txt_key)
        self.buttons(txt_key, txt, 2, self.dic_buttons)

    def show_button_quit(self):
        txt_key = 'quit_button'
        txt = self.screen.language_manager.load_txt('main_menu', txt_key)
        self.buttons(txt_key, txt, 11, self.dic_buttons)



class PlayChose:

    def __init__(self, screen):
        self.screen = screen
        self.dic_buttons = {}  # stock les coordonnées des bouttons

    def update_screen(self):
        self.show_background()
        self.show_title()
        self.show_buttons()

    def show_background(self):
        background_path = self.screen.utils.get_path_assets("pause_menu\pause_menu_bg.jpg")
        background = pygame.image.load(background_path)
        background = self.screen.transform_img(background, self.screen.display_width)
        self.screen.blit_ressource(background, (0, 0))

    def show_title(self):
        title = self.screen.language_manager.load_txt('play_chose', 'title')
        self.screen.draw_txt(title, 70, (0, 50), True, (255, 255, 255), True)

    def show_buttons(self):
        self.show_button_play()
        self.show_button_settings()
        self.show_button_back()

    def buttons(self, txt_key, txt, button_number, dic):
        y = 100+50*button_number
        txt_surface, position = self.screen.draw_txt(txt, 50, (0, y), True, (255, 255, 255), True)
        x, y, w, h = position
        button_position = x -10, y-10, w + 10, h + 10
        dic[txt_key] = button_position  # Stockez les coordonnées du bouton

    def show_button_play(self):
        txt_key = 'load_game'
        txt = self.screen.language_manager.load_txt('play_chose', txt_key)
        self.buttons(txt_key, txt, 1, self.dic_buttons)

    def show_button_settings(self):
        txt_key = 'new_game'
        txt = self.screen.language_manager.load_txt('play_chose', txt_key)
        self.buttons(txt_key, txt, 2, self.dic_buttons)

    def show_button_back(self):
        txt_key = 'back'
        txt = self.screen.language_manager.load_txt('play_chose', txt_key)
        self.buttons(txt_key, txt, 11, self.dic_buttons)


class ConfirmResetGame:

    def __init__(self, screen):
        self.screen = screen
        self.dic_buttons = {}  # stock les coordonnées des bouttons

    def update_screen(self):
        self.show_background()
        self.show_title()
        self.show_buttons()

    def show_background(self):
        background_path = self.screen.utils.get_path_assets("pause_menu\pause_menu_bg.jpg")
        background = pygame.image.load(background_path)
        background = self.screen.transform_img(background, self.screen.display_width)
        self.screen.blit_ressource(background, (0, 0))

    def show_title(self):
        title = self.screen.language_manager.load_txt('confirm_reset_game', 'title')
        title2 = self.screen.language_manager.load_txt('confirm_reset_game', 'title2')
        self.screen.draw_txt(title, 70, (0, 50), True, (255, 255, 255), True)
        self.screen.draw_txt(title2, 75, (0, 100), True, (255, 255, 255), True)

    def show_buttons(self):
        self.show_button_confirm_chose()
        self.show_button_cancel_chose()

    def buttons(self, txt_key, txt, button_number, dic):
        y = 100+50*button_number
        txt_surface, position = self.screen.draw_txt(txt, 50, (0, y), True, (255, 255, 255), True)
        x, y, w, h = position
        button_position = x -10, y-10, w + 10, h + 10
        dic[txt_key] = button_position  # Stockez les coordonnées du bouton

    def show_button_confirm_chose(self):
        txt_key = 'confirm'
        txt = self.screen.language_manager.load_txt('confirm_reset_game', txt_key)
        self.buttons(txt_key, txt, 5, self.dic_buttons)

    def show_button_cancel_chose(self):
        txt_key = 'cancel'
        txt = self.screen.language_manager.load_txt('confirm_reset_game', txt_key)
        self.buttons(txt_key, txt, 6, self.dic_buttons)


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
        path = self.screen.utils.get_path_assets('bg_fight.jpeg')
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
        x, y = 960, 640
        for txt in action:
            path = self.screen.utils.get_path_assets(f'action_player/{txt}.png')
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (75, 75))
            image_rect = image.get_rect()
            image_rect.topleft = (x, y)

            self.screen.blit_ressource(image, (x, y))
            x += 80

            self.append_txt_surface_rect(image_rect)

    def player_hud_fight(self, action):
        energy_position = (20, 648)
        life_position = (20, 671)
        xp_position = (20, 694)
        self.screen.show_life_player(life_position)
        self.screen.show_xp_player(xp_position)
        self.screen.show_energy_player(energy_position)
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
        path = self.screen.utils.get_path_assets('inventory\inventory_background.png')
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
        path = self.screen.utils.get_path_assets(f"Game_Over.png")
        image = pygame.image.load(path)
        self.screen.blit_ressource(image)

    def show_txt(self, cause, number_image):
        self.show_txt_death(cause, number_image)
        self.show_exit_txt()

    def show_txt_death(self, cause, number_image):
        txt_key = f"{cause}_{number_image}"
        txt = self.screen.language_manager.load_txt("game_over", txt_key)
        self.screen.draw_txt(txt, 45, (0, 200), True, (255, 255, 255), True) # affiche le txt a l'écran avec une police de 30 et en x=centre, y=200

    def show_exit_txt(self):
        txt_key_button = "press_space"
        txt_key_exit = 'exit'
        txt = f"{self.screen.language_manager.load_txt('button_press', txt_key_button)} {self.screen.language_manager.load_txt('message_system', txt_key_exit)}"
        self.screen.draw_txt(txt, 50, (0, 650), True, (255, 255, 255), True) # affiche le txt a l'écran avec une police de 50 et en x=centre, y=650



class VictoryScreen:

    def __init__(self, screen, loots=None, enemy_fight=None, xp_won=None):
        self.screen = screen
        self.dic_buttons = {} 

        self.loots = loots
        self.enemy_fight = self.screen.language_manager.load_txt(enemy_fight.key_name, 'name')
        self.xp_won = xp_won

        self.random_victory_txt = random.randint(0, 9) # génère un nombre pour choisir aléatoirement quel texte choisir

    def buttons(self, txt_key, txt, button_number, dic):
        y = 100+50*button_number
        txt_surface, position = self.screen.draw_txt(txt, 50, (0, y), True, (255, 255, 255), True)
        x, y, w, h = position
        button_position = x -10, y-10, w + 10, h + 10
        dic[txt_key] = button_position  # Stockez les coordonnées du bouton

    def show_elements(self):
        self.show_background()
        self.show_title()
        self.random_victory()
        self.show_enemy_death()
        self.show_object_won()
        self.show_xp_won()
        self.show_exit()

    def show_background(self):
        background_path = self.screen.utils.get_path_assets("pause_menu\pause_menu_bg.jpg")
        background = pygame.image.load(background_path)
        background = self.screen.transform_img(background, self.screen.display_width)
        self.screen.blit_ressource(background, (0, 0))

    def show_title(self):
        title = self.screen.language_manager.load_txt('victory', 'title')
        self.screen.draw_txt(title, 70, (0, 50), True, (255, 255, 255), True)

    def random_victory(self):
        txt_key = f"victory{self.random_victory_txt}"
        txt = self.screen.language_manager.load_txt('victory', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 2, self.dic_buttons)

    def show_enemy_death(self):
        txt_key = f"enemy_death"
        txt = self.screen.language_manager.load_txt('victory', txt_key)
        txt = f"{txt} {self.enemy_fight}"
        self.screen.pause_menu.buttons(txt_key, txt, 4, self.dic_buttons)

    def show_object_won(self):
        if self.loots: # vérifie si la liste est vide
            txt_key = "object_won"
        else:
            txt_key = 'not_object_won'

        txt = self.screen.language_manager.load_txt('victory', txt_key)

        for loot in self.loots:
            txt_object = self.screen.language_manager.load_txt("objects", loot[0].name)

            txt = f"{txt} {loot[1]} {txt_object}"

        self.screen.pause_menu.buttons(txt_key, txt, 5, self.dic_buttons)

    def show_xp_won(self):
        txt_key = "xp_won"
        txt = self.screen.language_manager.load_txt('victory', txt_key)
        txt = f"{txt} {self.xp_won}xp"
        self.screen.pause_menu.buttons(txt_key, txt, 6, self.dic_buttons)

    def show_exit(self):
        txt_key = "exit"
        txt = self.screen.language_manager.load_txt('victory', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 11, self.dic_buttons)



class Dialog:

    def __init__(self, screen):
        self.screen = screen

    def show_name_box(self, name):
        self.name = name
        self.show_background()
        self.show_txt()

    def show_background(self):
        # affiche la box avec la bonne dimention 
        self.txt_rect, self.text = self.calculate_weight()
        box_img = pygame.image.load(self.screen.utils.get_path_assets('dialog/dialog_box.png'))
        box_img = pygame.transform.scale(box_img, (self.txt_rect.width + 40, 35))
        self.screen.blit_ressource(box_img, (self.txt_rect.x, self.txt_rect.y))

    def calculate_weight(self) -> tuple:
        font = pygame.font.Font(None, 40)
        text = font.render(self.name, True, (0, 0, 0))
        txt_rect = text.get_rect()
        txt_rect.x = 315
        txt_rect.y = 570
        return txt_rect, text

    def show_txt(self):
        rect = self.txt_rect.x + 20, self.txt_rect.y + 4
        self.screen.blit_ressource(self.text, rect)

    def show_launch_dialog_txt(self):
        # Gère l'affichage du texte
        position = (0, 675)
        txt = self.screen.language_manager.load_txt('npc', 'launch_dialog')
        texte_surface, texte_position = self.screen.draw_txt(txt, police=30, position=position, color=(0, 0, 0), can_blit=False)

        texte_width, texte_height = texte_surface.get_size()
        image_size = texte_width + 20, texte_height + 5

        # Gère l'affichage du fond
        background_path = self.screen.utils.get_path_assets("dialog\dialog_box.png")
        image = pygame.image.load(background_path)
        image = pygame.transform.scale(image, image_size)
        image_position = texte_position[0] - 10, texte_position[1] - 5

        # Affiche le texte et le fond
        self.screen.blit_ressource(image, image_position)
        self.screen.blit_ressource(texte_surface, texte_position)




class Tutorial:
    def __init__(self, screen):
        self.screen = screen

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
        background_path = self.screen.utils.get_path_assets("pause_menu\pause_menu_bg.jpg")
        background = pygame.image.load(background_path)
        background = self.screen.transform_img(background, self.screen.display_width)
        self.screen.blit_ressource(background, (0, 0))

    def show_title(self):
        title = self.screen.language_manager.load_txt('pause_menu', 'title')
        self.screen.draw_txt(title, 70, (0, 50), True, (255, 255, 255), True)

    def show_buttons(self):
        self.show_quest_button()
        self.show_button_settings()
        self.show_button_tutorial()
        self.show_button_back_to_the_game()
        self.show_button_save_and_quit()

    def buttons(self, txt_key, txt, button_number, dic):
        y = 100+50*button_number
        txt_surface, position = self.screen.draw_txt(txt, 50, (0, y), True, (255, 255, 255), True)
        x, y, w, h = position
        button_position = x -10, y-10, w + 10, h + 10
        dic[txt_key] = button_position  # Stockez les coordonnées du bouton

    def show_quest_button(self):
        txt_key = 'quest_button'
        txt = self.screen.language_manager.load_txt('pause_menu', txt_key)
        self.buttons(txt_key, txt, 1, self.dic_buttons)

    def show_button_settings(self):
        txt_key = 'settings_button'
        txt = self.screen.language_manager.load_txt('pause_menu', txt_key)
        self.buttons(txt_key, txt, 2, self.dic_buttons)

    def show_button_tutorial(self):
        txt_key = 'tutorial_button'
        txt = self.screen.language_manager.load_txt('pause_menu', txt_key)
        self.buttons(txt_key, txt, 3, self.dic_buttons)

    def show_button_back_to_the_game(self):
        txt_key = 'back_to_the_game'
        txt = self.screen.language_manager.load_txt('pause_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 9, self.dic_buttons)

    def show_button_save_and_quit(self):
        txt_key = 'save_and_quit_button'
        txt = self.screen.language_manager.load_txt('pause_menu', txt_key)
        self.buttons(txt_key, txt, 11, self.dic_buttons)





class Tutorial_Menu:

    def __init__(self, screen):
        self.screen = screen
        self.dic_buttons = {}  # stock les coordonnées des bouttons

    def show_tutorial(self):
        self.show_background()
        self.show_title()
        self.show_buttons()

    def show_background(self):
        self.screen.pause_menu.show_background()

    def show_title(self):
        title = self.screen.language_manager.load_txt('tutorial_menu', 'title')
        self.screen.draw_txt(title, 70, (0, 50), True, (255, 255, 255), True)

    def show_buttons(self):
        self.show_button_back()

    def show_button_back(self):
        txt_key = 'back'
        txt = self.screen.language_manager.load_txt('tutorial_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 11, self.dic_buttons)





class Quest:

    def __init__(self, screen):
        self.screen = screen
        self.dic_buttons = {}  # stock les coordonnées des bouttons

    def show_elements(self):
        self.show_background()
        self.show_title()
        self.show_quests()
        self.show_button_back()

    def show_background(self):
        self.screen.pause_menu.show_background()

    def show_title(self):
        title = self.screen.language_manager.load_txt('quest_menu', 'title')
        self.screen.draw_txt(title, 70, (0, 50), True, (255, 255, 255), True)

    def show_quests(self):
        y_offset = 100  # Décalage vertical initial pour le premier élément de quête

        for quest in self.screen.game.active_quests:
            quest_name = self.screen.language_manager.load_txt(quest.name, 'title')
            quest_text = f"{quest_name} - {quest.progression}/{quest.objectif}"
            txt_surface, position = self.screen.draw_txt(quest_text, 50, (0, 0), True, (255, 255, 255), True, False)
            position.topleft = (position[0], y_offset)  # Position de la quête sur l'écran
            self.screen.screen.blit(txt_surface, position)  # Affichage de la quête sur l'écran
            y_offset += 50

    def show_button_back(self):
        txt_key = 'back'
        txt = self.screen.language_manager.load_txt('quest_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 11, self.dic_buttons)








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
        title = self.screen.language_manager.load_txt('settings_menu', 'title')
        self.screen.draw_txt(title, 70, (0, 50), True, (255, 255, 255), True)

    def show_buttons(self):
        self.show_button_language()
        self.show_button_game_settings()
        self.show_button_back()

    def show_button_language(self):
        txt_key = 'language'
        txt = self.screen.language_manager.load_txt('settings_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 1, self.dic_buttons)

    def show_button_game_settings(self):
        txt_key = 'game_settings'
        txt = self.screen.language_manager.load_txt('settings_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 2, self.dic_buttons)

    def show_button_back(self):
        txt_key = 'back'
        txt = self.screen.language_manager.load_txt('settings_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 11, self.dic_buttons)




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
        title = self.screen.language_manager.load_txt('settings_languages_menu', 'title')
        self.screen.draw_txt(title, 70, (0, 50), True, (255, 255, 255), True)

    def show_buttons(self):
        self.show_button_language_english()
        self.show_button_language_french()
        self.show_button_language_spanish()
        self.show_button_back()

    def show_button_language_english(self):
        txt_key = 'english'
        txt = self.screen.language_manager.load_txt('languages', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 1, self.dic_buttons)

    def show_button_language_french(self):
        txt_key = 'french'
        txt = self.screen.language_manager.load_txt('languages', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 2, self.dic_buttons)

    def show_button_language_spanish(self):
        txt_key = 'spanish'
        txt = self.screen.language_manager.load_txt('languages', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 3, self.dic_buttons)

    def show_button_back(self):
        txt_key = 'back'
        txt = self.screen.language_manager.load_txt('settings_languages_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 11, self.dic_buttons)


class GameSettingsMenu:

    def __init__(self, screen):
        self.screen = screen
        self.dic_buttons = {}  # stock les coordonnées des bouttons

    def show_elements(self):
        self.show_background()
        self.show_title()
        self.show_buttons()

    def show_background(self):
        self.screen.pause_menu.show_background()

    def show_title(self):
        title = self.screen.language_manager.load_txt('game_settings_menu', 'title')
        self.screen.draw_txt(title, 70, (0, 50), True, (255, 255, 255), True)

    def show_buttons(self):
        self.show_button_auto_save()
        self.show_button_back()

    def show_button_auto_save(self):
        txt_key = 'auto_save'
        txt = self.screen.language_manager.load_txt('game_settings_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 1, self.dic_buttons)

    def show_button_back(self):
        txt_key = 'back'
        txt = self.screen.language_manager.load_txt('game_settings_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 11, self.dic_buttons)


class AutoSaveMenu:

    def __init__(self, screen):
        self.screen = screen
        self.dic_buttons = {}  # stock les coordonnées des bouttons

    def show_elements(self):
        self.show_background()
        self.show_title()
        self.show_buttons()

    def show_background(self):
        self.screen.pause_menu.show_background()

    def show_title(self):
        title = self.screen.language_manager.load_txt('auto_save_menu', 'title')
        self.screen.draw_txt(title, 70, (0, 50), True, (255, 255, 255), True)

    def show_buttons(self):
        self.show_button_2min()
        self.show_button_5min()
        self.show_button_10min()
        self.show_button_15min()
        self.show_button_30min()
        self.show_button_1h()
        self.show_button_desactivated()
        self.show_actualy_time()
        self.show_button_back()

    def show_button_2min(self):
        txt_key = '2min'
        txt = self.screen.language_manager.load_txt('auto_save_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 1, self.dic_buttons)

    def show_button_5min(self):
        txt_key = '5min'
        txt = self.screen.language_manager.load_txt('auto_save_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 2, self.dic_buttons)

    def show_button_10min(self):
        txt_key = '10min'
        txt = self.screen.language_manager.load_txt('auto_save_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 3, self.dic_buttons)

    def show_button_15min(self):
        txt_key = '15min'
        txt = self.screen.language_manager.load_txt('auto_save_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 4, self.dic_buttons)

    def show_button_30min(self):
        txt_key = '30min'
        txt = self.screen.language_manager.load_txt('auto_save_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 5, self.dic_buttons)

    def show_button_1h(self):
        txt_key = '1h'
        txt = self.screen.language_manager.load_txt('auto_save_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 6, self.dic_buttons)

    def show_button_desactivated(self):
        txt_key = 'desactivated'
        txt = self.screen.language_manager.load_txt('auto_save_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 7, self.dic_buttons)

    def show_actualy_time(self):
        txt_key = "actualy_time"
        txt = self.screen.language_manager.load_txt('auto_save_menu', txt_key)
        txt = f"{txt} {self.screen.game.format_time}"
        self.screen.pause_menu.buttons(txt_key, txt, 9, self.dic_buttons)

    def show_button_back(self):
        txt_key = 'back'
        txt = self.screen.language_manager.load_txt('auto_save_menu', txt_key)
        self.screen.pause_menu.buttons(txt_key, txt, 11, self.dic_buttons)