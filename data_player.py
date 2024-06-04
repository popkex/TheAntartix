from inventory import *

class Data_Player:
    def __init__(self, game):
        self.game = game
        self.health = None
        self.max_health = None
        self.attack = None
        self.crit_luck = None
        self.crit_domage = None
        self.knock_out_luck = None
        self.luck_fail_attack = None
        self.xp = None
        self.xp_max = None
        self.lvl = None

    def load_attributes(self):
        data_1, data_2, data_3 = self.game.saves.load_attribut_player()
        self.health, self.max_health, self.attack = data_1
        self.crit_luck, self.crit_domage, self.knock_out_luck, self.luck_fail_attack = data_2
        self.xp, self.xp_max, self.lvl = data_3

# si le joueur gagne de l'exp
    def get_xp(self, give_xp):
        self.xp = int(self.xp + give_xp)
        while self.xp >= self.xp_max:
            self.xp = self.xp - self.xp_max 
            self.lvl_up()
        return give_xp

    def lvl_up(self):
        self.lvl += 1
        self.increase_xp()
        self.new_player_property()

    def new_player_property(self):
        self.max_health = int(self.max_health*1.1)
        self.health = self.max_health
        self.attack = int(self.attack*1.1)

    def increase_xp(self):
        self.xp_max = (self.xp_max*1.25)

# si le joueur perd de l'exp
    def remove_xp(self):
        if self.lvl > 1:
            if int(self.xp_max/1.5) < 1:
                self.xp = int(self.xp_max/1.1)
            else:
                self.lvl_down()
        else:
            if int(self.xp_max/1.5) < 1:
                self.xp = int(self.xp_max/1.1)
            else:
                self.xp = 0

    def lvl_down(self):
        self.lvl -= 1
        self.xp_max = int(self.xp_max/1.25)
        self.xp = int(self.xp_max/1.5)