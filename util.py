import sys
import os

class Utils:
    def __init__(self):
        self.fps_limite = 60
        self.delta_time = 0.0
        self.gravity = 1

    def get_path_assets(self, ressource):
        exe_assets_path = r'TA-datas\\assets'

        if os.path.exists(exe_assets_path):
            return f'{exe_assets_path}\\{ressource}'
        else:
            return f'assets\\{ressource}'

    def get_path_saves(self, ressource):
        exe_saves_path = 'TA-datas\\saves'

        if os.path.exists(exe_saves_path):
            return f'{exe_saves_path}\\{ressource}'
        else:
            return f'saves\\{ressource}'

    def get_path_utils(self, ressource):
        exe_utils_path = 'TA-datas\\utils'

        if os.path.exists(exe_utils_path):
            return f'{exe_utils_path}\\{ressource}'
        else:
            return f'utils\\{ressource}'
