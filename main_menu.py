import pygame
from game import Game
from screen import Screen
from pause_menu import Settings_Menu

class MainMenu:

    def __init__(self):
        self.game = Game()
        self.screen = Screen(self.game)
        self.settings_menu = Settings_Menu(self.game)

        self.defaut_language = "fr"
        self.game.load_language(self.defaut_language)

    def running(self):
        self.running = True

        while self.running:
            self.screen.main_menu.update_screen()
            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.QUIT:
                    self.running = False

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
                        self.running = False