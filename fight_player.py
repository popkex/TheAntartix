import pygame, random

class Fight_Player():
    def __init__(self, game):
        self.game = game
        self.enemy = game.fight.current_enemy
        self.player = game.data_player
        self.player_action_rects = []
        self.txt_player_action = ["sword", "item", "escape"]
        self.player_action_fonction = [
            self.player_attack,
            self.player_choose_object, 
            self.player_escape,
        ]

    def select_action_player(self, index):
        return self.player_action_fonction[index]()

    def is_alive(self):
        return self.player.health != 0

    def player_attack(self):
        if self.enemy.health > self.player.attack:
            self.enemy.health -= self.player.attack
        else: 
            self.enemy.health = 0

        message = self.game.load_txt('message_system', 'player_attack')
        self.game.add_message(message)
        self.game.update_screen()

        return False

    def player_escape(self):
        luck = random.randint(0, 100)

        # Le joueur a 15% de chance d'échouer à la fuite du combat 
        if luck <= 85: #de base 85
            self.game.active_fight = False
        else:
            message = self.game.load_txt('message_system', 'failed_escape')
            self.game.add_message(message)
            self.game.update_screen()

        return False

    def player_choose_object(self) -> bool:
        if not self.game.fight.player_selected_object:
            return self.game.inventory.open_inventory(self.game, "fight")

# Détécte sur quoi le joueur clique et lance l'action séléctionné
    def turn(self) -> bool:
        self.game.update_screen()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                index = 0
                for rect in self.player_action_rects:
                    if rect.collidepoint(event.pos):
                        return self.select_action_player(index)
                    index += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return self.player_choose_object()

                elif event.key == pygame.K_a:
                    return self.player_attack()

                elif event.key == pygame.K_ESCAPE:
                    return self.player_escape()

            if event.type == pygame.QUIT:
                self.game.saves.save_and_quit()
        return True