import pygame, sys, os

class DialogBox:

    x_position = 290
    y_position = 590

    def __init__(self):
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
    def execute(self, dialog=['erreur dans le chargement du dialogue']):
        if self.can_execute: # evite qu'il se lance 2fois (j'ai pas trouver pourquoi)
            if self.reading:
                self.next_text()
            else:
                self.reading = True
                self.txt_index = 0
                self.txts = dialog
            self.can_execute = False

    def render(self, screen):
        self.can_execute = True
        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.txts[self.txt_index]):
                self.letter_index = self.letter_index

            screen.blit(self.box, (self.x_position, self.y_position))
            
            # Séparer le texte en lignes
            lines = self.txts[self.txt_index].split('\n')
            y_offset = 10  # Ajustez cette valeur pour l'espacement vertical entre les lignes

            # Rendre chaque ligne séparément
            for line in lines:
                txt = self.font.render(line[0:self.letter_index], False, (0, 0, 0))
                screen.blit(txt, (self.x_position + 50, self.y_position + y_offset))
                y_offset += 20

    def next_text(self):
        self.txt_index += 1
        self.letter_index = 0

        if self.txt_index >= len(self.txts):
            # ferme le dialogue
            self.reading = False