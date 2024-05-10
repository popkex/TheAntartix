import pygame

class Pause_Menu:

    def __init__(self, game):
        self.game = game
        self.settings_menu = Settings_Menu(game)
        self.quest = Quest(game)

    def running(self):
        running = True

        while running:

            # Affiche l'écran de menu de pause
            self.game.screen.pause_menu.show_pause()

            #actualise l'écran
            self.game.update_screen()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()


    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.game.screen.pause_menu.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == 'quest_button':
                        self.quest.running()

                    if txt == 'settings_button':
                        self.settings_menu.running()

                    if txt == 'save_and_quit_button':
                        self.game.saves.save_and_quit()

class Quest:

    def __init__(self, game):
        self.game = game

    def running(self):
        running = True

        while running:
            self.game.screen.quest.show_elements()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

class Settings_Menu():
    def __init__(self, game):
        self.game = game
        self.settings_language = Settings_language(game)

    def running(self):
        running = True

        while running:
            self.game.screen.settings.show_settings()

            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.game.screen.settings.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == 'language':
                        self.settings_language.running()


class Settings_language:
    def __init__(self, game):
        self.game = game

    def running(self):
        running = True

        while running:
            self.game.screen.settings_languages.show_settings_languages()

            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.game.screen.settings_languages.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == 'english':
                        self.game.load_language('en')

                    elif txt == 'french':
                        self.game.load_language('fr')

                    elif txt == 'spanish':
                        self.game.load_language('es')