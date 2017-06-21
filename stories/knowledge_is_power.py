from oth_core.text_events import *
from oth_core.buildings import *


# helper function for chaining events regardless of player choice (might be moved to backend in the future)
def chain_unconditionally(event, function):
    new_actions = {}
    for k in event.actions.keys():
        v = event.actions.get(k)

        def new_action(state):
            v(state)
            function(state)

        new_actions[k] = new_action
    event.actions = new_actions
    return event


# helper for chaining actions with entering different branches
def enter_branch(func, branch):
    def ret(state):
        func(state)
        if branch == 1:
            pass  # TODO: add events in this branch
        if branch == 2:
            pass  # TODO: also add events in this branch

    return ret


# those should be self-explanatory: used for branch 1 when this variable is important
def increase_loyalty(state):
    state.counter.increment("Eliza's loyalty")


def decrease_loyalty(state):
    state.counter.decrement("Eliza's loyalty")


def loyalty_check(state):
    return True if counter_greater(state, "Eliza's loyalty", 3) else False


story_main = BasicEvent(
    name="Knowledge is Power",
    description=
    """The world around us is crumbling and yet we still prosper. Our workshops
and factories are kept alive by skilled workers, and their knowledge
will not be forgotten as the guilds they formed make sure that there
will be a new generation to keep repairing the city after they're dead.

There is, of course, a problem: the city needs the guilds and the guilds
know that the city needs them. Yesterday they were workers and today
they're the silent elite. Who knows what will happen tomorrow?""",
    actions={'OK': lambda state: spawn_after_n_turns(state, initial_chain, 12)}
)

knowledge_merchant_event = BasicEvent(
    name="The Knowledge Merchant",
    description=
    """Peter Ponzi arrives in your office with yet
another great idea that will surely bring the city a lot of money.
He explains that exchanging goods for money can only get you so far
because once people have enough goods they just won't buy them anymore.
The trick is to sell them something that can't be measured: knowledge.
It's not like they'll ever have all the knowledge they need and as long
as you're good at lying you don't even need to have the actual
knowledge, they'll just believe in everything you say.

Ponzi seems to be completely unaware that his bright idea amounts
to building schools, hiring incompetent teachers and hoping that nobody
notices that the alumni know less than members of the guild after
the first month of apprenticeship. Still, maybe you can turn this scheme
into something more advantageous.
""",
    actions={
        "Go with Ponzi's scheme": lambda state:
        spawn_immediately(state, BasicEvent(
            name="The Knowledge Merchant",
            description=
            """This may not be the most sophisticated fraud out there but it can work.
As time goes on, you're starting to appreciate its elegant simplicity:
selling bad knowledge to people who aren't knowledgeable enough to tell
the difference. It's as if we introduced a tax on stupidity.""",
            actions={'OK': lambda game_state: unlock_building(game_state, knowledge_merchant_building)}
        )),

        "Why build false schools when we can build real ones?": lambda state:
        spawn_immediately(state, BasicEvent(
            name="The Real Knowledge",
            description=
            """The city should not prey on its citizens. Instead, it should help them.
It's the right thing to do, and it can be profitable in the long run:
after all, educated citizens are productive citizens.""",
            actions={'OK': lambda game_state: unlock_building(game_state, trade_school_a)}
        )),

        "Why care about profit when we can get political power?": lambda state:
        spawn_immediately(state, BasicEvent(
            name="The Real Knowledge",
            description=
            """The idea of building schools appeals to you, but you don't really care
about money. You have bigger problems than that: the guilds are getting
more powerful and if you don't do something, the city will fall in their
hands. From now on, each guild will be required to send a teacher to
each of the schools - and they will have to teach everyone who wants to
learn. The ivory tower will be dismantled by those who wanted to build
it. Of course that means that the artisans will have to leave their
workshops and factories from time to time, but we can live with that.""",
            actions={'OK': lambda game_state: unlock_building(game_state, trade_school_b)}
        )),

        "Ignore Ponzi's proposal": lambda state:
        spawn_immediately(state, BasicEvent(
            name="The Knowledge Merchant",
            description=
            """A city making money from false schools? This has to be one of the worst
ideas you've ever heard. It's too stupid too work, it's immoral and it
just isn't how cities make money. If CHARACTER1 was the one in charge,
our police would be participating in burglaries and robberies instead
of stopping them.""",
            actions={'OK': lambda game_state: game_state.counter.increment("Eliza loyalty")}
        ))
    }
)

branch_event = BasicEvent(
    name="University man",
    description=
    """Just when everyone was starting to forget about the whole thing,
a thin, balding man carrying a large book arrives in town and starts
asking about 'Eliza Gutenberg, a child immune to the plague'. University
might be slow but it's always reliable.

After a lengthy medical examination, University man wants to have a word
with you and the girl's parents. Beyond any doubt, Eliza is healthy
and like every healthy child, she should leave for University as soon
as possible. He promises a substantial reward for letting him take her.
The parents protest - she's their only child, her place is with
the family.""",
    actions={
        'Send Eliza to University, share money with the parents.': enter_branch(
            lambda state: spawn_immediately(state, BasicEvent(
                name="To the University",
                description=
                """They raised the child, fed her, bought her clothes, spent what little
money the had on her well-being. Their efforts will be rewarded as now
they'll give CHARACTER3 something that few other children can dream of:
a future. They'll also receive half of the University donation because
while virtue might be its own reward, sometimes people need a more
concrete incentive to do the right thing.""",
                actions={'OK': lambda game_state: modify_state(game_state, {'money': 1000})}
            )),
            2),

        'Send Eliza to University, threaten the parents': enter_branch(
            lambda state: spawn_immediately(state, BasicEvent(
                name='To the University',
                description=
                """Their daughter can become a part of the country's most respected
institution, their city can solve its financial problems and yet they
can only think about themselves? This is not what a good citizen does.
This is theft, plain and simple: stealing the child's future
and stealing the town's prosperity! They'd better stop this behavior
before you lock them up with all the other thieves!""",
                actions={'OK': lambda game_state: modify_state(game_state, {'money': 2000})}
            )),
            2),

        'Allow the girl to stay in town': enter_branch(
            lambda state: spawn_immediately(state, BasicEvent(
                name="No place like home",
                description=
                """What CHARACTER3 needs is a family, and her family is here. A bunch of
pretentious academics will never be able to replace that. The child will
stay here and you'll give her the best education you can. It won't
be as good as what the University teaches (not even close) - but it
will make both her and her parents happy. And the University will
probably find some other healthy child anyway.""",
                actions={'OK': increase_loyalty}
            )),
            1)
    }
)

eliza_event = BasicEvent(
    name="Eliza",
    description=
    """The winter is over, the days are getting longer and the town looks
unusually pretty. You're taking a walk through its streets and trying
not to think about politics and taxes and food supply and the guilds.
Unfortunately, this moment of peace and quiet doesn't last for very long
because even when you forget about all the problems, the problems don't
forget about you. A messenger runs up to you and starts talking about
Geber Selgorn needing to see you in his office. Reluctantly, you stop
admiring nature and go perform your duties.

When you arrive, Selgorn is examining a girl, maybe old enough to
start going to school. Apparently, there's something unusual about
her. She's pale and weak and dehydrated but that's not what's important,
that's just minor food poisoning. The really interesting thing is that
unlike everyone else born in the last couple of decades she's never been
ill before - as if she didn't inherit the white plague. This would be
the first time someone like that was born here.

Selgorn admits that he took the liberty of sending a messenger to
the University. The road there is long and their bureaucratic procedures
are slow (everything there requires so many written documents, as if
talking to people was not enough for them; how can they even get
anything done?) but in a few months they'll probably send someone to
look at the girl. This can bring us a substantial amount of money,
provided we let her go to the University and the parent's don't protest
too strongly.""",
    actions={'OK': lambda state: spawn_after_n_turns(state, branch_event, 20)}
)

initial_chain = chain_unconditionally(knowledge_merchant_event,
                                      lambda state: spawn_next_season(state, eliza_event, 1))

knowledge_merchant_building = BasicBuilding(
    name="Knowledge Merchant",
    description="A perfect crime: selling questionable knowledge to people not knowledgeable enough to know better.",
    base_price=100,
    additional_effects={"prestige": -1},
    per_turn_effects={"money": 10}
)

trade_school_a = BasicBuilding(
    name="Trade School",
    description="A city's way of ensuring that the citizens actually know how to do their jobs.",
    base_price=200,
    additional_effects={"prestige": 1, "technology": 1},
    per_turn_effects={"money": -100}
)

trade_school_b = BasicBuilding(
    name="Trade School",
    description="A city's way of ensuring that those who know how to do their jobs won't take their knowledge to the grave.",
    base_price=200,
    additional_effects={"prestige": 1, "technology": -1},
    per_turn_effects={"money": -50}
)