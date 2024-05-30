import pygame
import screen

class Victory:

    def __init__(self, game, current_enemy):
        self.game = game
        self.current_enemy = current_enemy

    def give_enemy_loot(self):
        self.xp_won = self.game.data_player.get_xp(self.current_enemy.give_xp)
        self.loots = self.current_enemy.loot_enemy()
        object_loot = self.loots[0](self.game)
        self.object_name = object_loot.name
        self.number_loot = self.loots[1]
        self.game.inventory.append_object(object_loot, self.number_loot)

    def running(self):
        self.run = True

        self.give_enemy_loot()
        self.victory_screen = screen.VictoryScreen(self.game.screen, self.object_name, self.number_loot, self.current_enemy, self.xp_won)

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