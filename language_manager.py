import pygame

class LanguageManager:

    def __init__(self):
        self.load_language('en') # initie la langue par defaut

    def load_txt(self, page, txt):
        return self.current_language.translations[page][txt]

    def load_language(self, lang):
        if lang == 'en':
            import translation.english as new_language
            str_new_language = "en"
        elif lang == 'fr':
            import translation.french as new_language
            str_new_language = "fr"
        elif lang == 'es':
            import translation.spanish as new_language
            str_new_language = "es"

        self.current_language, self.str_language = new_language, str_new_language