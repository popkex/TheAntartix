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
            message = "Tu as attaqué !"
            self.game.add_message(message)
            self.game.update_screen()
        return False

    def player_escape(self):
        luck = random.randint(0, 100)
        # Le joueur a 20% de chance d'échouer à la fuite du combat 
        if luck <= 0: #de base 85
            self.game.active_fight = False
        else:
            message = "Tu n'as pas réussi a t'échapper"
            self.game.add_message(message)
            self.game.update_screen()
            # self.game.screen.system_message(message)
        return False

    def player_choose_object(self) -> bool:
        if not self.game.fight.player_selected_object:
            return self.game.inventory.open_inventory(self.game, "fight")

# Détécte sur quoi le joueur clique et lance l'action séléctionné
    def turn(self) -> bool:
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
                self.game.save_and_quit()
        return True