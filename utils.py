import sys, os

class Utils:

    def __init__(self):
        self.fps_limite = 60
        self.delta_time = 0.0
        self.gravity = 1

# permet de retrouver le chemin d'acces vers les assets lors de la compilation du jeu
    def get_path_assets(self, ressource):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, "assets") + "\\" + ressource

# permet de retrouver le chemin d'acces vers les saves lors de la compilation du jeu
    def get_path_saves(self, ressource=any, folder_path=False):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        if not folder_path:
            return os.path.join(base_path, "saves") + "\\" + ressource
        else:
            return os.path.join(base_path, "saves")

    def get_path_utils(self, ressource=any, folder_path=False):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        if not folder_path:
            return os.path.join(base_path, "dir_utils") + "\\" + ressource
        else:
            return os.path.join(base_path, "dir_utils")