from oth_core.text_events import *

"""This is the module for all the bad stuff that happens when your stats get too low"""
# TODO everything


def get_disasters():
    return []


class Disaster(ConditionalEvent):

    def __init__(self, name, description, actions, stat, counterval, threshold):
        self.stat = stat
        self.threshold = threshold
        counterstat = "disaster_" + stat
        # those events will fire when an associated counter reaches a certain value...
        super().__init__(name, description, actions, lambda state: counter_greater(state, counterstat, counterval))
        # ...and they'll reset the counter afterwards, so you won't get the same events each turn
        self.chain_unconditionally(lambda state: state.counter.reset(counterstat))

    def _is_disaster_over(self, state):
        return attr_greater(state, self.stat, self.threshold)
