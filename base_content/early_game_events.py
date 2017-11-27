from oth_core.text_events import *
from random import randint
from functools import wraps
import oth_core.buildings

"""This is the module for things that should happen in early game (first 10 years) and for random events that can happen
from early game onwards. NPC introductions, a bit of worldbuilding here and there, random events with (potentially)
bad outcome (but not bad enough to ruin your game), setting up a few bigger plots which will be resolved later."""


def get_random_events():
    return [speakers_hall_event, political_unrest_event, cold_winter_event, the_artist_leaves, bridge_builders,
            pollution_event, park_event, thieves_event, no_plague, futility_event]


def get_nonrandom_events():
    return [city_council_event, peter_ponzi, geber_selgorn, isabel_martell, george_connolly, transition_event]


def is_early_game(state):
    return state.branch.startswith("The Founding of ")


class EarlyGameEvent(ConditionalEvent):
    """A class for random events that can only happen during the early game"""

    def __init__(self, name, description, actions, condition=None):
        super().__init__(name, description, actions, condition)
        if condition is not None:
            self.should_be_activated = wraps(condition)(
                lambda state: (condition(state)) and (is_early_game(state)))
        else:
            self.should_be_activated = is_early_game


########################################################################################################################
#                                             non-random events go here

city_council_event = ConditionalEvent(
    name="The city council",
    description=
    """You begin to realize that running even a small town is more difficult than it
    first seems. There are just too many things to consider, and you don't really know
    anything about most of those things. You're not even sure that you know the complete
    list of things you should know about to successfully run the city but don't.

    You decide that of all the things you know that you don't know about, three are quite
    important: making your town the kind of place that people want to live in, preventing
    the diseases from killing everyone and making sure that all the things achieved by
    the modern civilization doesn't end up forgotten as the society slowly reverts back
    to living in the caves. To help with your own lack of knowledge, you decide to form
    a city council consisting of people who know those things.

    You ask members of three social groups that are known to know those things - merchants
    as experts on making things good to the buyers, doctors as experts on helping everyone
    stay alive and skilled workers as experts on operating and repairing obscure pre-plague
    machines - to select the most qualified representatives for a prestigious position
    that would allow them to help the community and defend their own interests at the same
    time.""",
    actions={'OK': lambda state: None},
    condition=lambda state: state.turn == 36
)

peter_ponzi = ConditionalEvent(
    name="Peter Ponzi",
    description=
    """The merchants have assured you that they have picked just the right person for
    the city council job. Unfortunately, it also seems that they have a fairly low opinion
    of politics and politicians as their choice of a council member is the least trustworthy
    person you've ever seen.

    Peter Ponzi, your new advisor, is a shady salesman of used everything. He's got hundreds
    of ideas for making money, and they all include various degrees of insincerity - but he
    assures you that if you listen to him, the city will become rich and prosperous. You have
    your doubts, although you're pretty sure that they will make Peter Ponzi rich and prosperous.
    He talks about everything from art to farming equipment and from wristwatches to weapons,
    but it always comes down to assessing monetary value and convincing people to buy for
    twice as much.

    Still, it seems that as far as untrustworthy liars go, Ponzi is at least fairly competent.
    He speaks with charisma and he makes you want to believe all his exaggerated promises of
    wealth and fame. Even the way he looks is all about walking the fine line between
    high-class elegance and tacky excess. Ponzi knows how to appeal to rich people and how to
    sell things that you wouldn't even want for free.""",
    actions={'OK': lambda state: None},
    condition=lambda state: state.turn == 48
)

geber_selgorn = ConditionalEvent(
    name="Geber Selgorn",
    description=
    """The doctors have picked a new city council member from among their ranks. They
    assure you that he's just the right person for the job: both competent (he was educated
    in a better time, in a school which doesn't exist now but apparently used to be
    well-respected and prestigious) and dedicated to selflessly helping other people
    (when the white plague decimated entire cities, he travelled to the most heavily
    affected regions to save as many people as he could - from tundras in the north to
    southern deserts). You can't help but be a bit excited to be able to work with someone
    like that.

    After you meet your new advisor, you realize that what his coworkers didn't tell you
    about him is more important than what they told. Geber Selgorn is a man with a lot of knowledge
    and dedication, but not a lot of sanity. When he comes into your office dressed in
    a coat (made from a fur of an animal you didn't even know existed) and a turban (which he
    may or may not have stolen from a desert nomad) and starts talking about your city
    as a next step in the alchemical transmutation of the world which started when the plague
    destroyed the old world, you seriously consider locking him in an asylum (before
    remembering that there's no asylum in your city).

    Despite his apparent insanity and his (strangely unscientific for a practitioner of
    medicine) occult interests, Selgorn is a knowledgable and experienced doctor. While you
    find yourself unable to decide if there's more to his weird philosophy than some
    kind of brain damage caused by the white plague, he sure knows a thing or two about
    keeping people from dying. His advice might help you keep everyone healthy, but you
    have a feeling that trusting him unconditionally might result in the whole town
    getting sacrificed to a forgotten deity in exchange for the elixir of life (or at least
    the universal solvent).""",
    actions={'OK': lambda state: None},
    condition=lambda state: state.turn == 72
)

isabel_martell = ConditionalEvent(
    name="Isabel Martell",
    description=
    """It took a long time before the members of worker guilds decided on their city council
    representative. Unlike the merchants and the doctors, they don't go out of their way
    to convince you that your new advisor will be good for the job - they just introduce
    you to the person and go back to their own business.

    Isabel Martell, the newest member of your council, appears to be determined and ambitious.
    She wasn't chosen for the position - she decided that this is what she wants to do,
    then she convinced the guilds that this is the thing that's worth doing. When telling
    you about how she left watchmaking to participate in local politics, she claims that
    from now on, the guilds will be politically active to keep the knowledge from being
    forgotten, but also to keep it from becoming a secret known only to the University.
    She tells you about her plans for the future: apprenticeship opportunities for young
    people, great factories and the society that slowly grows back to what it was before
    the white plague.

    You're not sure if you believe in her plan. You're not even sure if she believes in it.
    What you do know is that she's ambitious enough to help the city achieve something,
    but you can't be sure what will it be. You hope that it will at least be better than
    the slow decline that will inevitably happen if you don't do anything.""",
    actions={'OK': lambda state: None},
    condition=lambda state: state.turn == 84
)

george_connolly = ConditionalEvent(
    name="George John Connolly",
    description=
    """Just when you thought that you're done with assembling the city council, the city's
    police chief arrives in your office to tell you that the central government assigned him
    to make sure that all the state-wide laws are respected, the citizens are safe and crime
    is kept in check.

    George John Connolly, your newest advisor, is a tired-looking man who's probably old
    enough to retire. He's got many years of experience as a police officer under his belt,
    he is respected by his subordinates and even some of the citizen think of him as a hero.
    When talking to you, he makes sure to let you know that he's not a bureaucrat who wants to
    ensure a pedantic adherence to procedures and that his goal is to keep the citizens safe
    no matter the cost, not to create the appearance of safety by having policemen on every
    corner and prisons full of small-time pickpockets.

    You have a feeling that Connolly might be the right person for the job. In fact, you
    begin to realize that he, the person you didn't even consider as a potential member of
    the council, might be the only person who knows what he's doing. It seems that compared to
    him, everyone else - especially you - is stumbling around in the darkness and desperately
    trying not to break anything.""",
    actions={'OK': lambda state: None},
    condition=lambda state: state.turn == 99
)


def go_to_mid_game(state):
    import base_content.mid_game_events as mid_game
    state.branch = mid_game.BRANCH_NAME
    state._event_inactive_deck.extend(mid_game.get_random_events())
    state.nonrandom_events.extend(mid_game.get_nonrandom_events())


transition_event = ConditionalEvent(
    name="What now?",
    description=
    """You have laid foundations for what you hope will one day become a great city. You have
    assembled a city council that you hope will guide you toward your goals. You hope that
    everything will end up just right.

    You realize that you're doing an awful lot of hoping. This kind of optimism feels good,
    but it may be harmful if you don't exercise moderation. It might be a good idea to offset this
    enthusiasm by thinking about everything that could potentially go wrong, and maybe even
    do something to prevent it. This might even work.

    The future is uncertain and unpredictable. But it might not be hopeless.""",
    actions={'OK': go_to_mid_game},
    condition=lambda state: state.turn == 120
)

########################################################################################################################
#                                               random events go here

speakers_hall = oth_core.buildings.BasicBuilding(
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
    actions={'OK': lambda state: modify_state(state, {'prestige': -2, 'population': -1})}
)

bridge = oth_core.buildings.CustomBuilding(
    name="Bridge",
    description="More convenient than using a boat.",
    base_price=400,
    additional_effects={'technology': -1},
    per_turn_effects={'money': -10},
    build_predicate=lambda tile, neighbors:
    oth_core.buildings.has_neighboring_buildings(neighbors) and oth_core.buildings.is_on_water_tile(tile)
)


def unlock_bridge(state):
    modify_state(state, {'money': -1000, 'population': 4})
    unlock_building(state, bridge)


bridge_builders = BasicEvent(
    name="The bridge builders",
    description=
    """A group of travellers arrive in your town. Like more or less all travellers,
    they are poor and dirty. Unlike most travellers, they don't ask nicely to be allowed
    to stay. No, they claim that they will leave unless you pay them a fairly large
    sum of money.

    Before you laugh them out of the room, one of them explains that they're bridge builders
    and that this may be your only chance to find someone who knows how to build bridges
    that don't fall apart at the worst possible moment. This might be necessary if you
    can't expand the city without crossing some kind of water.""",
    actions={'Accept the offer': unlock_bridge,
             'Turn them away': None}
)

pollution_event = EarlyGameEvent(
    name="Poisonous air",
    description=
    """Recently, a few people in your town suddenly died despite not suffering from
    any known previous illness (outside of the white plague, obviously). After the doctors
    examine their bodies, they come to the unsettling conclusion: those people have been
    poisoned.

    The policemen assigned to the case are unable to find any suspect. However, one of them
    notices that all of those people have been leaving close to one of the factories.
    After the doctors study smoke coming from their chimneys, they conclude that it is, in
    fact, potentially poisonous.

    The factory's chief engineer admits that their revolutionary new method of production
    might be the cause of the problem - but he urges you not to take action against
    the factory. He claims that the factory's increased output is necessary to produce
    hospital equipment, medicine, farming tools and many other necessities, and that more
    lives will be saved than lost if it continues running.""",
    actions={
        'Force the factory to abandon their new method.': lambda state: spawn_immediately(state, BasicEvent(
            name=pollution_event.title,
            description=
            """The engineer is obviously lying. He cares only about making profits and doesn't care
            about the people whose lives he puts in danger. Fortunately, he is able to make a cost-benefit
            analysis and decides that he'll make more profit if he uses conventional production methods
            than if you shut down his factory because he was too stubborn.""",
            actions={'OK': lambda game_state: modify_state(game_state, {'technology': -2, 'health': 1})}
        )),
        'Allow them to continue': lambda state: spawn_immediately(state, BasicEvent(
            name=pollution_event.title,
            description=
            """The engineer is right. We need the factories. Deaths due to poisonous air might be horrible,
            but if we can't produce all the necessities, there will be even more deaths. It sounds wrong
            to apply a cost-benefit analysis to human lives, but what else you can do when choosing between
            deaths and more deaths?""",
            actions={'OK': lambda game_state: modify_state(game_state, {'technology': 2, 'health': -1, 'prestige': -1})}
        ))
    },
    condition=lambda state: counter_greater(state, 'Factory', 0)
).chain_unconditionally(lambda state: modify_state(state, {'population': randint(-3, -6)}))

park = oth_core.buildings.BasicBuilding(
    name="City park",
    description="A piece of forest inside the city. Hopefully without dangerous animals.",
    base_price=50,
    additional_effects={'health': 1},
    per_turn_effects={}
)

park_event = ConditionalEvent(
    name="The lack of trees",
    description=
    """Farmers responsible for the city's supply of food are complaining that it's too much
    like a city with just streets and buildings but no trees or any other kind of plants.
    You feel tempted to dismiss those complaints as coming from people who don't understand
    the purpose of a city but they actually might have a point. Maybe some trees would make
    the city more pleasant.""",
    actions={'OK': lambda state: unlock_building(state, park)},
    condition=lambda state: counter_greater(state, 'Farm', 0)
).chain_unconditionally(lambda state: modify_state(state, {'prestige': -1}))

thieves_event = EarlyGameEvent(
    name="The city of thieves",
    description=
    """According to rumors, some of the people who recently migrated to your city
    are professional thieves who wish to set up a base for their illegal operations
    and to secretly educate young people about theory, practice and ethics of
    criminal life.

    You're not sure if there's truth to this rumors but you instruct the police
    to be careful. Then again, the same rumors claim that the thieves are bribing
    someone from your police force to help them avoid detection.""",
    actions={'OK': lambda state: modify_state(state, {'population': 4, 'safety': -2})}
).chain_unconditionally(lambda state: add_inactive_event(state, ConditionalEvent(
    name="The not-so-great heist",
    description=
    """It seems that nothing is sacred and no place is safe! The thieves have stolen
    the city's money. It wasn't much - they could have easily taken more. You feel
    that it was less about profit and more about sending you a message. They are not
    afraid of you.""",
    actions={'Make them afraid. Hire more police.': lambda game_state: modify_state(game_state,
                                                                                    {'money': -500, 'safety': 2}),
             'Do nothing': lambda game_state: None},
    condition=lambda game_state: attr_lower(game_state, 'safety', 3)
).chain_unconditionally(lambda game_state: modify_state(game_state, {'money': -500, 'prestige': -1}))))

no_plague = BasicEvent(
    name="A new age?",
    description=
    """Generally speaking, doctors aren't happy when their patient dies - but today,
    it seems they were relieved when they brought you what usually would be bad news
    (and also what usually wouldn't be something they bother the city's mayor with).
    You can't blame them.

    If what they told you is true, the patient who died today was the last known person
    in the city to be infected with what they refer to as 'acute form of the white plague'.
    While everyone else is still infected and will still suffer from the consequences,
    it looks like the days of mass graves and quarantines are over.

    You have a feeling of entering a new age - but you also know that it will not be
    the same as the time before the plague. We won't know everything we would like
    to know or build the monuments to the greatness of humanity, but maybe we won't forget
    everything and maybe our creations won't crumble to dust.""",
    actions={'OK': lambda state: modify_state(state, {'health': 4})}
)

futility_event = BasicEvent(
    name="Exercise in futility",
    description=
    """You come home after a long day at work, you get the overwhelming feeling that
    everything you're doing is entirely pointless. Your future is going to be all about
    listening to pointless arguments in which everyone is wrong, having to choose between
    different wrong options, get blamed for every decision you make and also get blamed
    for not making decisions.

    It is not going to get any better.""",
    actions={'OK': lambda state: None}
)
