import json
from collections import OrderedDict


def get_initial_buildings():
    return parse_json_data('buildings.json')


def get_basic_random_events():
    return parse_json_data('events.json')


def get_basic_special_actions():
    return parse_json_data('actions.json')


def parse_json_data(filename):
    return dict_to_game_objects(json.load(filename, object_hook=OrderedDict))


def dict_to_game_objects(data_dict):
    # TODO: actually create game objects
    pass
