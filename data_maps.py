import json
from utils import Utils

class DataMap:
    def __init__(self, map_name):
        with open(Utils().get_path_utils(r"data_maps.json"), 'r') as f:
            data = json.load(f)

        self.data = data.get(map_name, {})