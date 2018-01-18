from math import floor

from oth_core.text_events import *
from oth_core.buildings import BasicBuilding
from oth_core.special_actions import LimitedSpecialAction

"""This module is for events that can happen in the mid-game or from mid-game onwards. Events should have bigger
possible disadvantages and bigger rewards, the advisors should unlock new buildings and special actions while also
giving advice and we should have a few small event chain with more plot than before. Also, weird stuff (preferably
subtly weird and never explained too much) should start happening."""


BRANCH_NAME = "Uncertain but Hopeful"


def get_random_events():
    return [mansion_event, going_underground, contradiction_society, underground_war]


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
                                                                  if attr_greater(state, 'safety', 5)
                                                                  else BasicEvent(
                                                                      name=going_underground.title,
                                                                      description=
                                                                      """According to the police, there are absolutely no underground tunnels beneath the city. There are no
                                                                      conspiracies, all disappearances have a mundane explanation and there is absolutely nobody corrupt enough
                                                                      to take bribes in exchange for covering up the truth.""",
                                                                      actions={'OK': lambda game_state: {'safety': -2,
                                                                                                         'prestige': -1}
                                                                               }).chain_unconditionally(
                                                                      lambda game_state: set_flag(game_state,
                                                                                                  'contradictors_remain'
                                                                                                  )),
                                                                  1),
             'Do nothing': lambda state: [modify_state(state, {'safety': -2}),
                                          set_flag(state, 'contradictors_remain')],
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
).chain_unconditionally(lambda state: modify_state(state, {'population': -randint(1, 10)}))

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
                actions={'OK': lambda game_state: [modify_state(game_state, {'money': 5000}),
                                                   set_flag(game_state, 'bribed_by_contradictors')]}
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
                 actions={'OK': lambda game: modify_state(game, {'prestige': 4, 'safety': 1})}
             ) if counter_greater(state, 'safety', 7) else BasicEvent(
                 name=contradiction_society.title,
                 description=
                 """You reject the offer. You fully expect to die because of that, but you walk out of the tunnels
                 unscathed. Unfortunately, this does not mean you're successful.
                 
                 The police is reluctant to arrest anyone based on your 'crazy' story. When after Connolly's urging
                 a few of the officers go to question the conspirators and look for entrance to the tunnels in their
                 houses, they come back with nothing (maybe aside from a bribe or two). A few days later, conspirators
                 publicly mock you, Selgorn and the whole affair. You become famous for your paranoia and absurd
                 accusations - even though you always spoke the truth.""",
                 actions={'OK': lambda game: [modify_state(game, {'prestige': -5}),
                                              set_flag(game, 'enemy_of_contradictors')]}
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
             ).chain_unconditionally(lambda game: set_flag(game, 'member_of_contradiction_society')))},
    condition=lambda state: flag_isset(state, 'going_underground') and counter_greater(state, mansion.name, 0)
).chain_unconditionally(lambda state: unset_flag(state, 'going_underground'))

underground_war = ConditionalEvent(
    name="Underground war",
    description=
    """It is happening again. People are disappearing, and the citizens are once again talking about
    tunnels beneath the city and whatever happens inside them.""",
    # TODO write specific events
    actions={'OK': lambda state: spawn_immediately(state, BasicEvent(
        name=underground_war.title,
        description=
        """There's a war in the underground tunnels - but you may be able to stop it.
        
        A group known as Free Contradictors has separated itself from The International Contradiction Society.
        They oppose what they see as the betrayal of the organization's original goal: it is not longer about
        balancing the opposites and exploring all impossibilities, it focused too much on bureaucracy, internal
        politics and pointless theorizing about what such impossibilities mean for society and humanity. In other
        words, it became boring.
        
        A representative of contradictors loyal to The International Contradiction Society (chosen by a council
        which is elected by the majority of organization's members once every 5 years, with an explicit approval
        of The Paradoxical Court - as long as the High Contradictor doesn't use his right to veto) offers
        an alternative vision: the institutions are there to draw the line between ethical impossibility
        and behavior that can violate the law, make other contradictors feel uncomfortable and/or harm
        the organization's image should someone find the tunnels and decides to expose them. Besides,
        contradicting the original goals is a fitting evolution for groups that dedicate themselves to seeking
        contradictions and paradoxes.""",
        actions={'Side with Free Contradictors': lambda game: spawn_immediately(game, BasicEvent(
            name=underground_war.title,
            description=
            """You decide to aid the Free Contradictors. To do so, you carefully study all the rules created by
            The International Contradiction Society. Then, you arrange for a situation in which it's impossible to act
            in any way without violating them. When the institutions are paralyzed, you deliver the killing blow: you
            prove that inaction is also against the rules.
            
            As the bureaucratic paradox absorbs everyone still loyal to the local chapter of The International
            Contradiction Society, an artist belonging to Free Contradictors redirects the pure absurd energies into
            the nearest wall. He tells you that the paradoxified rocks and impossible soil he created will be a great
            sculpture material - but it won't be cheap.""",
            actions={'OK': lambda game_state: unlock_building(game_state, BasicBuilding(
                name="The Monument To Non-Existence",
                description=
                """This impressive sculpture built from impossible materials is a sight you won't forget as long you live - then again, this might not be very long.""",
                base_price=5000,
                additional_effects={'prestige': 5},
                per_turn_effects={'population': -100}
            ))}
        )),
                 'Side with The International Contradiction Society': lambda game: spawn_immediately(game, BasicEvent(
                     name=underground_war.title,
                     description=
                     """The world is a dangerous, chaotic place and if bureaucracies want to survive, they must stick together. You
                     blame the recent disappearances on Free Contradictors and make sure that they get arrested. Then, you use your
                     political experience to help The International Contradiction Society re-establish its underground authority by
                     designing a new set of rules and regulations to complement the existing rules and regulations while also
                     explicitly forbidding breaking of any past, present or future rules and regulations. For added contradictory
                     flavor, you make sure that it's impossible to follow (or even remember) all those laws.
                     
                     For your contribution to his victory, High Contradictor (after consulting the matter with The Anti-Senate)
                     grants you three wishes. The wishes must come from a predetermined list of achievable impossibilities
                     and The International Contradiction Society bears no responsibility for any undesirable side-effects.""",
                     actions={'OK': lambda game_state: unlock_action(game_state, LimitedSpecialAction(
                         name="Make a wish",
                         description=
                         """The International Contradiction Society owes you a favor and it is allowed - even required! - to make them do something
                         impossible for you. Unfortunately, it can't be just any impossible thing you can imagine: they'll only do impossible
                         things that were proposed by the High Contradictor or five members of Anti-Senate and approved by the supermajority
                         of the organization's members.""",
                         event_to_spawn=BasicEvent(
                             name="Doing the impossible",
                             description=
                             """Hidden from the eyes of unenlightened masses, you met with the most powerful members of your city's chapter of The International
                             Contradiction Society. You stood in the center of the great underground hall and, as the laws demanded, gathered The Paradoxical
                             Court. In their presence, you demanded that High Contradictor returns your favor. You wished to...""",
                             actions={
                                 '...turn space into time': lambda x: modify_state(
                                     x, {'population_max': -x.population_max, 'actions': 10}),
                                 '...turn policemen into gold': lambda x: modify_state(
                                     x, {'population': -floor(state.safety / 10), 'money': x.safety * 1000,
                                         'safety': -x.safety}),
                                 '...try again': lambda x: add_active_event(x, going_underground),
                                 '...suffer for your art': lambda x: modify_state(x, {'safety': -10, 'health': -10,
                                                                                      'food': -x.food, 'prestige': 10}),
                                 '...read a book': lambda x: modify_state(x, {'technology': 1})
                             }
                         ),
                         limit=3
                     ))}
                 )),
                 'Let them fight': lambda game: spawn_immediately(game, BasicEvent(
                     name=underground_war.title,
                     description=
                     """You're not here to take sides. They want war, conflict and murder? Let them have it. You joined the secret
                     society to take a break from ruthless and corrupt world of politics and you're not going to waste your time
                     and energy on it if it can't even give you that.""",
                     actions={'OK': lambda x: modify_state(x, {'safety': -1})}
                 ))}
    ) if flag_isset(state, 'member_of_contradiction_society') else BasicEvent(
        name=underground_war.title,
        description=
        """The whole thing is, of course, not your problem. After all, there are no underground tunnels
        or secret societies in your cities. Every disappearance can be explained without insane, overly
        complicated theories. Let's focus on something different - like that large sum of money which
        you have suddenly received from an unknown source.""",
        actions={'OK': lambda game: modify_state(game, {'money': 6000, 'safety': -5, 'prestige': -3})}
    ) if flag_isset(state, 'bribed_by_contradictors') else BasicEvent(
        name=underground_war.title,
        description=
        """This was bound to happen. You tried to fight The International Contradiction Society once
        and you failed. This made them feel powerful so of course they are back to committing the same
        crimes - after all, they don't fear punishment.
        
        You feel that you should try again - but you don't know if anyone will believe you.""",
        actions={k: v for (k, v, p) in
                 (('They will not believe you', lambda game: spawn_immediately(game, BasicEvent(
                    name=underground_war.title,
                    description=
                    """Nobody will believe you. The police is too corrupt to do anything so there's no need to bother
                    trying. In the end, the only thing you'll get will be public ridicule.""",
                    actions={'OK': lambda game_state: modify_state(game_state, {'safety': -2})})),
                  True),
                  ('Maybe they will', lambda game: spawn_immediately(state, BasicEvent(
                      name=underground_war.title,
                      description=
                      """You decide to make sure that everything goes according to your plan. The police might be
                      corrupt, but even the least trustworthy of them does not dare take bribes or falsify evidence
                      in Connolly's presence - and aside from that underground presence, the city is safe enough for him
                      to be able to personally participate in the raid.
                      
                      With Connolly's help, you quickly dismantle The International Contradiction Society. Apparently,
                      the organization went to war against itself - the bureaucrats entrenched themselves within what
                      seemed to be a secret society inside a secret society, and other members of the group decided to
                      oppose them. In the end, the contradictors have contradicted each other as well as themselves
                      - and maintaining secrecy while killing one another proved to be the one impossibility they were
                      not able to achieve.
                      
                      A fitting end.""",
                      actions={'OK': lambda game: modify_state(game, {'safety': 2, 'prestige': 2})}
                  )),
                  attr_greater(state, 'safety', 5)))
                 if p}
    ) if flag_isset(state, 'enemy_of_contradictors') else BasicEvent(
        name=underground_war.title,
        description=
        """The fact that you even consider doing something based on such silly rumors makes you
        doubt your own sanity. You're not sure if you should ignore all this madness, get the police
        involved or seek medical attention.""",
        actions={'Do nothing': lambda game: modify_state(game, {'safety': -2}),
                 'Go to the police': lambda game: spawn_immediately(game, BasicEvent(
                     name=underground_war.title,
                     description=
                     """Fortunately for you, it appears that even if you have gone mad, so did the world. The police
                     managed to find the entry to the underground tunnels beneath the city. Inside them, people were
                     fighting each other - apparently over either some strange philosophical issues or internal politics
                     involving institutions, voting and other such nonsense.
                     
                     While several people were caught, many have escaped. If their crimes don't come to light,
                     the experience they acquired can lead them to a successful political career.""",
                     actions={'OK': lambda game_state: modify_state(game_state, {'safety': 1})}
                 ) if attr_greater(game, 'safety', 5) else BasicEvent(
                     name=underground_war.title,
                     description=
                     """Predictably, the police didn't find anything. There's probably nothing to find. You're becoming
                     painfully aware of your poor judgement.""",
                     actions={'OK': lambda game_state: modify_state(game_state, {'safety': -2,
                                                                                 'prestige': -1,
                                                                                 'health': -1})}
                 )),
                 'Go to the doctor': lambda game: modify_state(game, {'safety': -2, 'health': 1})}
    ))},
    condition=lambda state: (
        flag_isset(state, 'contradictors_remain') or
        flag_isset(state, 'member_of_contradiction_society') or
        flag_isset(state, 'enemy_of_contradictors') or
        flag_isset(state, 'bribed_by_contradictors'))
).chain_unconditionally(lambda state: modify_state(state, {'population': -randint(1, 20)}),
                        lambda state: [unset_flag(state, x) for x in ('contradictors_remain',
                                                                      'member_of_contradiction_society',
                                                                      'enemy_of_contradictors',
                                                                      'bribed_by_contradictors')])
########################################################################################################################
