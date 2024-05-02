import pygame

class Tutorial:

    def __init__(self, game):
        self.game = game

    def running(self, message):
        running = True

        while running:

            # actualise l'écran
            self.game.screen.tutorial.show_tutorial(message)
            self.game.update_screen()

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()