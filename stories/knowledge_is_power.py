from oth_core.text_events import *
from oth_core.buildings import *
from oth_core.game_errors import InternalError


# helper for chaining actions with entering different branches
def enter_branch(func, branch):
    def ret(state):
        func(state)
        if branch == 1:
            randoms = [tech_museum_event, occult_educator_event, eliza_museum_event, library_event, factory_event]
            deterministic = [
                (education_choice_event, 24)
            ]
            pass  # TODO: add events in this branch
        elif branch == 2:
            randoms = []
            deterministic = []
            pass  # TODO: also add events in this branch
        else:
            raise InternalError("Unknown branch number")
        for r in randoms:
            add_inactive_event(state, r)
        for d in deterministic:
            spawn_after_n_turns(state, *d)

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

initial_chain = knowledge_merchant_event.chain_unconditionally(
    lambda state: spawn_next_season(state, eliza_event, 1))

tech_museum_event = BasicEvent(
    name="The Guild Museum",
    description=
    """A small group of factory workers comes to your office with a business
proposal: if you give them a sufficiently large building and donate
some old mechanical devices you have no need for, they'll make a museum
of technology and engineering to talk to the citizens about how
wonderful and amazing all those machines are.

To be completely honest, you don't see how anyone could learn anything
from such a museum. Those workers don't seem too bright or
knowledgeable, although they're definitely passionate (maybe event too
passionate - in a way, they remind you of religious zealots). After
you question them a bit, they admit that they weren't really good at
their jobs so their guild came up with the idea of a museum to let them
earn money elsewhere, without getting in the way of the actual work.
Still, they do seem to be pretty good speakers so maybe they will manage
to captivate the audience the same way some of the storytellers do with
their fiction.""",
    actions={'OK': lambda state: unlock_building(state, tech_museum_building)}
)

education_choice_event = BasicEvent(
    name="Eliza's Education",
    description=
    """You promised Eliza's parents to give her the best education you
can. It is time to make good on that promise.""",
    actions={'OK': lambda state: BasicEvent(
        name="Eliza's Education",
        description=
        """You think about your options. The guilds are very selective about who
becomes their apprentice but you can use your political power to make
them accept her. On the other hand, she can attend a public trade school
- she won't learn as much as she would with the craftsmen but at least
they won't try to indoctrinate them with their politics.""",
        actions={

            "Convince the guilds to take Eliza as an apprentice.":
                lambda game_state: spawn_immediately(game_state, BasicEvent(
                    name="Eliza's Education",
                    description=
                    """You decide to put politics aside and ask the guilds for help. Eliza
will become an apprentice, learning everything she can about operating
the machines and repairing them - and if she's good, maybe they'll even
tell her how and why those machines work. You have your doubts about
the last part though - you're not sure if even they know that much about
what keeps their factories going.""",
                    actions={'OK': decrease_loyalty}
                )),

            "Send Eliza to a trade school.":
                lambda game_state: spawn_immediately(state, BasicEvent(
                    name="Eliza's Education",
                    description=
                    """Eliza Gutenberg will be allowed to attend one of the trade schools for free.
She'll be given the same knowledge that everyone else receives but
maybe her immunity to the white plague will make learning easier
for her.

Members of the guilds will be angry when they hear about it, but it's
not like they can do anything about it. They might spread rumors about
you and your city but this is yet another proof of how powerless they
really are.""",
                    actions={'OK': increase_loyalty}
                ))
        }
    ) if counter_greater(state, trade_school_a.name, 0) else BasicEvent(
        name="Eliza's Education",
        description=
        """You don't really have much choice - the only people in the city
qualified to teach the girl are craftsmen and factory workers. You spend
two days going door to door and asking each and every one of them to
take her as an apprentice and they keep refusing.

Obviously, it's not that they don't actually want to teach her - a child
who doesn't suffer from the white plague is a dream come true for them.
But they know you have no other choice and they are ready to use that
knowledge to their advantage.

After many more days of frustration, you reach an agreement: CHARACTER3
will learn from the best workers in each profession, but only after
the city donates a generous amount of money to the guilds.""",
        actions={'OK': decrease_loyalty}
    ).chain_unconditionally(lambda game_state: modify_state(game_state, {'money': -2000}))}
).chain_unconditionally(lambda state: spawn_after_n_turns(state, BasicEvent(
    name="The Apprentice Crisis",
    description="""The rich citizens are complaining that the guilds are taking in less
apprentices than they used to, and that the quality of education they
receive has gone down significantly (it seems that they now spend less
time teaching practical skills, instead focusing on attempts to turn
factory work into some kind of philosophy). You try to explain that you
don't really have much power over the guilds and their recruitment
process but despite your best efforts you also don't have much power
over the emotions of your citizens. In other words, they get angry.

During the next council meeting, you ask Isabel Martell about the issue.
Predictably, she doesn't say much. The only concrete information you can
get is that it has something to do with 'the Gutenberg affair',
but it's not like it clarifies anything.""",
    actions={'OK': lambda game_state: modify_state(game_state, {'prestige': -2})}
), 13))

occult_educator_event = BasicEvent(
    name="The Occult Educator",
    description=
    """Today, you have spent the whole day in your office. Ordinary citizens,
laborers, merchants, guild members, police officers, doctors - everyone
had something important to discuss with you. It is evening now and
you're ready to go home and finally get some sleep when once again
someone knocks on your door. With a resigned sigh, you tell the citizen
to enter.

Things soon go from bad to worse - it's not just someone with a strong
opinion about noise or alcohol or taxes, it' Geber Selgorn. You prepare
yourself for a long debate on the plague, the gods and the unknown. For
a few minutes, this is exactly what happens but to your surprise,
instead of going on for a few hours he steers conversation in
a different direction. Apparently, he thinks that the plague, the gods
and the unknown are what Eliza needs to learn about if she's to
fully realize her potential, and he's the best person to teach her about
those things.
""",
    actions={

        "Let Selgorn educate the girl": lambda state: spawn_immediately(state, BasicEvent(
            name="The Occult Educator",
            description=
            """For all his eccentricities, Selgorn knows a lot about medicine -
maybe as much as some of the professors at the University. And sure, his
ideas are not conventional - but it seems that the whole world is now
different from what we thought it is, so maybe those ideas have some
truth to them.

You let the old doctor educate the girl. He's delighted to find someone
who actually wants to listen to him - maybe because she's too young and
inexperienced to recognize his insanity or maybe because she was born
and raised after the white plague and therefore doesn't think in terms
of the old world's rules. Unfortunately, he becomes so absorbed by his
responsibilities as a teacher that he seems to forget that he's supposed
to care for the ill and take part in council meetings.""",
            actions={'OK': increase_loyalty}
        ).chain_unconditionally(lambda game_state: modify_state(state, {'health': -3}))),

        "Refuse": lambda state: spawn_immediately(state, BasicEvent(
            name="The Occult Educator",
            description=
            """You try to think of a convincing excuse and end up arguing that right
now CHARACTER3 must focus on understanding the intricacies of mechanical
engineering and learn how to repair trains. This, of course, isn't true,
but if it was possible to reason with him then he'd stop trying to
uncover the hidden truth (or whatever it is he's looking for) when it
became apparent that he's confusing knowledge with the legends he heard
on some remote desert. And what CHARACTER3 needs is real knowledge,
not legends and fairy tales.""",
            actions={'OK': lambda game_state: None}
        ))
    }
)

eliza_museum_event = ConditionalEvent(
    name="Girl in the Museum",
    description=
    """A group of well-dressed men arrives in your office. You do not recognize
them until they start talking: they may not look like themselves without
the factory worker's protective clothing but when they talk about
the machines the way religious people talk about their gods, you realize
that they're the workers who wanted to build the museum.

Apparently, Museum of Technology is a great success. People are always
coming to see the machines and hear about their greatness, and they're
always willing to pay. They claim that it's not just about the money
though: they want people to know the truth. Of course, the one who needs
it the most is Eliza - and they're willing to let her learn for
free.""",
    actions={

        'Agree': lambda state: spawn_immediately(state, BasicEvent(
            name="Girl in the Museum",
            description=
            """You send CHARACTER3 to Museum of Technology. After one visit, she keeps
going there a few times a month. Unfortunately, she doesn't seem to
learn anything about the machines there - the only thing she talks about
after going there is some strange, rambling philosophy. After a while,
you decide that it's just a waste of her time and forbid her from
visiting the museum, hoping to replace it with something more
educational. Unfortunately, it seems that the hours she spent listening
to those lunatics have affected her - she seems to believe that
the machines are alive, powerful and terrifying.""",
            actions={'OK': decrease_loyalty}
        )),

        'Disagree': lambda state: spawn_immediately(state, BasicEvent(
            name="Girl in the Museum",
            description=
            """If they want to preach their insane philosophy and pretend they're
teaching something useful, they're free to do that - but CHARACTER3
needs something better than this. You tell them that if the guilds want
her to learn, they'd better offer her some real knowledge instead of
cheap tricks designed to fool people into thinking that they're wiser
than they really are.""",
            actions={'OK': lambda game_state: None}
        ))
    },
    condition=lambda state: counter_greater(state, tech_museum_building.name, 0)
)

library_event = ConditionalEvent(
    name="The Library of Anything",
    description=
    """When analyzing the city's expenses, you notice that you're spending
quite a bit more money on a building that is of use to absolutely
nobody: the library. Just what the hell where you thinking when you
decided to build this thing?

You're about to order some workers to demolish it until you realize
that maybe it isn't so useless after all. Maybe CHARACTER3 can dig
through the books that gather dust there, maybe she can understand
the words on their pages and maybe, just maybe, among the piles
of boring diaries, useless government records from previous centuries
and the works of barely talented storytellers, she will find something
that she needs.""",
    actions={'OK': increase_loyalty},
    condition=lambda state: counter_greater(state, "Library", 0)
)

factory_event = ConditionalEvent(
    name="Absence",
    description=
    """In the last few weeks, Isabel hasn't been coming to the council
meetings. You find it strange - she never misses the meetings.
Peter? Sure, he's often too busy with his schemes of dubious
profitability and dubious legality. Geber? Of course, he tends to
get lost in his research. Everyone has a personal life, a day job
or just a personal project they're passionate about - some even have
all three. That is, everyone but Isabel - her entire life revolves
around giving the guilds a voice in the city's bureaucracy. Her absence
seems suspicious.""",
    actions={

        'Investigate': lambda state: spawn_immediately(state, BasicEvent(
            name="The Secret Teacher",
            description=
            """With the help of a few trusted policemen, you manage to find out that
Isabel Martell is now spending a lot of time at the factory. This is weird
as she never even worked there - before her involvement in city politics
and guild scheming she was a watchmaker with a small workshop.
On the other hand, it's not something that could warrant official police
involvement, especially if you don't want to anger some powerful people.

You decide to solve the issue outside of the official channels: you'll
just take a casual morning stroll down the streets near the factory
and 'accidentally' meet her on the way there. Surprisingly, this works.
Even more surprisingly, she's not alone when you meet her. She's with
Eliza.

Before you even ask the question, she starts to explain how extremely
sorry she is not to be able to attend the meetings. She then angrily
describes how inadequate Eliza's education is and how she needed
to take matters into her own hands until all the incompetent people
around her manage to absolutely and irreversibly ruin the child's
potential. After what feels like an hour of complaints about you,
the teachers and the guilds she runs off with the girl while talking
about practical, real-world knowledge.""",
            actions={'OK': lambda game_state: None}
        )),

        'Ignore': lambda state: spawn_immediately(state, BasicEvent(
            name="Absence",
            description=
            """Who are you to intrude on other people's lives? Maybe she went back
to watchmaking, maybe she's busy with the internal politics of
the guilds, maybe she even fell in love - that is, with a person, not
with trying to get you to give money for new factories or lower taxes
on gears and springs. Besides, it's not like you really miss her.
The council could do with less guild influence right now.

For some time, you can work in relative peace. Unfortunately, this
doesn't last very long as in a few weeks she's back at the council
meetings - and she has a lot to say about taxes and subsidies.""",
            actions={'OK': lambda game_state: None}
        ))
    },
    condition= lambda state: counter_greater(state, "Factory", 0)
).chain_unconditionally(decrease_loyalty)

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
    name=trade_school_a.name,
    description="A city's way of ensuring that those who know how to do their jobs won't take their knowledge to the grave.",
    base_price=200,
    additional_effects={"prestige": 1, "technology": -1},
    per_turn_effects={"money": -50}
)

tech_museum_building = BasicBuilding(
    name="Museum of Technology",
    description="Resting place for everything too broken to actually work but complex enough to impress the masses.",
    base_price=100,
    additional_effects={"technology": -1},
    per_turn_effects={"money": 10}
)
