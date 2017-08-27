from oth_core.text_events import *


def get_random_events():
    return []


def get_nonrandom_events():
    return []


def is_early_game(state):
    return state.branch.startswith("The Founding of ")


class EarlyGameEvent(ConditionalEvent):
    """A class for random events that can only happen during the early game"""
    def __init__(self, name, description, actions, condition=None):
        super().__init__(name, description, actions, condition)
        if condition is not None:
            self.should_be_activated = lambda state:\
                (self.should_be_activated(state)) and (is_early_game(state))
        else:
            self.should_be_activated = is_early_game
