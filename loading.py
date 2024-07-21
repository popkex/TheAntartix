import pygame

class LoadingScreen:

    def __init__(self, screen, paths_img_list):
        self.screen = screen.screen
        paths_list = []
        for path in paths_img_list:
            img = screen.utils.get_path_assets(path)
            paths_list.append(img)

        paths_img_list = paths_list

        self.images = [pygame.image.load(path) for path in paths_img_list]
        self.current_image = 0
        self.last_update_time = 0
        self.update_interval = 200

    def show_element(self, message=""):
        self.screen.fill((0, 0, 0))
        self.display_image()
        self.display_message(message)
        pygame.display.flip()
        pygame.time.delay(100)

    def display_image(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.update_interval:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.last_update_time = current_time

        self.screen.blit(self.images[self.current_image], (0, 0))

    def calculate_position_message(self, message=""):
        size_screen = self.screen.get_size()
        size_message = message.get_size()
        position = (size_screen[0] - size_message[0] - 20, size_screen[1] - size_message[1] - 20)
        return (position)

    def display_message(self, message):
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, (255, 255, 255))
        position = self.calculate_position_message(message=text)
        self.screen.blit(text, position)

    def complete(self):
        self.show_element("Loading complete")

class Loading:

    def __init__(self, game, paths_img_list=[]):
        self.game = game
        self.loading_screen = LoadingScreen(game.screen, paths_img_list)

    def execut(self):
        self.loading_screen.show_element("Starting loading...")
