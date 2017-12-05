from oth_core.text_events import *
from oth_core.game_errors import *
from math import floor
from random import randint

"""This is the module for all the bad stuff that happens when your stats get too low"""


# TODO disasters for low money and pop>maxpop


def get_disasters():
    return [famine, epidemic, riot, forgetting]


class Disaster(ConditionalEvent):
    """Do not use this directly, it's just for that threshold classvariable. Use either Basic or Lazy version depending
    on what you need."""

    thresholds = []

    def __init__(self, name, description, actions, stat, threshold_getter, consecutive_turns_to_trigger):
        if consecutive_turns_to_trigger < 2:
            raise InternalError("Stat should be below threshold for more than 1 turn to trigger a disaster")
        counter_name = "disaster_" + stat
        # those events will fire when an associated counter reaches a certain value...
        super(Disaster, self).__init__(name, description, actions, lambda state: counter_equal(state, counter_name,
                                                                                 consecutive_turns_to_trigger - 1))
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
        super(BasicDisaster, self).__init__(name, description, actions, stat, lambda state: threshold,
                                            consecutive_turns_to_trigger)


class LazyDisaster(Disaster):
    """This time, we make a function that evaluates threshold lazily. This is useful when the disaster happens if
    one stat is lower than other stat ('reference_stat') for a few turns - e.g. when there's less food than people
    to feed."""

    def __init__(self, name, description, actions, stat, reference_stat, consecutive_turns_to_trigger):
        super(LazyDisaster, self).__init__(name, description, actions, stat,
                                           lambda state: getattr(state,reference_stat, 0), consecutive_turns_to_trigger)


famine = LazyDisaster(
    name="Famine",
    description=
    """The food shortages your city was suffering from have now turned into a disastrous
    famine. Many people have already died of starvation and many more are barely surviving
    without food. The ones who didn't lose all their strength are either protesting outside
    of the city hall or just trying to steal something even remotely edible.""",
    actions={'Do nothing': lambda state: modify_state(state, {'safety': -5, 'health': -3, 'prestige': -2}),
             'Implement food rationing': lambda state: modify_state(state, {'food': floor(state.food / 2),
                                                                            'prestige': -3}),
             'Buy as much as you can afford and give to the people': lambda state: modify_state(
                 state, {'food': min(state.population, state.money), 'money': -state.money})},
    stat='food',
    reference_stat='population',
    consecutive_turns_to_trigger=3
)

epidemic = BasicDisaster(
    name="Epidemic",
    description=
    """Whether due to all the dirt and filth that has accumulated in your city or because
    of not enough hospitals and not enough doctors, your city has been struck by a disastrous
    epidemic. Disease is spreading like wildfire and the air smells like death.""",
    actions={'Do nothing': lambda state: modify_state(state, {'health': -5, 'prestige': -4, 'safety': -1}),
             'Quarantine the sick': lambda state: modify_state(state, {'health': 1, 'prestige': -4, 'population': floor(
                 state.population * (state.health / 100))}),
             'Bring doctors from all over the country, regardless of cost': lambda state: modify_state(
                 state, {'population': floor(state.money/500), 'health': min(floor(state.money/1000), -state.health),
                         'money': -state.money})},
    stat='money',
    threshold=-3,
    consecutive_turns_to_trigger=5
)

riot = BasicDisaster(
    name="Riot",
    description=
    """Neither you nor anyone else has any idea what started it, but the violence in your
    city is quickly spiralling out of control. Maybe someone insulted somebody else, then it
    got physical and then friends and friends of friends got involved. Maybe political
    extremists attempted a revolution but then forgot what they're angry about. Or maybe some
    criminals were fighting other criminals and the bystanders were so bored of their normal
    everyday life that they decided that they also want to punch someone in the face.""",
    actions={'Do nothing': lambda state: modify_state(state, {'safety': -5, 'prestige': -5}),
             'Arrest the worst troublemakers': lambda state: modify_state(state, {'safety': -2, 'prestige': -2,
                                                                                  'money': -500}),
             'Fight fire with fire': lambda state: modify_state(state, {'money': -1000, 'population': state.safety*10,
                                                                        'safety': -state.safety, 'prestige': -5})},
    stat='safety',
    threshold=0,
    consecutive_turns_to_trigger=10
)


# removes buildings and/or special actions from player's hand
def forget_random(state):
    to_forget = randint(1, -state.technology)
    buildings = state.buildings_deck
    actions   = state.special_actions

    for _ in to_forget:
        try:
            if randint(0, 1):
                del buildings[randint(0, len(buildings)-1)]
            else:
                del actions[randint(0, len(actions)-1)]
        except (ValueError, IndexError):
            # IndexError is just a sanity check, ValueError = empty range (i.e. we try to del from empty list)
            continue

forgetting = BasicDisaster(
    name="Forgetting",
    description=
    """It seems that due to your city's lack of care for preserving the knowledge, some things
    have been forgotten. Unfortunately, you also forgot what you have forgotten - but you can't
    shake the feeling that you are certainly going to regret it.""",
    actions={'OK': forget_random},
    stat='technology',
    threshold=0,
    consecutive_turns_to_trigger=12
)