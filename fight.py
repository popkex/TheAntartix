import pygame, random
from screen import Screen
from entity import *

class Fight:

    def __init__(self, game):
        self.screen = Screen(game)
        self.game = game

        self.is_player_action = True
        self.player_selected_object = False

        #choisi un enemie aléatoirement
        enemy_list = [EnemyA(game), EnemyB(game)]
        self.current_enemy = random.choice(enemy_list)

    # Vérifie si il reste des entités en vie
    def entity_is_alive(self) -> bool:
        return self.game.fight_player.is_alive() and self.current_enemy.is_alive()

    def reset_life(self):
        self.game.data_player.health = self.game.data_player.max_health / 2

    def give_enemy_loot(self):
        self.game.data_player.get_xp(self.current_enemy.give_xp)
        loots = self.current_enemy.loot_enemy()
        object_loot = loots[0](self.game)
        number_loot = loots[1]
        self.game.inventory.append_object(object_loot, number_loot)

    def kill_player(self):
        self.reset_life()
        self.game.data_player.remove_xp()
        self.player_death()

    def who_win(self):
        self.game.player.change_animation('up')

        # si le joueur gagne
        if self.game.fight_player.is_alive() and not self.current_enemy.is_alive():
            self.give_enemy_loot()
        # si le joueur perd
        elif not self.game.fight_player.is_alive():
            self.kill_player()

    def player_death(self):
        running = True
        number_image = random.randint(1, 10)
        while running:
            self.game.screen.death_display.show_death("fight_message", number_image)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        running = False
                        self.game.map_manager.teleport_player_with_name('player_spawn')

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

# Gère le système de tour par tour
    def turn_management(self):
        #laisse le joueur/l'ia faire le tour chaqu'un leurs tours
        if self.is_player_action:
            self.is_player_action = self.game.fight_player.turn()
        elif self.current_enemy.is_alive():
            pygame.time.delay(500)
            self.is_player_action = self.current_enemy.turn(self.game)
            pygame.time.delay(500)

#le combat
    def run(self):
        while self.game.active_fight:
            #affiche l'écran de fight
            self.screen.fight_display.screen_fight(self.game.fight_player.txt_player_action)

            # lance le tuto et le désactive une fois que l'utilisateur le quitte
            if not self.game.tutorial.dic_tutorial['fight']:
                self.game.tutorial.running('tuto_fight')
                self.game.tutorial.dic_tutorial['fight'] = True

            self.game.update_screen()

            self.game.active_fight = self.entity_is_alive()

            self.turn_management()

            pygame.display.flip()
            self.game.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.saves.game.save_and_quit()

        self.who_win()