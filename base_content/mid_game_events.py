from oth_core.text_events import *
from oth_core.buildings import BasicBuilding

"""This module is for events that can happen in the mid-game or from mid-game onwards. Events should have bigger
possible disadvantages and bigger rewards, the advisors should unlock new buildings and special actions while also
giving advice and we should have a few small event chain with more plot than before. Also, weird stuff (preferably
subtly weird and never explained too much) should start happening."""


BRANCH_NAME = "Uncertain but Hopeful"


def get_random_events():
    return [mansion_event, going_underground]


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
    unlock_predicate=lambda state: attr_greater(state, 'money', 2000)
)

going_underground = MidGameEvent(
    name="Going underground",
    description=
    """Lately, you,ve been hearing rumors about a complex system of underground tunnels built
    beneath your city. According to several people, there are monsters living there and they
    are responsible for several disappearances. Others claim that monsters do not exist and that
    the tunnels are where criminals store their contraband as well as the remains of occasional
    rival or witness.
    
    To you, all of that sounds like stories made up by a particularly creative drunkard,
    but a few people have in fact disappeared this month. You may send the police to investigate,
    just to be sure - but it might cause suspicion, so maybe denying everything is the right choice.
    After all, tall tales and insane ramblings don't deserve the city's attention.
    
    According to Geber Selgorn, underground tunnels exist and they are a matter of the occult.
    He also thinks that sending the police will not solve anything and that as a founder and leader
    of the city, you are spiritually responsible for discovering the truth. Geber Selgorn is probably
    insane, but you already know that.""",
    actions={'Send the police': lambda state: spawn_after_n_turns(state,
                                                                  BasicEvent(
                                                                      name=going_underground.title,
                                                                      description=
                                                                      """Surprisingly, the rumors were true. The police investigation has uncovered that a group of wealthy citizens
                                                                      ordered the creation of underground tunnels under a mansion belonging to one of them. Apparently, they have
                                                                      formed a secret society with unclear (but potentially anti-government) goals. The conspirators have admitted
                                                                      that their organization caused the disappearances of several citiziens, although they refused to elaborate
                                                                      on the details. According to them you wouldn't be able to understand them even if they did tell you everything.""",
                                                                      actions={'OK': lambda game_state: None})
                                                                  if attr_greater(state, 'security', 5)
                                                                  else BasicEvent(
                                                                      name=going_underground.title,
                                                                      description=
                                                                      """According to the police, there are absolutely no underground tunnels beneath the city. There are no
                                                                      conspiracies, all disappearances have a mundane explanation and there is absolutely nobody corrupt enough
                                                                      to take bribes in exchange for covering up the truth.""",
                                                                      actions={'OK': lambda game_state: {'security': -2,
                                                                                                         'prestige': -1}
                                                                               }),
                                                                  1),
             'Do nothing': lambda state: modify_state(state, {'security': -2}),
             'Investigate the matter yourself': lambda state: spawn_immediately(state, BasicEvent(
                 name=going_underground.title,
                 description=
                 """The mad doctor thinks that you should personally look for the underground tunnels. You decide to follow
                 his advice, which means that you're probably becoming equally mad. Every day after work you wander
                 the streets looking for a secret entrance, and the only person helping you is an old man obsessed with
                 alchemy, ghosts and gods.""",
                 actions={'OK': lambda game_state: set_flag(game_state, 'going_underground')}
             ))},  # TODO: other events in this chain (controlled by the 'going_underground' flag)
    condition=lambda state: counter_greater(state, mansion.name, 0)
).chain_unconditionally(lambda state: modify_state(state, {'population': randint(1, 10)}))
