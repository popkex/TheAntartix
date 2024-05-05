class Quest:

    def __init__(self, game, name=None, objectif=None, rewards=None, rewards_quantity=None):
        self.game = game
        self.name = name
        self.progression = 0
        self.objectif = objectif
        self.rewards = rewards
        self.rewards_quantity = rewards_quantity
        self.state = False # False pour non completer

    def add_quest(self, name, objectif, rewards, rewards_quantity):
        can_add_quest = True

        #vérifie dans toute les quests si celle qu'on essaye d'ajouter existe ou non
        for quest in self.game.active_quests:
            if quest.name == name:
                can_add_quest = False

        if can_add_quest:
            self.name = name  # Mettre à jour le nom de la quête
            self.objectif = objectif  # Mettre à jour l'objectif
            self.rewards = rewards  # Mettre à jour les récompenses
            self.rewards_quantity = rewards_quantity  # Mettre à jour les quantités des récompenses
            self.game.active_quests.append(self) 

    def is_completed(self):
        return self.state

    def add_progress(self, quest_name, progress):
        for quest in self.game.active_quests:
            if quest.name == quest_name:
                quest.progress(progress)
                break
            else:
                self.progression = progress
                self.progress(progress)

    def progress(self, name, progress):
        for quest in self.game.active_quests:
            if quest.name == name:
                quest.progression += progress

                if quest.progression >= quest.objectif:
                    quest.complete()

    def complete(self):
        self.remove_quest(self.name)
        self.receved_rewards()
        self.state = True # True pour completer

    def remove_quest(self, quest_name):
        # Recherchez la quête dans la liste des quêtes actives
        for quest in self.game.active_quests:
            if quest.name == quest_name:
                self.game.active_quests.remove(quest)
                break

    def receved_rewards(self):
        self.game.inventory.append_object(self.rewards, self.rewards_quantity)