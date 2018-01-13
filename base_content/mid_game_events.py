from oth_core.text_events import *
from oth_core.buildings import BasicBuilding

"""This module is for events that can happen in the mid-game or from mid-game onwards. Events should have bigger
possible disadvantages and bigger rewards, the advisors should unlock new buildings and special actions while also
giving advice and we should have a few small event chain with more plot than before. Also, weird stuff (preferably
subtly weird and never explained too much) should start happening."""


BRANCH_NAME = "Uncertain but Hopeful"


def get_random_events():
    return [mansion_event, going_underground, contradiction_society]


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


########################################################################################################################
# 'Going underground' event chain: you build mansion for rich people, then they build underground tunnels and create
# a secret society
# TODO: - war between factions of secret society (you can participate if you're a member, people just die if you aren't)
# TODO: - (optional) events about going underground (before finding the secret society)
# TODO: - (optional) events about being a member of the secret society

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
             ))},
    condition=lambda state: counter_greater(state, mansion.name, 0)
).chain_unconditionally(lambda state: modify_state(state, {'population': randint(1, 10)}))

contradiction_society = ConditionalEvent(
    name="The Contradiction Society",
    description=
    """You finally did it. You found the underground tunnels beneath the city. The maze
    connects houses of some of the wealthiest citizens with a confusing system of impressively
    large halls, small, oddly-shaped rooms and everything in between. Occasionally, you see
    strange symbols painted on the walls, floors and ceilings. Sometimes, you find what looks
    like an everyday object - it can be a chair, a spoon, a shoe - but it's always somehow
    twisted into something wrong, strange and impractical. Rarely, you see a machine - not
    as big as the ones they have in the factories but as incomprehensible to someone without
    technical knowledge. After a few hours, you find the people ones built this place.
    
    There are neither monsters living here nor there's a hidden society of hardened criminals
    and violent madmen - those stories were a lie. On the contrary, you know many of those
    people from your everyday life: you pass them on the street, they come to your office,
    they buy and sell things, they work in workshops and hospitals. Most of them are members
    of high society, some of them are popular artists. They are your town's chapter of
    The International Contradiction Society.
    
    There's no conspiracy here. No murder, no plotting against the government, not even theft
    or smuggling. Just a group of people with similar interests, doing what they can
    to explore the contradictory, the paradoxical, the impossible. The only goal here is to
    find things that are despite the fact that theoretically they shouldn't be. And yes,
    in the early days some people died here - but it's much safer now, and this will not
    happen again.
    
    At least that's what they tell you. You're not sure if you believe them - especially
    when they offer you quite a substantial sum of money should you allow them to carry on.""",
    actions={'Leave them alone': lambda state: spawn_immediately(state, BasicEvent(
                name=contradiction_society.title,
                description=
                """The International Contradiction Society continues to thrive underneath your city. You hope
                that you didn't make the mistake and that no more people will disappear. Meanwhile, you're going
                to enjoy the donation that was given to you in exchange for maintaining the secrecy.""",
                actions={'OK': lambda game_state: modify_state(game_state, {'money': 5000})}
    )),
             'Expose them': lambda state: spawn_immediately(state, BasicEvent(
                 name=contradiction_society.title,
                 description=
                 """This needs to end. There will be no secret societies in your city.
                 
                 The police arrests the conspirators and raids their underground tunnels. They try to publicly
                 discredit you as either a madman or a malicious liar, but there is enough evidence to convince
                 everyone that you haven't lost your mind. The whole affair quickly catches the eye of the central
                 government and before you realize it, members of The International Contradiction Society are
                 taken to a remote prison for traitors, revolutionaries and other political criminals. You become
                 famous for your dedication to keeping your city safe.""",
                 actions={'OK': lambda game: modify_state(game, {'prestige': 4, 'security': 1})}
             ) if counter_greater(state, 'security', 7) else BasicEvent(
                 name=contradiction_society.title,
                 description=
                 """You reject the offer. You fully expect to die because of that, but you walk out of the tunnels
                 unscathed. Unfortunately, this does not mean you're successful.
                 
                 The police is reluctant to arrest anyone based on your 'crazy' story. When after Connolly's urging
                 a few of the officers go to question the conspirators and look for entrance to the tunnels in their
                 houses, they come back with nothing (maybe aside from a bribe or two). A few days later, conspirators
                 publicly mock you, Selgorn and the whole affair. You become famous for your paranoia and absurd
                 accusations - even though you always spoke the truth.""",
                 actions={'OK': lambda game: modify_state(game, {'prestige': -5})}
             )),
             'Join them': lambda state: spawn_immediately(state, BasicEvent(
                 name=contradiction_society.title,
                 description=
                 """Money? Police? You don't care about such things. What you care about is the great work that's
                 being done by The International Contradiction Society. You will not stop them, but neither will
                 you ignore them. You must become one of them.
                 
                 You join the best people your city has to offer. With them, you explore the contradictory,
                 the paradoxical, the impossible. You search for things that are - and you're not foolish enough
                 to claim that they shouldn't be.""",
                 actions={'OK': lambda game: modify_state(state, {'prestige': 5})},
             ))},
    condition=lambda state: flag_isset(state, 'going_underground') and counter_greater(state, mansion.name, 0)
).chain_unconditionally(lambda state: unset_flag(state, 'going_underground'))
