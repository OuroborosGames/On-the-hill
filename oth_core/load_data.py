import base_content.early_game_events
import base_content.disasters

"""This module gives us the most important parts of the game: events and buildings. Now it's really just a loader for
data files contained in the base_content and stories packages but it used to contain a truly horrible JSON parser
which created game data from files generated by an even worse JSON generator. Thankfully, I realized that the whole
thing was really fucking bad and decided to just do everything in Python instead of succumbing to the dreaded inner
platform effect."""


# those functions are used by the game to initialize its state
def get_initial_buildings():
    import base_content.buildings
    return base_content.buildings.get_initial_buildings()


def get_basic_random_events():
    return base_content.early_game_events.get_random_events()


def get_basic_special_actions():
    return []


def get_nonrandom_events():
    from base_content.dispatcher_event import DispatcherEvent
    return [DispatcherEvent(_get_stories())]\
        + base_content.early_game_events.get_nonrandom_events()\
        + base_content.disasters.get_disasters()


def get_disaster_thresholds():
    return base_content.disasters.Disaster.thresholds


def _get_stories():
    import pkgutil
    import stories
    ret = []
    for importer, module, ispackage in pkgutil.iter_modules(stories.__path__):
        if not ispackage:
            story = importer.find_module(module).load_module(module)
            ret.append((story.get, story.should_enter_branch))
    return ret
