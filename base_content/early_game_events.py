from oth_core.text_events import *
from random import randint
import base_content.buildings


def get_random_events():
    return [speakers_hall_event, political_unrest_event, cold_winter_event, the_artist_leaves]


def get_nonrandom_events():
    return []


def is_early_game(state):
    return state.branch.startswith("The Founding of ")


class EarlyGameEvent(ConditionalEvent):
    """A class for random events that can only happen during the early game"""
    def __init__(self, name, description, actions, condition=None):
        super().__init__(name, description, actions, condition)
        if condition is not None:
            self.should_be_activated = lambda state:\
                (self.should_be_activated(state)) and (is_early_game(state))
        else:
            self.should_be_activated = is_early_game

speakers_hall = base_content.buildings.BasicBuilding(
    name="Speaker's Hall",
    description="This is a place in which people pay to hear the so-called speakers talk about boring political issues you don't care about from the perspective you don't agree with. Others pay to hear the so-called storytellers talk about interesting things which unfortunately are only products of their imagination.",
    base_price=800,
    additional_effects={"prestige": 2},
    per_turn_effects={"money": 100}
)

speakers_hall_event = EarlyGameEvent(
    name="Speakers and Storytellers",
    description=
    """After a day of hard work (it seems that managing even a small town is much
    more difficult than it may seem), you decide to relax at one of the local cafes.
    The place is more crowded than usual - it seems that you paid it a visit during
    a performance by one of your city's more popular artists.

    After the performance, you can't help but be impressed by the artist's talent
    and imagination. He tells a fascinating tale about the rise and fall of a great
    city in a world which appears to be governed by the laws of nature slightly
    different from the ones you know, although the difference is not obvious or
    easy to describe.

    When he's finished with his speech, the artist walks between the tables to
    ask for money so that he can keep performing in front of the audience instead
    of finding what some would refer to as 'an actual job'. When he reaches you, he
    refuses to accept payment. Instead, he asks you to help him turn the city into
    a place renowned for its art and culture. The first step, he says, would be
    building the Speakers' Hall - a place for speakers and storytellers (he insists
    on differentiating between those two groups of performers as the former report
    on true events while the latter are true artists who create events of their own)
    to rehearse and perform on stage in an organized fashion instead of randomly
    shouting their creations in cafes and pubs.

    You say that you'll consider his proposition.""",
    actions={'OK': lambda state: unlock_building(state, speakers_hall)},
    condition=lambda state: counter_greater(state, "Cafe", 0)
)

political_unrest_event = EarlyGameEvent(
    name="Political unrest",
    description=
    """A group of political radicals consisting of two artists nobody has heard of,
    one shopkeeper and one bored young man decides to stage a protest in the town square.
    After a while, their spirited (even if copied wholesale from Enlightenment Radio)
    tirades against the University's influence on the central government get interrupted
    by a slightly larger group of physical laborers who don't share their controversial
    worldview.

    Before the police arrives on the scene, everyone is gone. Despite the whole affair
    having no actual impact on anyone's life, both sides of the conflict are now certain
    that a violent revolution is coming and that they need to be prepared to fight for
    their cause. Of course, they both see you as the cause of their suffering: supporters
    of the government think that you don't do enough to keep everyone safe while its opponents
    claim that by not opposing the University, you're implicitly supporting it.""",
    actions={'OK': lambda state: modify_state(state, {'safety': -2, 'prestige': -1})}
)

cold_winter_event = BasicEvent(
    name="Rumors of cold winter",
    description=
    """There's a rumor that the next winter is going to be extraordinarily harsh. When
    you try to find out why do people believe it, they usually point to something about clouds,
    animals or tree leaves. Some say that they just know it. While you're not entirely convinced,
    it won't hurt to be prepared.""",
    actions={'OK': lambda state: spawn_next_season(state, BasicEvent(
        name="Cold days",
        description=
        """The cold winter arrived, just like the people predicted. The roads and buildings are covered
        with a thick layer of snow. When you have to go outside, the wind makes you wish you stayed home
        - but when you go inside, it's still so cold that you begin to seriously consider burning the whole
        city down for warmth.

        Parts of the town are paralyzed by the weather. Many of the people are sick. Some even froze
        to their deaths during a particularly cold night.

        You can't wait for spring.""",
        actions={'OK': lambda game_state: modify_state(game_state, {'health': (-2 if game_state.health < 5 else -1),
                                                                    'population': randint(-2, -20),
                                                                    'money': -500})}
    ).chain_unconditionally(spawn_next_season(state, BasicEvent(
        name="The winter's gone",
        description=
        """Finally, the spring has come. You have survived the terrible winter. Once again, there's sun
        and rain and hope. At least for the next few months.""",
        actions={'OK': lambda game_state: modify_state(game_state, {'health': 1})}
    ),
                                              1)),
                                                   0)}
)

the_artist_leaves = EarlyGameEvent(
    name="The artist leaves",
    description=
    """A painter, unknown to the general public but popular in the city's art community,
    decides to leave the town and move elsewhere. When asked why, he claims that it's
    because it's the most boeing, backwards place he's ever seen, that nobody here appreciates
    real talent and that the only way to succeed here is to repair watches, sell cheap
    beer or just become a thief.

    After a few weeks, nobody remembers the painter - either as an artist or as a person.
    Unfortunately, the one thing that does remain in public consciousness is his opinion about
    the town. Hating the city and planning to move out becomes the fashionable thing to do as
    everyone tries to distance themselves from the 'watchmakers, beer merchants and thieves'
    stereotype.""",
    actions={'OK': lambda state: modify_state(state, {'prestige': -2})}
)
