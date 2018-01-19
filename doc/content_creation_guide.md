On The Hill Content Creation Guide
==================================

1. Introduction
---------------

As with the GUI guide, this is **not** a comprehensive API reference.
It's an informal introduction to various modules, functions and classes
used for defining content for On The Hill. This is a **technical** guide
about **programming** in-game buildings, special actions and text-based
events, as well as whole branches of the game's storyline which lead
to the game's endings. If you're interested in the non-technical
perspective about the writing style, setting and other elements of our
narrative, please read the [Writing Style and Worldbuilding](writing_style_and_worldbuilding.md)
document. It is recommended that you read that file, as given the game's
quirky nature (both as a result of a dreamlike, intentionally 'undefined'
setting and the fact that for a long time it was a one-man project;
maybe it still is), it can be surprisingly hard to separate what's
technical and what's non-technical. Programming is obviously technical
and writing is obviously not but there's also a whole lot of game
design which is sometimes like programming, sometimes like writing
and often its own thing.

The API itself is not as good as I hoped it would be, for several reasons.
The big one is that it relies on functions as first-class objects (e.g.
event constructors take functions as their arguments), and Python's limited
lambdas make in-line function definitions less useful than it should be
- and that means that sometimes you'll need to use ```def```, which breaks
the natural flow of writing (and reading) event code that I wanted to
achieve. I'm not sure that a typical object-oriented design with a lot of
classes would have been better though, although it would surely make some
of the backend stuff (e.g. serialization) trivial. Other problems include
the need to make many of the functions you write take the game's state
as an explicit argument, which is a bit tedious and error-prone.

Of course I'm only seeing all of this from hindsight: everything seemed
like a good idea at the beginning and only writing a lot of the content
for the game made me see room for improvement. For that reason, I decided
that attempting to redo it from scratch will not be worth it (I don't want
to scrap everything I already wrote). I am not ruling out the possibility
of designing something better: it might be Python's own metaclasses, it
might be Hy's powerful macros, it might be code generators and it might
even be a full-blown DSL (I once made a JSON-based DSL for this game;
unfortunately, I had to get rid of it because it was shitty and embarassing).
If I do any of that, I'll make sure to keep backwards compatibility though
so while this guide might get deprecated, it's not going to become
completely useless.

2. Basic concepts
-----------------

The game's content can be divided into several distinct categories:
buildings, events, special actions and stories.

**Buildings**, obviously, represent everything that the player can create
in his city. Games start with a set of **initial buildings**, and additional
ones can be **unlocked** through events. Initial and unlocked buildings
don't do anything by themselves - the player needs to place them on the map.
Usually, buildings need to be placed next to other buildings and cannot
be placed on water, although it is possible to create exceptions to those
rules. Generally, buildings should provide both benefits and costs, with
the player needing to balance his priorities - but it's better to err on
the side of making them too useful, as they're the player's most reliable
way of influencing the game.

**Events** represent CYOA/hypertext segments of the game in which
the player reads a portion of narrative text and then chooses an action
from a specified list (which cause changes in the player's city and/or
leads to more events). Events can be further divided into **non-random**
and **random**. The former will happen in a deterministic fashion when certain
conditions are met. They include storyline events which happen at specific
turns and disasters which happen when the city's stats get too low. Random
events can be picked at the beginning of each turn according to the desires
of our cruel RNG - but only if they're **active**. Some events will always
be active, others will switch between active and **inactive** state
depending on specified conditions. Once a random event is spawned, it is
then discarded and it will not be spawned again. Usually, you'll want
to err on the side of making events' outcomes more negative than positive,
as they should force the players to adapt to them.

**Special actions** are simple: they're events that can be activated at will
by the player. Special actions can be either initial or unlocked just like
buildings, and you can additionally set a **limit** on how often the action
can be used. Generally, the more powerful the action, the more limited it
should be.

**Stories** are the major branches (or 'paths' in the visual novel jargon,
but I'm not sure if On The Hill qualifies as a VN so I'll use my own term)
of the game's plot which lead to different endings. Stories are mutually
exclusive: at one point in the game, the appropriate story will be picked
depending on specified conditions. All the other ones will be ignored.

//TODO: actual technical details