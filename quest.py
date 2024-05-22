class Quest:

    def __init__(self, game, name=None, type=None, objectif=None, rewards=None, rewards_quantity=None, key_description=None):
        self.game = game
        self.name = name
        self.type = type
        self.progression = 0
        self.objectif = objectif
        self.rewards = rewards
        self.rewards_quantity = rewards_quantity
        self.key_description = key_description
        self.state = False # False pour non completer

    def reset_all_quests(self):
        self.game.active_quests = []

    def add_quest(self, name, type, objectif, rewards, rewards_quantity, key_description):
        if len(self.game.active_quests) <= 5:
            existing_quest = None

            # Vérifie si une quête avec le même nom est déjà active
            for quest in self.game.active_quests:
                if quest.name == name:
                    existing_quest = quest
                    break

            if existing_quest:
                # Mettre à jour la quête existante
                existing_quest.type = type
                existing_quest.objectif = objectif
                existing_quest.rewards = rewards
                existing_quest.rewards_quantity = rewards_quantity
                existing_quest.key_description = key_description
            else:
                # Ajouter une nouvelle quête
                new_quest = Quest(self.game, name, type, objectif, rewards, rewards_quantity, key_description)
                self.game.active_quests.append(new_quest)

    def check_quest_progress(self, type, number=1):
        for quest in self.game.active_quests:
            if quest.type == type:
                quest.progress_quest(number)

    def quest_type_exist(self, quest_name):
        for quest in self.game.active_quests:
            if quest.type == quest_name:
                return True
        return False

    def all_quests_data(self):
        quests_caracteres = []

        for quest in self.game.active_quests:
            data = (quest.name, quest.type, quest.objectif, quest.rewards.__class__.__name__, quest.rewards_quantity, quest.key_description, quest.progression)
            quests_caracteres.append(data)

        return quests_caracteres

    def is_completed(self):
        return self.state

    def progress(self, quest_type, progress):
        if self.game.can_modifie_quest:
            for quest in self.game.active_quests:
                if quest.type == quest_type:
                    quest.progression += progress

                    # Vérifier si la quête est complétée
                    if quest.progression >= quest.objectif:
                        quest.complete()

                    break

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