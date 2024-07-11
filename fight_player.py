import pygame, random

class Fight_Player():
    def __init__(self, game):
        self.game = game
        self.language_manager = game.language_manager
        self.enemy = game.fight.current_enemy
        self.player = game.data_player
        self.player_action_rects = []
        self.txt_player_action = ["sword", 'shield', "item", "escape"]
        self.player_action_fonction = [
            self.player_attack,
            self.player_defense,
            self.player_choose_object, 
            self.player_escape,
        ]

    def can_remove_energy(self, quantity_removed):
        if self.game.data_player.energy - quantity_removed >= 0: # si la quantité restante est en gros de plus de 0
            return True
        return False

    def remove_energy(self, quantity_removed):
        new_quantity = self.game.data_player.energy - quantity_removed

        if new_quantity >= 1:
            self.game.data_player.energy = new_quantity
        else:
            self.game.data_player.energy = 0

    def add_energy(self, quantity_add):
        new_quantity = self.game.data_player.energy + quantity_add

        if new_quantity > self.game.data_player.energy_max:
            self.game.data_player.energy = self.game.data_player.energy_max
        else:
            self.game.data_player.energy = new_quantity

    def reset_energy(self):
        self.game.data_player.energy = self.game.data_player.energy_max

    def select_action_player(self, index):
        return self.player_action_fonction[index]()

    def is_alive(self):
        return self.player.health != 0

    def calculate_crit_dommage(self):
        domage = self.player.attack*self.player.crit_domage

        # vérifie si le crit a bien augmenter l'attack 
        if domage == self.player.attack:
            domage += 1

        return domage

    def player_crit(self):
        crit_luck = random.randint(0, 100)

        domage = self.player.attack

        if crit_luck <= self.player.crit_luck:
            domage =  self.calculate_crit_dommage()
            message = self.language_manager.load_txt('message_system', 'player_crit')
        else:
            message = self.language_manager.load_txt('message_system', 'player_attack')

        return domage, message

    def player_fail_attack(self):
        luck_fail = random.randint(0, 100)

        if self.player.luck_fail_attack < luck_fail:
            return False
        return True

    def player_attack(self):
        # si le joueur a encore suffisament d'énergie 
        if self.can_remove_energy(self.game.data_player.energy_consumed_attack):
            if not self.player_fail_attack(): 
                domage, message = self.player_crit()

                if self.enemy.health > domage:
                    self.enemy.health -= domage
                else: 
                    self.enemy.health = 0
            else:
                message = self.language_manager.load_txt('message_system', 'player_fail_attack')

            # retire de l'energie, affiche le message et passe le tour du joueur
            self.remove_energy(self.game.data_player.energy_consumed_attack)
            self.game.add_message(message)
            self.game.update_screen()
            return False
        else:
            # affiche le message et ne passe pas le tour du joueur
            message = self.language_manager.load_txt('message_system', 'player_dont_have_enough_energy_for_attack')
            self.game.add_message(message)
            self.game.update_screen()
            return True

    def player_fail_defense(self):
        luck_fail = random.randint(0, 100)

        # si le joueur ne loupe pas ca défense
        if self.player.luck_fail_defense < luck_fail:
            return False
        # si le joueur loupe ca défense
        return True

    def calculate_sudden_domage(self):
        # calcule des dommage subbit par le joueur en pourcent
        percent_damage = self.enemy.attack*100/self.player.max_health
        new_percent_damage = percent_damage - self.player.defense

        # vérifie que le chiffre est pas négatif
        if new_percent_damage < 0:
            new_percent_damage = 0

        # reconvertie en les pourcents en int (comme avant)
        return percent_damage*self.player.max_health/100

    def player_defense(self):
        if not self.player_fail_defense():
            self.enemy.attack = self.calculate_sudden_domage()
            message = self.language_manager.load_txt('message_system', 'defense')
        else:
            message = self.language_manager.load_txt('message_system', 'fail_defense')

        self.game.add_message(message)
        self.game.update_screen()
        self.add_energy(self.game.data_player.energy_regain_defense)

        return False

    def player_escape(self):
        luck = random.randint(0, 100)

        # Le joueur a 15% de chance d'échouer à la fuite du combat 
        if luck <= 85: #de base 85
            self.game.active_fight = False
        else:
            message = self.language_manager.load_txt('message_system', 'failed_escape')
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
                    return not self.player_choose_object()

                elif event.key == pygame.K_a:
                    return self.player_attack()

                elif event.key == pygame.K_r:
                    return self.player_escape()

                elif event.key == pygame.K_z:
                    return self.player_defense()

            if event.type == pygame.QUIT:
                self.game.saves.save_and_quit()
        return True