import pygame

class Tutorial:

    def __init__(self, game):
        self.game = game
        self.dic_tutorial = {} # se défini quand on load si le fichier existe pas

    def running(self, tutorial):
        running = True
        key_txt = 'tutorials', tutorial
        key_name_txt = "tutorials", "tutorial"
        self.game.dialog_box.execute(key_txt, key_name_txt)
        self.clock = pygame.time.Clock()

        while running:
            # actualise l'écran
            self.game.dialog_box.render(self.game.screen.screen, "tutorial")

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = self.game.dialog_box.execute(key_txt, key_name_txt)

                    if event.key == pygame.K_RETURN:
                        self.game.dialog_box.close_dialog()
                        running = False

                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()  

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

        self.game.screen.tutorial.clear_tutorial()