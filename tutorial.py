import pygame

class Tutorial:

    def __init__(self, game):
        self.game = game
        self.dic_tutorial = {} # se défini quand on load si le fichier existe pas

    def running(self, tutorial):
        running = True
        key_txt = 'tutorials', tutorial
        self.game.dialog_box.execute(key_txt)
        self.clock = pygame.time.Clock()

        while running:
            # actualise l'écran
            self.game.dialog_box.render(self.game.screen.screen)

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = self.game.dialog_box.execute(key_txt)

                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

        self.game.screen.tutorial.clear_tutorial()