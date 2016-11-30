import json
import text_events
import buildings
import special_actions
from collections import OrderedDict
from game_errors import ParserError
from functools import partial


# those functions are used by the game to initialize its state
def get_initial_buildings():
    return _parse_json_data('buildings.json') + _get_hardcoded_buildings()


def get_basic_random_events():
    return _parse_json_data('events.json') + _get_hardcoded_events()


def get_basic_special_actions():
    return _parse_json_data('actions.json') + _get_hardcoded_actions()


# those internal functions handle data files
def _parse_json_data(filename):
    # return _dict_to_game_objects(json.load(filename, object_hook=OrderedDict))
    with open(filename) as f:
        return _dict_to_game_objects(json.load(f, object_hook=OrderedDict))


def _dict_to_game_objects(data_dict, filename=""):  # filename only used to report errors
    if (len(data_dict) != 1) or ('contents' not in data_dict.keys()):
        raise ParserError(filename + "is not a valid OTH data file")
    ret = []
    for d in data_dict['contents']:
        ret.append(_parse_recursively(d))
    return ret


# I'm a bit ashamed because this parser is really horrible
def _parse_recursively(data):
    if isinstance(data, OrderedDict):
        if 'event_title' in data.keys():
            if (len(data)) == 3:
                return text_events.BasicEvent(data['event_title'], data['description'],
                                              _parse_recursively(data['actions']))
            if 'unlock_predicate' in data.keys():
                return text_events.UnlockableEvent(data['event_title'], data['description'],
                                                   _parse_recursively(data['actions']),
                                                   _parse_recursively(data['unlock_predicate']))
            return text_events.ConditionalEvent(data['event_title'], data['description'],
                                                _parse_recursively(data['actions']),
                                                _parse_recursively(data['condition']))
        if 'building_name' in data.keys():
            if len(data.keys()) == 5:
                return buildings.BasicBuilding(data['building_name'], data['description'], data['base_price'],
                                               data['additional_effects'], data['per_turn_effects'])
            if 'required_tile' in data.keys():
                return buildings.TerrainRestrictedBuilding(data['building_name'], data['description'],
                                                           data['base_price'], data['additional_effects'],
                                                           data['per_turn_effects'], data['required_tile'])
            return buildings.CustomBuilding(data['building_name'], data['description'], data['base_price'],
                                            data['additional_effects'], data['per_turn_effects'],
                                            _parse_recursively(data['build_predicate']))
        if 'name' in data.keys():
            if len(data.keys()) == 3:
                return special_actions.SpecialAction(data['name'], data['description'],
                                                     _parse_recursively(data['event']))
            return special_actions.LimitedSpecialAction(data['name'], data['description'],
                                                        _parse_recursively(data['event']), data['limit'])
        return partial(getattr(text_events, data['predicate']), key=data['key'], value=data['value'])
    if isinstance(data, list):
        ret = {}
        for d in data:
            # print(d['name'])
            if 'event_to_create' in d['effect']:
                if (len(d['effect'])) == 1:
                    # print(d['effect']['event_to_create'])
                    ret.update({d['name']: partial(text_events.spawn_immediately,
                                                   event=_parse_recursively(d['effect']['event_to_create']))})
                elif 'turns' in d['effect']:
                    ret.update({d['name']: partial(text_events.spawn_after_n_turns,
                                                   event=_parse_recursively(d['effect']['event_to_create']),
                                                   turns=d['effect']['turns'])})
                elif 'season' in d['effect']:
                    ret.update({d['name']: partial(text_events.spawn_next_season,
                                                   event=_parse_recursively(d['effect']['event_to_create']),
                                                   season=d['effect']['season'])})
                elif d['effect']['active']:
                    ret.update({d['name']: partial(text_events.add_active_event,
                                                   event=_parse_recursively(d['effect']['event_to_create']))})
                else:
                    ret.update({d['name']: partial(text_events.add_inactive_event,
                                                   event=_parse_recursively(d['effect']['event_to_create']))})
            elif 'building_to_unlock' in d['effect']:
                ret.update(
                    {d['name']: partial(text_events.unlock_building, building=d['effect']['building_to_unlock'])})
            elif 'action_to_unlock' in d['effect']:
                ret.update({d['name']: partial(text_events.unlock_action,
                                               action=_parse_recursively(d['effect', 'action_to_unlock']))})
            elif 'attributes_to_apply' in d['effect']:
                ret.update(({d['name']: partial(text_events.modify_state,
                                                attributes=d['effect']['attributes_to_apply'])}))
            else:
                ret.update({d['name']: lambda state: None})
        return ret
    # print(getattr(buildings, data))
    return getattr(buildings, data)


# those internal functions are used to define more complex objects
# (basically, if you see no reasonable way of creating something with data files, create it here)
def _get_hardcoded_buildings():
    return []


def _get_hardcoded_events():
    return []


def _get_hardcoded_actions():
    return []
