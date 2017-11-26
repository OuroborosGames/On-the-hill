from oth_core.text_events import *

"""This is the module for all the bad stuff that happens when your stats get too low"""
# TODO everything


def get_disasters():
    return [famine]


class Disaster(ConditionalEvent):
    """Do not use this directly, it's just for that threshold classvariable. Use either Basic or Lazy version depending
    on what you need."""

    thresholds = []

    def __init__(self, name, description, actions, stat, threshold_getter, consecutive_turns_to_trigger):
        self.stat = stat
        counter_name = "disaster_" + stat
        # those events will fire when an associated counter reaches a certain value...
        super().__init__(name, description, actions, lambda state: counter_greater(state, counter_name,
                                                                                   consecutive_turns_to_trigger))
        # ...and they'll reset the counter afterwards, so you won't get the same events each turn
        self.chain_unconditionally(lambda state: state.counter.reset(counter_name))
        # this is for the game state to know what counters to use, what stat to check and how to do it
        self.thresholds.append((stat, threshold_getter, counter_name))


class BasicDisaster(Disaster):
    """Those disaster evaluate the stat threshold eagerly, although in an roundabout and overengineered way (we actually
    make a function that always return a provided value). If this sounds like overcomplicated bullshit then you're
    right, and there's probably a better way to do it (although I can't think of one that also allows the lazy version
    below).

    TL;DR is: use this class if the disaster counter gets incremented when a stat falls below a certain constant
    value (e.g. health is lower than 0)."""

    def __init__(self, name, description, actions, stat, threshold, consecutive_turns_to_trigger):
        super().__init__(name, description, actions, stat, lambda state: threshold, consecutive_turns_to_trigger)


class LazyDisaster(Disaster):
    """This time, we make a function that evaluates threshold lazily. This is useful when the disaster happens if
    one stat is lower than other stat ('reference_stat') for a few turns - e.g. when there's less food than people
    to feed."""
    def __init__(self, name, description, actions, stat, reference_stat, consecutive_turns_to_trigger):
        super().__init__(name, description, actions, stat, lambda state: getattr(state, reference_stat, 0),
                         consecutive_turns_to_trigger)

famine = LazyDisaster(
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
    reference_stat='population',
    consecutive_turns_to_trigger=3
)
