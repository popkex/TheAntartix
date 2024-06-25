import json

class DataMap:
    def __init__(self, map_name):
        with open(r"data_maps.json", 'r') as f:
            data = json.load(f)

        self.data = data.get(map_name, {})