import pygame, sys, os

class DialogBox:

    descr_x_position = 290
    descr_y_position = 590

    def __init__(self, game):
        self.game = game
        self.name = "???"
        self.box = pygame.image.load(self.get_path_assets('dialog/dialog_box.png'))
        self.box = pygame.transform.scale(self.box, (700, 100))
        self.txts = ['salut', 'oki', 'ok']
        self.txt_index = 0
        self.letter_index = 0
        font_path = self.get_path_assets('font/dialog_font.ttf')
        self.font = pygame.font.Font(font_path, 18)
        self.reading = False
        self.can_execute = True

    def get_path_assets(self, ressource):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, "assets") + "\\" + ressource


    # traduire l'erreur
    def execute(self, key_txt, name=None, quest=None) -> bool:
        self.name = name
        page, txt = key_txt
        dialog = self.game.load_txt(page, txt)

        # regarde si un nom est donner 
        if name:
            page, txt = name
            self.name = self.game.load_txt(page, txt)
        else:
            self.name = "???"

        if self.can_execute: # evite qu'il se lance 2fois (j'ai pas trouver pourquoi)
            if self.reading:
                self.next_text(quest)
            else:
                self.reading = True
                self.txt_index = 0
                self.txts = dialog

            self.can_execute = False

        return self.reading

    def close_dialog(self):
        self.reading = False
        self.letter_index = 0
        self.txt_index = 0
        self.can_execute = True

    def render(self, screen, origin="world"):
        self.can_execute = True

        if self.game.map_manager.check_player_far_npc() and origin != "tutorial":
            self.close_dialog()
            self.reading = False

        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.txts[self.txt_index]):
                self.letter_index = self.letter_index

            # affiche la box avec les dialogs dedans
            screen.blit(self.box, (self.descr_x_position, self.descr_y_position))
            self.game.screen.dialog.show_name_box(self.name)

            # Séparer le texte en lignes
            lines = self.txts[self.txt_index].split('\n')
            y_offset = 20  # l'emplacement y de la position la plus haute pour le premier txt

            # Rendre chaque ligne séparément
            for line in lines:
                txt = self.font.render(line[0:self.letter_index], False, (0, 0, 0))
                screen.blit(txt, (self.descr_x_position + 45, self.descr_y_position + y_offset))
                y_offset += 20

    def next_text(self, quest=None):
        self.txt_index += 1
        self.letter_index = 0

        if self.txt_index >= len(self.txts):

            if quest:
                name, type, objectif, rewards, rewards_quantity, key_description = quest
                self.game.quest.add_quest(name, type, objectif, rewards, rewards_quantity, key_description)

            # ferme le dialogue
            self.reading = False