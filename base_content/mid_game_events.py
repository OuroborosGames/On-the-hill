from oth_core.text_events import *
from oth_core.buildings import BasicBuilding

"""This module is for events that can happen in the mid-game or from mid-game onwards. Events should have bigger
possible disadvantages and bigger rewards, the advisors should unlock new buildings and special actions while also
giving advice and we should have a few small event chain with more plot than before. Also, weird stuff (preferably
subtly weird and never explained too much) should start happening."""


BRANCH_NAME = "Uncertain but Hopeful"


def get_random_events():
    return [mansion_event]


def get_nonrandom_events():
    return []


def is_mid_game(state):
    return state.branch == BRANCH_NAME


class MidGameEvent(ConditionalEvent):
    """A class for random events that can only happen in the mid game"""

    def __init__(self, name, description, actions, condition=None):
        super(MidGameEvent, self).__init__(name, description, actions, condition)
        if condition is not None:
            self.should_be_activated = lambda state: \
                (condition(state)) and (is_mid_game(state))
        else:
            self.should_be_activated = is_mid_game


mansion = BasicBuilding(
    name="Mansion",
    description="This large and expensive house with more bedrooms than there are rooms in most apartments is home to rich people and those who work for them. Its architecture might not be the most functional, but it's aesthetic enough to make its surroundings seem more exclusive than they really are.",
    base_price=2000,
    additional_effects={'prestige': 4, 'population_max': 7},
    per_turn_effects={'money': -300}
)

mansion_event = UnlockableEvent(
    name="Attracting the right crowd",
    description=
    """According to Peter Ponzi, your city has enough money to start making even more money
    - and this can be done by attracting more citizens, which is best achieved by first attracting
    a few rich citizens. After you repeatedly ask him for a more straightforward explanation,
    you learn that this was just an overly complicated way of making the city invest in expensive
    and impractical houses conveniently designed by an architect who just happens to be his cousin.
    Apparently, rich people love them.""",
    actions={'OK': lambda state: unlock_building(state, mansion)},
    unlock_predicate=lambda state:attr_greater(state, 'money', 2000)
)
