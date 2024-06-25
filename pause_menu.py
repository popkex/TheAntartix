import pygame
from language_manager import LanguageManager

class Pause_Menu:

    def __init__(self, game):
        self.game = game
        self.settings_menu = Settings_Menu(game)
        self.quest = Quest(game)
        self.tutorial_menu = Tutorial_Menu(game)

    def running(self):
        self.run = True

        while self.run:

            # Affiche l'écran de menu de pause
            self.game.screen.pause_menu.show_pause()

            #actualise l'écran
            self.game.update_screen()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.game.screen.pause_menu.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == 'quest_button':
                        self.quest.running()

                    elif txt == 'settings_button':
                        self.settings_menu.running()

                    elif txt == 'tutorial_button':
                        self.tutorial_menu.running()

                    elif txt == 'back_to_the_game':
                        self.run = False

                    elif txt == 'save_and_quit_button':
                        self.game.saves.save_and_quit()

class Quest:

    def __init__(self, game):
        self.game = game

    def running(self):
        self.run = True

        while self.run:
            self.game.screen.quest.show_elements()

            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.game.screen.quest.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == 'back':
                        self.run = False

class Settings_Menu():
    def __init__(self, game):
        self.game = game
        self.settings_language = Settings_language(game)
        self.game_settings = GameSettings(game)

    def running(self):
        self.run = True

        while self.run:
            self.game.screen.settings.show_settings()

            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.game.screen.settings.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == 'language':
                        self.settings_language.running()

                    elif txt == 'game_settings':
                        self.game_settings.running()

                    elif txt == 'back':
                        self.run = False

class Settings_language:
    def __init__(self, game):
        self.game = game
        self.language_manager = self.game.language_manager

    def running(self):
        self.run = True

        while self.run:
            self.game.screen.settings_languages.show_settings_languages()

            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.game.screen.settings_languages.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == 'english':
                        self.language_manager.load_language('en')

                    elif txt == 'french':
                        self.language_manager.load_language('fr')

                    elif txt == 'spanish':
                        self.language_manager.load_language('es')

                    elif txt == 'back':
                        self.run = False


class Tutorial_Menu():
    def __init__(self, game):
        self.game = game

    def running(self):
        self.run = True

        while self.run:
            self.game.screen.tutorial_menu.show_tutorial()

            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.game.screen.tutorial.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == 'back':
                        self.run = False


class GameSettings:

    def __init__(self, game):
        self.game = game
        self.auto_save = AutoSave(game)

    def running(self):
        self.run = True

        while self.run:
            self.game.screen.game_settings_menu.show_elements()

            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.game.screen.game_settings_menu.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == "auto_save":
                        self.auto_save.running()

                    elif txt == 'back':
                        self.run = False


class AutoSave:

    def __init__(self, game):
        self.game = game

    def running(self):
        self.run = True

        while self.run:
            self.game.screen.auto_save_menu.show_elements()

            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.game.screen.auto_save_menu.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == '1min':
                        self.game.time_auto_save = 60
                        self.game.format_time = "1minute"
                    elif txt == '2min':
                        self.game.time_auto_save = 120
                        self.game.format_time = "2minutes"
                    elif txt == '5min':
                        self.game.time_auto_save = 300
                        self.game.format_time = "5minutes"
                    elif txt == '10min':
                        self.game.time_auto_save = 600
                        self.game.format_time = "10minutes"
                    elif txt == '15min':
                        self.game.time_auto_save = 900
                        self.game.format_time = "15minutes"
                    elif txt == '30min':
                        self.game.time_auto_save = 1800
                        self.game.format_time = "30minutes"
                    elif txt == '1h':
                        self.game.time_auto_save = 3600
                        self.game.format_time = "1heure"
                    elif txt == 'desactivated':
                        self.game.time_auto_save = False
                        self.game.format_time = "Désactivé"
                    elif txt == 'back':
                        self.run = False