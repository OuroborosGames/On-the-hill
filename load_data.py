import json
from collections import OrderedDict

def parse_json_data(filename):
    return dict_to_game_objects(json.load(filename, object_hook=OrderedDict))

def dict_to_game_objects(data_dict):
    # TODO: actually create game objects
    pass