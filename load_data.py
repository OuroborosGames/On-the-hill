import json
from collections import OrderedDict
from game_errors import ParserError


# those functions are used by the game to initialize its state
def get_initial_buildings():
    return _parse_json_data('buildings.json') + _get_hardcoded_buildings()


def get_basic_random_events():
    return _parse_json_data('events.json') + _get_hardcoded_events()


def get_basic_special_actions():
    return _parse_json_data('actions.json') + _get_hardcoded_actions()


# those internal functions handle data files
def _parse_json_data(filename):
    #return _dict_to_game_objects(json.load(filename, object_hook=OrderedDict))
    with open(filename) as f:
        return _dict_to_game_objects(json.load(f, object_hook=OrderedDict))


def _dict_to_game_objects(data_dict, filename=""): # filename only used to report errors
    if (len(data_dict) != 1) or ('contents' not in data_dict.keys()):
        raise ParserError(filename + "is not a valid OTH data file")
    return _parse_recursively(data_dict['contents'])


def _parse_recursively(data):
    # TODO: maybe actually parse the fucking data
    print(data)
    ret = []
    for d in data:
        print(d)
    return ret

# those internal functions are used to define more complex objects
# (basically, if you see no reasonable way of creating something with data files, create it here)
def _get_hardcoded_buildings():
    return []


def _get_hardcoded_events():
    return []


def _get_hardcoded_actions():
    return []
