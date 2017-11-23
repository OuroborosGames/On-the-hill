from oth_core.text_events import *

"""This is the module for all the bad stuff that happens when your stats get too low"""
# TODO everything


def get_disasters():
    return [famine]


class Disaster(ConditionalEvent):

    def __init__(self, name, description, actions, stat, counterval):
        self.stat = stat
        counterstat = "disaster_" + stat
        # those events will fire when an associated counter reaches a certain value...
        super().__init__(name, description, actions, lambda state: counter_greater(state, counterstat, counterval))
        # ...and they'll reset the counter afterwards, so you won't get the same events each turn
        self.chain_unconditionally(lambda state: state.counter.reset(counterstat))

famine = Disaster(
    name="Famine",
    description=
    """The food shortages your city was suffering from have now turned into a disastrous
    famine. Many people have already died of starvation and many more are barely surviving
    without food. The ones who didn't lose all their strength are either protesting outside
    of the city hall or just trying to steal something even remotely edible.""",
    actions={
        'Do nothing': lambda state: modify_state(state, {'safety': -5, 'health': -3, 'prestige': -2}),
        'Implement food rationing': lambda state: modify_state(state, {'food': state.food/2, 'prestige': -3}),
        'Buy as much as you can afford and give to the people': lambda state: modify_state(
            state, {'food': min(state.population, state.money), 'money': -state.money})
    },
    stat='food',
    counterval=3
)
