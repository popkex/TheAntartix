import pygame, random
from screen import Screen
from fight_entity import *

class Fight:

    def __init__(self, game, enemy):
        self.screen = Screen(game)
        self.game = game

        self.is_player_action = True
        self.player_selected_object = False

        self.current_enemy = enemy

        self.first_turn = True

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

            if self.game.quest.quest_type_exist('kill_enemy'):
                self.game.quest.progress('kill_enemy', 1)

        # si le joueur perd
        elif not self.game.fight_player.is_alive():
            self.kill_player()

        # retire l'ennemie courrant
        self.current_enemy = None

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

    def player_turn(self):
        if not self.entity_can_play_again('enemy'):
            self.is_player_action = self.game.fight_player.turn()
        else:
            self.is_player_action = False

    def ia_turn(self):
        if not self.entity_can_play_again('player'):
            pygame.time.delay(500)
            self.is_player_action = self.current_enemy.turn(self.game)
        else:
            self.is_player_action = True

    def entity_can_play_again(self, turn_entity):
        can_replay = random.randint(0, 100)
        if turn_entity == 'player' and can_replay <= self.game.data_player.knock_out_luck:
            return True

        elif turn_entity == 'enemy' and can_replay <= self.current_enemy.knock_out_luck:
            return True

# Gère le système de tour par tour
    def turn_management(self):
        if not self.first_turn:
            # si c'est au joueur de jouer
            if self.is_player_action:
                self.player_turn()
            # si il peut rejouer
            elif self.is_player_action:
                self.player_turn()
                '''
                mettre un message disant que le joueur a assomé l'enemie
                '''

            # si c'est a l'enemie de jouer
            elif self.current_enemy.is_alive():
                self.ia_turn()
            # si il peut rejouer
            else:
                self.ia_turn()
                '''
                mettre un message disant que le joueur a assomé l'enemie
                '''
        else:
            self.player_turn()
            self.first_turn = self.is_player_action

            print(self.first_turn)

#le combat
    def run(self):
        message = self.current_enemy.lanch_fight_message
        self.game.add_message(message, 15)

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
                    self.game.saves.save_and_quit()

        self.who_win()