import json
from collections import OrderedDict


# those functions are used by the game to initialize its state
def get_initial_buildings():
    return _parse_json_data('buildings.json') + _get_hardcoded_buildings()


def get_basic_random_events():
    return _parse_json_data('events.json') + _get_hardcoded_events()


def get_basic_special_actions():
    return _parse_json_data('actions.json') + _get_hardcoded_actions()


# those internal functions handle data files
def _parse_json_data(filename):
    return _dict_to_game_objects(json.load(filename, object_hook=OrderedDict))


def _dict_to_game_objects(data_dict):
    # TODO: actually create game objects
    return []


# those internal functions are used to define more complex objects
# (basically, if you see no reasonable way of creating something with data files, create it here)
def _get_hardcoded_buildings():
    return []


def _get_hardcoded_events():
    return []


def _get_hardcoded_actions():
    return []
