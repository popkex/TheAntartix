# utils.py
import os
import sys

class PathUtils:
    @staticmethod
    def get_path_assets(resource):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, "assets", resource)

    @staticmethod
    def get_path_saves(resource=None, folder_path=False):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        if not folder_path:
            return os.path.join(base_path, "saves", resource)
        else:
            return os.path.join(base_path, "saves")
