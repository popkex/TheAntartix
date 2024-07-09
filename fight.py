import pygame, random
from screen import Screen
from victory_fight import Victory
from fight_entity import *
from language_manager import LanguageManager

class Fight:

    def __init__(self, game, enemy):
        self.screen = Screen(game)
        self.game = game

        self.language_manager = LanguageManager()

        self.is_player_action = True
        self.player_selected_object = False

        self.current_enemy = enemy

        self.first_turn = True
        self.can_modifie_replay_luck = True

    # Vérifie si il reste des entités en vie
    def entity_is_alive(self) -> bool:
        return self.game.fight_player.is_alive() and self.current_enemy.is_alive()

    def reset_life(self):
        self.game.data_player.health = self.game.data_player.max_health / 2

    def kill_player(self):
        self.reset_life()
        self.game.data_player.remove_xp()
        self.player_death()

    def check_all_quest(self):
        if self.game.quest.quest_type_exist('kill_enemy'):
            self.game.quest.progress('kill_enemy', 1)
        if self.game.quest.quest_type_exist(f'kill_{self.current_enemy.name}'):
            self.game.quest.progress(f'kill_{self.current_enemy.name}', 1)

    def who_win(self):
        self.game.player.change_animation('up')

        # si le joueur gagne
        if self.game.fight_player.is_alive() and not self.current_enemy.is_alive():
            self.check_all_quest()

            Victory(self.game, self.current_enemy).running()

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
                        self.game.map_manager.reload_map()

                if event.type == pygame.QUIT:
                    self.game.saves.save_and_quit()

    def player_turn(self):
        if not self.entity_can_play_again('enemy'):
            self.is_player_action = self.game.fight_player.turn()
        else:
            self.is_player_action = False
            message = self.language_manager.load_txt('message_system', 'enemy_known_out_player')
            self.game.add_message(message)

    def ia_turn(self):
        if not self.entity_can_play_again('player'):
            pygame.time.delay(500)
            self.is_player_action = self.current_enemy.turn(self.game)
        else:
            self.is_player_action = True
            message = self.language_manager.load_txt('message_system', 'player_known_out_enemy')
            self.game.add_message(message)

    def entity_can_play_again(self, turn_entity):
        if self.can_modifie_replay_luck:
            can_replay_luck = random.randint(0, 100)
            self.can_modifie_replay_luck = False
        else:
            can_replay_luck = 101 # met la valeur au dessus du seuille possible pour empecher de rejouer (et de crash)

        if turn_entity == 'player' and can_replay_luck <= self.game.data_player.knock_out_luck:
            self.can_modifie_replay_luck = True
            return True

        elif turn_entity == 'enemy' and can_replay_luck <= self.current_enemy.knock_out_luck:
            self.can_modifie_replay_luck = True
            return True

        return False

# Gère le système de tour par tour
    def turn_management(self):
        if not self.first_turn:
            # si c'est au joueur de jouer
            if self.is_player_action:
                self.player_turn()
            # si c'est a l'enemie de jouer
            elif self.current_enemy.is_alive():
                self.ia_turn()

        else:
            self.player_turn()
            self.first_turn = self.is_player_action

#le combat
    def run(self):
        self.game.fight_player.reset_energy()
        message = self.current_enemy.lanch_fight_message
        self.game.add_message(message, 15)

        while self.game.active_fight:
            #affiche l'écran de fight
            self.screen.fight_display.screen_fight(self.game.fight_player.txt_player_action)

            # lance le tuto et le désactive une fois que l'utilisateur le quitte
            ## le laisser dans la boucle meme si c'est mal opti sinon l'écran reste noir lors du tuto
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