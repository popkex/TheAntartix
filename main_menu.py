import pygame
from game import Game
from screen import Screen
from pause_menu import Settings_Menu

class MainMenu:

    def __init__(self):
        self.game = Game(self)
        self.screen = Screen(self.game)
        self.settings_menu = Settings_Menu(self.game)

        self.defaut_language = "fr"
        self.game.load_language(self.defaut_language)

    def show_lunch_game(self):
        self.screen.screen.fill((0, 0, 0))
        self.screen.main_menu.show_logo()

    def running(self):
        self.run = True

        self.show_lunch_game()

        while self.run:
            self.screen.main_menu.update_screen()
            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.QUIT:
                    self.run = False

        pygame.quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.screen.main_menu.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == 'play_button':
                        self.game.running()

                    elif txt == 'settings_button':
                        self.settings_menu.running()

                    elif txt == 'quit_button':
                        self.run = False