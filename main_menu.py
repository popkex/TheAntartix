import pygame
from game import Game
from screen import Screen
from saves import Saves
from pause_menu import Settings_Menu
from loading import Loading

def start_game_loading(self):
    paths_img_list = ["assets\enemy\enemyA.gif", "assets\mobilier.png", "assets\player.png"]
    loading = Loading(self, paths_img_list)
    loading.execut()
    self.game = Game(self, loading)
    self.game.running()

class MainMenu:

    def __init__(self):
        self.game = Game(self)
        self.screen = Screen(self.game)
        self.settings_menu = Settings_Menu(self.game)
        self.saves = Saves(self.game)
        self.play_chose = PlayChose(self.game, self.screen, self.saves)
        self.saves.load_settings()

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
                    self.saves.save_settings()
                    self.run = False

        pygame.quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.screen.main_menu.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == 'play_button':
                        self.play_chose.running()

                    elif txt == 'settings_button':
                        self.settings_menu.running()

                    elif txt == 'quit_button':
                        self.run = False

class PlayChose:

    def __init__(self, game, screen, saves):
        self.game = game
        self.screen = screen
        self.saves = saves

        self.confirm_reset_game = ConfirmResetGame(self.game, self.screen, self.saves)

    def running(self):
        self.run = True

        while self.run:
            self.screen.play_chose.update_screen()
            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.QUIT:
                    self.run = False

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.screen.play_chose.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == 'load_game':
                        start_game_loading(self)

                    elif txt == 'new_game':
                        self.confirm_reset_game.running()

                    elif txt == 'back':
                        self.run = False

class ConfirmResetGame:

    def __init__(self, game, screen, saves):
        self.game = game
        self.screen = screen
        self.saves = saves

    def running(self):
        self.run = True

        while self.run:
            self.screen.confirm_reset_game.update_screen()
            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_mouse_click(event)

                if event.type == pygame.QUIT:
                    self.saves.save_and_quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.screen.confirm_reset_game.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == 'confirm':
                        self.saves.reset_game()
                        start_game_loading(self)

                    elif txt == 'cancel':
                        self.run = False