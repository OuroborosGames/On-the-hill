from oth_core.text_events import *

"""This module is for events that can happen in the mid-game or from mid-game onwards. Events should have bigger
possible disadvantages and bigger rewards, the advisors should unlock new buildings and special actions while also
giving advice and we should have a few small event chain with more plot than before. Also, weird stuff (preferably
subtly weird and never explained too much) should start happening."""


# TODO everything
BRANCH_NAME = "Uncertain but Hopeful"


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
