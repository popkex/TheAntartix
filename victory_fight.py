import pygame, random
import screen

class Victory:

    def __init__(self, game, current_enemy):
        self.game = game
        self.current_enemy = current_enemy

    def get_object_won(self, loot):
        objects_won = []

        for objet in loot:
            number = random.randint(0, objet[1]) # génère un nombre entre 0 et le nombre d'objet max possible avec se mob

            if not number == 0:
                self.game.inventory.append_object(objet[0](self.game), number)
                objects_won.append((objet[0](self.game), number))

        return objects_won 

    def give_enemy_loot(self):
        self.xp_won = self.game.data_player.get_xp(self.current_enemy.give_xp)
        self.loots = self.current_enemy.loot_enemy()

        self.loots = self.get_object_won(self.loots)

    def running(self):
        self.run = True

        self.give_enemy_loot()
        self.victory_screen = screen.VictoryScreen(self.game.screen, self.loots, self.current_enemy, self.xp_won)

        while self.run:
            self.victory_screen.show_elements()

            pygame.display.flip()

            for event in pygame.event.get():
                self.handle_mouse_click(event)
                
                if event.type == pygame.KEYDOWN:
                    self.run = False

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for txt, button_position in self.victory_screen.dic_buttons.items():
                rect = pygame.Rect(button_position)
                if rect.collidepoint(event.pos):
                    if txt == 'exit':
                        self.run = False