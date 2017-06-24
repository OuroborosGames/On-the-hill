from random import randint

from . import timers_and_counters

"""Module for text-based/CYOA events."""

"""Text event interface consists of:
        title, description - I don't have to explain those, do I?
        get_actions() - returns a list of possible player choices
        perform_action(action, state) - perform an action identified by the first parameter (must be one of the elements
                                        returned by get_actions()) on the game state passed as the second one
        should_be_activated(state) - a predicate; if it returns true, the event will become active (which means it can
                                     be spawned if it's a random event and that it will be spawned immediately if it's
                                     a non-random one; no effect on events spawned immediately by other events or
                                     special actions) #TODO: non-random events in game state
        should_be_deactivated(state) - if it returns true, the event will become inactive; this means that a random
                                       event cannot be spawned and it has no effect on any other events"""


class TextEventPrototype(object):
    def __init__(self):
        self.title = "Test event"
        self.description = "Something happens"
        self._actions = {'OK': lambda state: None}
        self.should_be_activated = lambda state: True
        self.should_be_deactivated = lambda state: False

    def get_actions(self):
        ret = []
        for action in self._actions:
            ret.append(action)
        return ret

    def perform_action(self, action, state):
        return self._actions[action](state)


class BasicEvent(TextEventPrototype):
    def __init__(self, name, description, actions):
        super(BasicEvent, self).__init__()
        self.title = name
        self.description = description
        self.actions = actions

    def chain_unconditionally(self, *functions):
        """This method makes all the actions in this event perform an additional action; useful for chaining events
        together"""
        for k in self.actions.keys():
            v = self.actions[k]

            def new_action(state):
                v(state)
                for function in functions:
                    function(state)

            self.actions[k] = new_action
        return self


class UnlockableEvent(BasicEvent):
    def __init__(self, name, description, actions, unlock_predicate):
        super(UnlockableEvent, self).__init__(name, description, actions)
        self.should_be_activated = unlock_predicate


class ConditionalEvent(BasicEvent):
    def __init__(self, name, description, actions, condition):
        super(ConditionalEvent, self).__init__(name, description, actions)
        self.should_be_activated = condition
        self.should_be_deactivated = lambda state: not condition(state)


def get_basic_random_events():
    return [TextEventPrototype(), TextEventPrototype(), TextEventPrototype()]


# a bunch of horrible functions (should have been lambdas) that will be useful for data-driven object creation

# horrible mutators (use for actions)
def spawn_immediately(state, event):
    state._event_queue.append(event)


def add_active_event(state, event):
    state._event_active_deck.append(event)


def add_inactive_event(state, event):
    state._event_inactive_deck.append(event)


def spawn_after_n_turns(state, event, n):
    state.timers.append(timers_and_counters.BasicEventTimer(n, event))


def spawn_next_season(state, event, season):  # winter = 0, spring = 1, summer = 2, autumn = 3
    current_month = (state.turn % 12) + 1
    if season == 0:
        season_start = 12
    else:
        season_start = season * 3
    to_season_start = (season_start - current_month % 12) + 1
    # return (to_season_start + randint(0, 2)) % 12
    spawn_after_n_turns(state, event, (to_season_start + randint(0, 2)) % 12)


def modify_state(state, attributes):
    for attr in attributes:
        setattr(state, attr, getattr(state, attr) + attributes[attr])


def unlock_building(state, building):
    state.buildings_deck.append(building)


def unlock_action(state, action):
    state.special_actions.append(action)


def set_flag(state, flag):
    state.flags.set(flag)


def unset_flag(state, flag):
    state.flags.unset(flag)


# horrible predicates (use for lock/unlock conditions)
def counter_equal(state, key, value):
    return _counter_predicate(state, key, value, lambda x, y: x == y)


def counter_greater(state, key, value):
    return _counter_predicate(state, key, value, lambda x, y: x > y)


def counter_lower(state, key, value):
    return _counter_predicate(state, key, value, lambda x, y: x < y)


def attr_equal(state, key, value):
    return _attribute_predicate(state, key, value, lambda x, y: x == y)


def attr_greater(state, key, value):
    return _attribute_predicate(state, key, value, lambda x, y: x > y)


def attr_lower(state, key, value):
    return _attribute_predicate(state, key, value, lambda x, y: x < y)


def flag_isset(state, flag):
    return state.flags.isset(flag)


def flag_isunset(state, flag):
    return not flag_isset(state, flag)


def _counter_predicate(state, counter_key, value, func):
    if func(state.counter.get_count(counter_key), value):
        return True
    return False


def _attribute_predicate(state, attr, value, func):
    if func(getattr(state, attr), value):
        return True
    return False
