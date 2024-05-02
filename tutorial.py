import pygame

class Tutorial:

    def __init__(self, game):
        self.game = game

    def running(self):
        running = True

        while running:

            # actualise l'écran
            self.game.screen.tutorial.show_tutorial()
            self.game.update_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.save_and_quit()