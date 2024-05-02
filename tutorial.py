import pygame

class Tutorial:

    def __init__(self, game):
        self.game = game
        self.dic_tutorial = {} # se défini quand on load si le fichier existe pas

    def running(self, message):
        running = True

        while running:

            # actualise l'écran
            self.game.screen.tutorial.show_tutorial(message)

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.screen.tutorial.clear_tutorial()
                        running = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()