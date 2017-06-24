from oth_core.text_events import *
from oth_core.buildings import *
from oth_core.game_errors import InternalError


# helper for chaining actions with entering different branches
def enter_branch(func, branch):
    def ret(state):
        func(state)
        if branch == 1:
            randoms = [tech_museum_event, occult_educator_event, eliza_museum_event, library_event, factory_event,
                       riot_event, walk_event, dispute_event]
            deterministic = [
                (education_choice_event, 24),
                (guild_ball_event, 168),
                (graduation_event, 180)
            ]
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
    condition=lambda state: counter_greater(state, "Factory", 0)
).chain_unconditionally(decrease_loyalty)


def riot_teach(state):
    increase_loyalty(state)
    modify_state(state, {'health': -3, 'safety': -5})


def riot_prevent(state):
    decrease_loyalty(state)
    modify_state(state, {'prestige': 3})


riot_event = BasicEvent(
    name="A Bad Day",
    description=
    """When things go wrong, they never have the decency to go wrong one at
a time. A few days ago, there's been a big food poisoning so Selgorn
was forced to temporarily forget about the less important matters like
his council duties, his occult research or sleep. Yesterday, some
merchants got angry at Ponzi because he allegedly didn't fulfill
his contractual obligations and now he has to run around the market,
selling all his valuables to be able to pay them back. A few hours ago,
George J. Connolly has left the council meeting in
a hurry because the angry merchants were trying to take out their
frustration on doctors who tried to prevent people from dying of food
poisoning. Somewhere along the way, Eliza's current teacher became
temporarily unable to work (this may or may not be related to food
poisoning, violence or both) while you're trying to control
the situation.""",
    actions={

        "Teach the girl yourself": lambda state: spawn_immediately(state, BasicEvent(
            name="A Bad Day",
            description=
            """You decide to give the girl a lesson in local politics and dealing with
emergency situations. Unfortunately, your multitasking skills are not
good enough to prevent the city from descending into chaos while at
the same time teaching someone about the complexity of preventing
the city from descending into chaos. Obviously, this causes the city
to descend into chaos as the sight of angry merchants assaulting
police officers manages to draw random small-time criminals into
the fight (it doesn't matter why there's a fight as long as you can
punch the man who caught you stealing) and the doctors' attempts at
dealing with the poisoning are interrupted by the need to deal with
their own wounds. Still, Eliza will probably learn a lot from this
situation.""",
            actions={'OK': riot_teach}
        )),

        "Focus on preventing the disaster": lambda state: spawn_immediately(state, BasicEvent(
            name="A Bad Day",
            description=
            """You decide to let someone else take care of the girl while you prevent
the city from descending into chaos. Because everyone else is also
preoccupied with preventing the city from descending into chaos,
the only person who has time to be a teacher right now is CHARACTER4
(she doesn't seem to care that much about rioting and disease as long
as workshops and factories are not suffering), always eager to impart
carefully selected, guild-approved knowledge upon CHARACTER3.

This division of responsibilities seems to work well: CHARACTER4 stops
complaining about your policies for a while, CHARACTER3 gets to learn
something and you manage to use all your diplomatic skills to a great
effect - in the end, the merchants are happy, CHARACTER1 is only
slightly more broke than he usually is and the doctors do their job
without killing any patients.""",
            actions={'OK': riot_prevent}
        ))
    }
)

walk_event = BasicEvent(
    name="Exploring the Known",
    description=
    """When taking a walk through the streets of your city, you decide
to take Eliza with you. You tell her all that you know about
architecture and history of each building you pass on your way. The girl
seems interested in the topic, asking many difficult questions which
make you doubt your urban planning skills. Maybe it's Gutenberg who
would do better as the mayor?""",
    actions={'OK': increase_loyalty}
)


def side_with_selgorn(state):
    increase_loyalty(state)
    modify_state(state, {'health': 3, 'technology': -2})


def side_with_martell(state):
    decrease_loyalty(state)
    modify_state(state, {'health': -2, 'technology': 3})


dispute_event = ConditionalEvent(
    name="A Philosophical Dispute",
    description=
    """During an otherwise boring day in the city hall, the peace gets suddenly
interrupted by a loud argument between Geber and Isabel.
When you try to find out what's happening, they insist that it's just
a philosophical debate about the importance of different areas
of knowledge.

Before you manage to get away, the council members demand that you
solve the conflict. According to Selgorn, we should learn about life
(human or otherwise), death, everything in between and the processes
behind them. Martell, on the other hand, prefers to focus on
the energies which push both living beings and inanimate objects forward
- she thinks there's nothing special about this 'life' and that to push
forward, we need to think in more general terms instead of limiting
ourselves to our own point of view.""",
    actions={

        "Life is more important": lambda state: spawn_immediately(state, BasicEvent(
            name="A Philosophical Dispute",
            description=
            """You say that we're living creatures and our inner workings are
the source of our problems - but understanding them is the solution.
Knowing about the lives of plants and animals will help us grow the food
we need to continue our own lives, and knowing how we ourselves work
can save us from deadly diseases.

Hearing this, Isabel becomes angry. It appears that the whole debate
was a wager - she wanted to use Geber's old gambling habit against
him but she bet on the wrong horse. Interestingly, the loser has to give
away not the money but the influence over what's taught in the city's
trade schools. From now on, they're going to be more medical than
technical.""",
            actions={'OK': side_with_selgorn}
        )),

        "Only the energies matter": lambda state: spawn_immediately(state, BasicEvent(
            name="A Philosophical Dispute",
            description=
            """You say that Selgorn's spiritual beliefs are wrong - life is nothing
more than a consequence of how the natural energies work. If we focus
on it, we miss the bigger picture - but if we look at what's common
to everything in the world, we can learn more not only about plants
and animals but also about mountains and rivers and stars and machines.

After you finish, Martell smiles. It appears that the whole debate
was a wager - she wanted to use Geber's old gambling habit against
him, and she succeeded. Interestingly, the loser has to give
away not the money but the influence over what's taught in the city's
trade schools. From now on, they're going to be more technical than
medical.""",
            actions={'OK': side_with_martell}
        )),

        "Art and history matter more than life and energies": lambda state: spawn_immediately(state, BasicEvent(
            name="A Philosophical Dispute",
            description=
            """Clearly, they're both wrong. The most important things are not the ones
that were given to us but those we create. We must learn from both
good and bad examples set by the previous generations, and we must
make the world more interesting and more beautiful. It's a good thing
that we want to know and understand, but we also shouldn't forget to
create and experience.

Neither the doctor nor the watchmaker are impressed by your speech.
In retrospect, it might have been better suited for a cafe full
of artists than an office full of bureaucrats.""",
            actions={'OK': lambda game_state: modify_state(game_state, {'prestige': 3})}
        ))
    },
    condition=lambda state: counter_greater(state, trade_school_a.name, 0)
)

guild_ball_event = BasicEvent(
    name="Night in the Factory",
    description=
    """You find yourself inside a large factory hall. Everything seems wrong:
through the windows, you see that it's night - but there are people
here. Despite the noise from the machines, everyone behaves as if it was
a high-class party - they're dressed in their best clothes, they drink
expensive alcohol and they're talking about things so meaningless
that even the most boring, self-absorbed socialite would not be able
to stand them for too long.

Seemingly out of nowhere, Isabel comes up to you. She tells you
that you should be proud - you've been invited to the guilds' secret
ball, and that you're the first person from outside of the guilds to be
there. When you try to find out how did you actually get there, she
only says that you shouldn't worry about it and try to make powerful
friends.""",
    actions={

        "Try to find business opportunities": lambda state: spawn_immediately(state, BasicEvent(
            name="A Great Opportunity",
            description=
            """The whole situation seems completely absurd to you. Why organize a ball
inside of a factory? Why make it secret? Why are you here and how did
it happen? This doesn't matter though: the important thing is that
there are high-ranking guild members out there, and that means there's
money to be made.

You make your way towards people who are loud but don't have anything
interesting to say and those who put on as much expensive jewelry
as possible without thinking of how good or bad it looks: those who
have money but lack common sense. You drink, but not too much.

In the end, you make some great deals - that is, they're great for you
and the city but not necessarily for the other side of the contracts.
You try to justify such unfair outcome with the guilds' countless
schemes against you.""",
            actions={'OK': lambda game_state: modify_state(game_state, {'money': 5000})}
        )),

        "Try to have fun": lambda state: spawn_immediately(state, BasicEvent(
            name="Drunk Diplomacy",
            description=
            """People tend to think that diplomacy is boring when in reality it's
anything but. Lengthy formal meetings aren't very interesting, sure,
but they're mostly a facade you put up in front of both your superiors
and the general public. Real diplomacy often happens during dinners,
parties and balls which start off not unlike those meetings but get less
formal as time goes on.

You drink. You talk. You dance. You drink some more. You learn a few
secrets, some more damaging than others. You drink even more, which
makes your memories of the night a bit unreliable. You're sure you've
been trying to seduce somebody, and you think you were in a fight or two
- but you don't remember the results.

In the end, you gain a few friends, some enemies and a terrible
hangover. You get introduced to the emerging elite, which you will soon
introduce to the old elite. The city's social life just became much
more interesting.""",
            actions={'OK': lambda game_state: modify_state(game_state, {'prestige': 5})}
        )),

        "Observe": lambda state: spawn_immediately(state, charles_pope_event),

        "Leave": lambda state: spawn_immediately(state, BasicEvent(
            name="Night outside of the Factory",
            description=
            """You don't know how you got here but you know how you're going to get
out. You ignore the party and start walking towards the door. When
someone offers you a drink, you take it without stopping. After
what feels like eternity, you make your way through the crowd and leave
the building.

It's quiet outside, despite the fact that a few guild members who had
too much to drink are desperately fighting an uneven battle against
the gravity. You walk home and when you're there, you fall asleep
quickly.

In the morning, you're not sure whether anything really happened - it
might as well have been a strange dream. There's only one thing you're
certain about - if the guilds are so busy organizing lavish parties
and keeping them secret, they're going to go bankrupt before they
become a real threat to you.""",
            actions={'OK': lambda game_state: None}
        ))
    }
)

charles_pope_event = BasicEvent(
    name=guild_ball_event.title,
    description=
    """As you approach the small gathering of guild members, it begins
to disperse slowly until only the man in the center of it all remains.
He smiles and introduces himself as Charles Pope. After a bit of
smalltalk that was so brief it could as well be nonexistent, he steers
the discussion towards politics.

Unlike Martell, he seems mostly uninterested in taxes and subsidies.
His interests are long-term: he talks about the white plague and how it
makes the organization of skilled workers into communities essential
to prevent the society from reverting to a more primitive state. He
praises the relationship between master and apprentice and criticizes
the school system as something that can't succeed in the new world.
Surprisingly, he also has a lot to say about religion: at first he seems
to repeat the ideas popular among the revolutionaries (the concept of
myths being used by those in power to promote social order which is
beneficial to them, the similarities between hierarchies of church
and state) but then he starts talking like a conservative, arguing that
there needs to be order, even if it's artificial. In the end, he
distances himself from that point of view as well by claiming that all
the contemporary religions are dying as their holy books are slowly
but surely becoming forgotten - and without them, the gods are too
distant to strike fear into people's hearts.

After a long discussion, he recites an old saying about the one-eyed
in the kingdom of the blind. He then follows it up by asking what should
the one-eyed king do when he sees someone with two eyes. He disappears
before you can answer.""",
    actions={

        "Try to find him": lambda state: spawn_immediately(state, BasicEvent(
            name=guild_ball_event.title,
            description=
            """Once again, you try to filter out all the noise and look for what's
important. Unfortunately, it seems that nothing is. You walk around
the factory hall, trying to find the strange man with a lot to say about
politics and religion but it looks like he simply vanished. After
an hour, you get visibly frustrated. After two, your behavior starts
bothering the guild members and you get asked to leave.""",
            actions={'OK': lambda game_state: modify_state(game_state, {'prestige': -2})}
        )),

        "Try to forget about the encounter": lambda state: spawn_immediately(state, BasicEvent(
            name=guild_ball_event.title,
            description=
            """You're not sure why but you find the whole situation unsettling. It's
clear that the man has his own agenda, and as is always the case with
the guilds, his agenda is different from your own. Suddenly, the whole
factory appears more hostile than it used to be and the unclear
circumstances under which you ended up here are making it much worse.
You decide that the only cure for this is alcohol.

In the morning, you wake up with a terrible hangover. The memories are
hazy but you're pretty sure you were talked into agreeing to some
horrible business proposal by an owner of one of the factories.""",
            actions={'OK': lambda game_state: modify_state(game_state, {'money': -500})}
        )),

        "Leave": lambda state: spawn_immediately(state, BasicEvent(
            name=guild_ball_event.title,
            description=
            """You're not sure why but you find the whole situation unsettling. It's
clear that the man has his own agenda, and as is always the case with
the guilds, his agenda is different from your own. Suddenly, the whole
factory appears more hostile than it used to be and the unclear
circumstances under which you ended up here are making it much worse.
You decide it's better to just leave this place.""",
            actions={'OK': lambda game_state: None}
        ))
    }
).chain_unconditionally(lambda state: spawn_after_n_turns(state, BasicEvent(
    name="The Aftermath",
    description=
    """You keep thinking about the guilds' secret ball and your discussion
with Charles Pope. It's obvious that he's planning something, and that
it will not end well for you.

You try to remember the details of the conversation. He liked
the idea of religious institutions but he was not a believer and he was
critical of the church. He didn't like trade schools. He was interested
in the white plague. What should you do about it - and isn't it too
late?""",
    actions={

        "Give money to the churches": lambda game_state: spawn_immediately(game_state, BasicEvent(
            name="The Aftermath",
            description=
            """A man who doesn't believe in a god and doesn't like any existing church
but thinks that some form of religion is necessary has to be an aspiring
cult leader - and the thing about cults is that they prey on
the weakness of bigger churches. You have to fight fire with fire: if
the churches become more important in people's lives, there will be no
interest in strange cults. The guilds are rich, and money is how they
will influence the public - therefore, churches must become even richer.""",
            actions={'OK': lambda g_state: modify_state(g_state, {'money': -3000, 'prestige': 1})}
        )),

        "Invest in education": lambda game_state: spawn_immediately(game_state, BasicEvent(
            name="The Aftermath",
            description=
            """Pope thinks that the best way to teach people is by making them
apprentices, but the guilds haven't been taking in new apprentices for
years. Obviously, they're trying to control who and when gets educated.
The solution is simple - the city must hire teachers, and those teachers
must teach everyone. The young and the old, the rich and the poor,
everyone has to become knowledgeable enough for the guilds to be unable
to control the knowledge.""",
            actions={'OK': lambda g_state: modify_state(g_state, {'money': -3000, 'technology': 1})}
        )),

        "Isolate Eliza from the guilds": lambda game_state: spawn_immediately(game_state, BasicEvent(
            name="The Aftermath",
            description=
            """Whatever Pope's plan is, it relies on people having the white
plague. There's one person in the city who doesn't suffer from it, and
she must be protected at all costs. Maybe they'll try to kill her, maybe
they'll try to make her one of them - it doesn't matter, they won't be
able to do that. At least not until she becomes an adult in the eyes
of the law (which is unfortunately very soon).""",
            actions={'OK': increase_loyalty}
        )),

        "Strike against the guilds directly": lambda game_state: spawn_immediately(game_state, BasicEvent(
            name="The Aftermath",
            description=
            """You don't need to know the details of the plan to stop it. The guilds
are powerful because they have money and they have money because of
workshops and factories. From now on, those will become much less
profitable as you go against Martell's every wish by raising taxes
on all the mechanisms and by withdrawing all the subsidies you gave
to the industry.""",
            actions={'money': 500, 'technology': -6}
        )),

        "Do nothing": lambda game_state: spawn_immediately(game_state, BasicEvent(
            name="The Aftermath",
            description=
            """Pope is playing games with you. He wants you to waste time and
money figuring out his plan and trying to stop it - but he wouldn't do
that if the plan hasn't been already put in motion. It is too late to
change the outcome - you will win if you prepared yourself, you will
lose if you didn't.""",
            actions={'OK': lambda g_state: None}
        ))
    }
), 1))


def get_graduation_event(state):
    if loyalty_check(state):
        if counter_greater(state, trade_school_a.name, 0): return eliza_ending
        return pope_ending
    return enlightener_ending
    pass

cult_event = BasicEvent(
    name="The Machine Cult",
    description=
    """A strange, new religion appears in the city. Its adherents believe that
the gods do not exist yet and that they need to be created by men,
and that the creation of gods is opposed by demons who try to prevent it
by spreading the white plague. Designing, assembling and maintaining
complex mechanical devices is seen as the divine duty, although only
the select few are allowed to do so - the unworthy will always introduce
flaws into the design, delaying the gods' arrival.

A central figure in the cult's mythology is The Enlightener who is
supposed to build the first generation of gods in the form of light
sources which, when looked at, allow people to see the designs
of greater gods. All faithful must protect The Enlightener as the demons
will be constantly attempting to kill him and if he dies, it won't
be possible to build gods until the next Enlightener is born after
a hundred years.""",
    actions={'OK': lambda state: modify_state(state, {'prestige': -1})}
)

graduation_event = BasicEvent(
    name="The Graduation",
    description="Eliza Gutenberg is now legally an adult. Her education is over.",
    actions={'OK': lambda state: spawn_immediately(state, get_graduation_event(state))}
).chain_unconditionally(lambda state: spawn_after_n_turns(state, cult_event, 22))

eliza_ending = BasicEvent(
    name="Graduation in the City Hall",
    description=
    """A small crowd has gathered in the city hall. It is Eliza Gutenberg's
graduation ceremony, and it might not look like what they have at
the University but it sure feels this way to everyone in the room.
The young woman's parents make a big speech, thanking everyone who ever
taught the girl. Gutenberg also makes a speech, praising the city's
efforts to educate her without separating her from her family. She ends
the monologue by announcing that she wants to share her knowledge with
everyone else and that she's going to become a teacher in one of
the city's trade schools.""",
    actions={'OK': lambda state: spawn_after_n_turns(state, BasicEvent(
        name="ENDING: The Gutenberg Polytechnique",
        description=
        """In the coming years, the city's political landscape changes. The machine
worshippers become a significant religion, at one point gaining more
followers than any of the more traditional churches. Most of
the faithful have a guild background, with most of the higher offices
taken by high-ranking guild members. The high priest, Charles Pope,
encourages workers to build shrines inside workshops and factories
as he thinks that work and worship are deeply connected.

The cult's success doesn't last long. As the guilds gradually turn
into religious organizations, the output of the factories slows down
and rich citizens start enrolling their children into trade schools
instead of begging for apprenticeship. Gutenberg distinguishes herself
as the teacher, with the alumni of those schools seeing her as an almost
legendary figure: a woman who cheated the white plague, acquired
knowledge without the help of the University and in the end used it not
for her personal gain but to help fellow citizens.

Your career as the mayor doesn't last much longer. After the influence
and wealth of the guilds fade, the popular view of them becomes much
more negative: they're seen as an evil secret society for the rich,
always scheming to gain more power and secretly worshipping unknown
gods. In this light, your choice of council members suddenly becomes
suspect: Isabel Martell's membership in the watchmakers' guild results in
multiple conspiracy theories and Geber Selgorn's occult interests (despite
how different they are from the machine worship) also don't make him
too popular.

As the situation starts getting out of hand, you resign from your
position. Eliza takes your place and to avoid bloodshed, decides
to exile everyone with connections to guilds, machine worship or
the council. Everyone, that is, except of you. As a gesture of
gratitude, you stay in the city and even become one of her advisors.

Under Eliza Gutenberg's rule, the city becomes renowned for its education
system. As the trade schools expand, she decides to build a higher
education institution known as the Polytechnic. While it never becomes
as renowned as the University, its acceptance of those affected by
the white plague turn it into the country's primary source of skilled
workers. The city prospers.""",
        actions={'OK': modify_state(state, {'game_over': 1})}
    ), 58)}
)

pope_ending = BasicEvent(
    name=eliza_ending.title,
    description=
    """A small crowd has gathered in the city hall. It is CHARACTER3's
graduation ceremony, and it might not look like what they have at
the University but it sure feels this way to everyone in the room.
The young woman's parents make a big speech, thanking everyone who ever
taught the girl. CHARACTER3 also makes a speech, praising the city's
efforts to educate her without separating her from her family. She ends
the monologue by announcing that she is going to join the engineers'
guild to work on the machines that will improve our lives.""",
    actions={'OK': lambda state: spawn_after_n_turns(state, BasicEvent(
        name="ENDING: Technological Theocracy",
        description=
        """In the coming years, the city's political landscape changes. The machine
worshippers become a significant religion, at one point gaining more
followers than any of the more traditional churches. Most of
the faithful have a guild background, with most of the higher offices
taken by high-ranking guild members. The high priest, Charles Pope,
encourages workers to build shrines inside workshops and factories
as he thinks that work and worship are deeply connected.

Despite her protests, the machine cult starts worshipping Eliza Gutenberg
as The Enlightener. This causes a small sect to break off from the group
under Isabel Martell's leadership. After a mysterious explosion in one of
the factories kills CHARACTER2, the cult is blamed for her death.
The cult's orthodox branch reacts violently, with Martell being
the only survivor as she managed to run away from the city before
the purge. Some say this was all planned beforehand, and that
the inner conflict was only an excuse to start riots.

You never find out the truth. After the sect is dealt with, the rioting
cultists start looking for another scapegoat and unfortunately, that
scapegoat happens to be you. As the rioters storm the city hall, you
find yourself in an uncomfortable proximity of their knives. You don't
survive.

Your death prevents you from seeing the city turned into a technological
theocracy. Pope takes the position of the mayor, although he's
never referred to as such - after all, he's a priest, not a politician.
After the riots end, the guilds once again start taking in new
apprentices and new factories are getting built. In a few years,
the city itself becomes a big factory. Travellers and merchants avoid
it but the national government sees its value and decides to tolerate
the religious symbols on the machine parts it produces as long as they
work. Like the machine from before the plague, the factory city becomes
something that everyone relies on yet no-one understands.""",
        actions=eliza_ending.actions
    ), 60)}
)

enlightener_ending = BasicEvent(
    name="Graduation in the Factory",
    description=
    """Once again, you find yourself inside a large factory hall. It is
different this time: the crowd of well-dressed guild members is not
having a party, they're listening to someone giving a speech. You move
to the front and notice that the speaker is CHARACTER3. She's standing
on a raised platform and she's dressed in what at first appears to be
factory workers' protective clothing but is in fact purely decorative:
the fabric is too light to protect her from anything and she has a lot
of jewelry that is against every safety code you've ever heard of.
You realize that this is a ceremonial costume.

CHARACTER3 speaks loudly, almost shouting - maybe for dramatic effect,
maybe to be heard over the noise of the machines. She criticizes you
and the city council while praising the guilds, claiming they saved
her from the ignorance and darkness. But the dark days will be over
soon as she'll bring back the light and make the city see the truth.""",
    actions={'OK': lambda state: spawn_after_n_turns(state, BasicEvent(
        name="ENDING: The Enlightened City",
        description=
        """In the coming years, the city's political landscape changes. The machine
worshippers become a significant religion, at one point gaining more
followers than any of the more traditional churches. Most of
the faithful have a guild background, with most of the higher offices
taken by high-ranking guild members. The high priestess, Eliza Gutenberg,
is worshipped as The Enlightener and she encourages members of the cult
to spread their faith across the world.

As time goes on, the cult becomes more and more violent. At first, it's
an internal conflict as The Enlightener accuses Charles Pope, the former
high priest, of lack of faith. He is soon found dead, crushed between
the gears of an enormous machine. Similar fate happens to priests of
other, more traditional religions, which leads to an investigation by
the police. This does not end well for the police force which is soon
wiped out by the cultists.

Without the police to keep peace, the cult takes over the city. Their
reign is a violent one, with dissidents executed publicly by
the terrifying Punishment Machine which now stands on the main square.
This almost happens to you, although you're saved by the intervention
of The Enlightener's most trusted advisor: Isabel Martell who first
introduced her to the guilds. Your punishment is changed from death
to exile, which also becomes the fate of your saviour as The Enlightener
cannot surround herself with people who question her decisions.

You spend the rest of your life as a storyteller specializing in factual
accounts of your city's history. The tale of how you lost power to
a strange cult becomes more famous as the city declines (it seems that
the more people get executed or exiled, the less people there are to
work on all those 'divine' mechanisms) and the University pays to tell
it to its students. The professors emphasize that you decided against
sending Gutenberg to the University and use it as a cautionary tale:
knowledge is power, the powerful will abuse their power if they don't
receive proper guidance and nobody is as good at giving that guidance
as the University.""",
        actions=eliza_ending.actions
    ), 66)}
)


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
