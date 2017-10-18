from oth_core.text_events import *

# TODO everything
BRANCH_NAME = ""


def get_random_events():
    return []


def get_nonrandom_events():
    return []


def is_mid_game(state):
    return state.branch == BRANCH_NAME


class MidGameEvent(ConditionalEvent):
    """A class for random events that can only happen in the mid game"""

    def __init__(self, name, description, actions, condition=None):
        super().__init__(name, description, actions, condition)
        if condition is not None:
            self.should_be_activated = lambda state: \
                (condition(state)) and (is_mid_game(state))
        else:
            self.should_be_activated = is_mid_game
