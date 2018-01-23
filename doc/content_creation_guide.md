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
\- and that means that sometimes you'll need to use ```def```, which breaks
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

3. Project structure
--------------------

When creating content, the only directories you should be worried about are
```On-the-hill/base-content/``` and ```On-the-hill/stories/```. The former
consists of things that are universal to the whole game, the latter defines
content specific for different stories (i.e. branches/paths).

```On-the-hill/base-content/actions.py``` and ```On-the-hill/base-content/buildings.py```
files are straightforward: they define special actions and buildings that
will be available to the player from the start of the game. They do so in
a fairly straight-forward manner: through ```get_initial_special_actions()```
and ```get_initial_buildings()``` function. Those functions return lists, and
you can alter what the player gets at the beginning of the game by modifying
the lists' content. ```On-the-hill/base-content/disasters.py``` is similar:
it returns a list with its ```get_disasters()``` function, and that list
determines the non-random events that will fire when the player's stats get
too low.

```On-the-hill/base-content/dispatcher_event.py``` contains a definition of
a special class which will be instantiated once during the game: the constructor
receives a list of ```(get_story, predicate)``` tuples that define stories,
and the object it creates is an event that will check ```predicate(state)``` and
will spawn ```get_story()``` event if it's true (but **only once**). This is used
for choosing the story branch to enter and you probably shouldn't modify it,
unless you want to create some custom 'story precedence', or maybe create/change
a default story for when no predicates are true.

```On-the-hill/base-content/early_game_events.py``` and ```On-the-hill/base-content/mid_game_events.py```
are a bit more complex, as they're more related to scripting the game's story.
They both define ```get_random_events()``` and ```get_nonrandom_events()``` which
return lists of events that will be added to appropriate decks (the first one at
the beginning, the second one after 10 years), but due to the nature of the events
as both a narrative mechanism and means of modifying the game, the events returned
by those functions also refer to other events they activate as well as buildings
and actions they unlock. For that reason, those files allow you not only to modify
the events you can find during those portions of the game but also other pieces
of content that gets unlocked as their result.

Each file in ```On-the-hill/stories/``` is similar to those that define early
and mid-game events in that it contains chains of events and gameplay objects related
to them, although they do it in different ways: each of those file defines a separate
branch (so branches can be added/deleted automatically just by creating and removing
those files) through ```get()``` and ```should_enter_branch(state)``` functions it
defines. Those functions are the ```get_story()``` and ```predicate(state)``` from
dispatcher event: the first one returns the story's first event, the second one checks
if conditions for entering the branch have been satisfied.

4. Buildings and actions
------------------------

### 4.1. Buildings

When working with buildings, make sure that this backend module is imported:
```from oth_core.buildings import *```

This module defines three classes of buildings: BasicBuilding, TerrainRestrictedBuilding
and CustomBuilding. Those classes are instantiated through constructors that take at
least this data:

```python
BasicBuilding(
    name="This is a string",
    description="This is also a string",
    base_price=0  # this is an int,
    additional_effects={'keys are strings': 0  # values are ints
                       },                      # the whole thing is a dict
    per_turn_effects={'this works just like the previous one': 0}
)
TerrainRestrictedBuilding(
    name="This is a string",
    description="This is also a string",
    base_price=0  # this is an int
    additional_effects={'keys are strings': 0  # values are ints
                       },                      # the whole thing is a dict
    per_turn_effects={'this works just like the previous one': 0},
    required_neighbor='string again'
)
CustomBuilding(
    name="This is a string",
    description="This is also a string",
    base_price=0  # this is an int
    additional_effects={'keys are strings': 0  # values are ints
                       },                      # the whole thing is a dict
    per_turn_effects={'this works just like the previous one': 0},
    predicate=lambda map_tile, neighbors: True  # this is a function
)
```
The first two arguments should be self-explanatory. The third one is simple: it's
the building's price before applying terrain modifiers (as some types of terrain make
building on them more expensive). The fourth and fifth might require a bit mor explanation.

Keys to the dictionaries are strings, and they represent attributes of the object that
holds the game state. The values of those keys will be added (subtracted if negative)
to the respective attributes when player creates the building and the alteration will be
reversed when removing it, or they will be applied repeatedly with each turn, and
the alterations will be stopped (but not reversed) when it is removed. Figuring out which
dict does which is left as an exercise to the reader.

'prestige', 'health', 'safety' and 'technology' are attributes which change things in the city
with each turn, therefore they work better when modified once - and so does 'population_max',
which determines the safe upper limit for 'population'. 'money' and 'food' can be modified
per-turn, and so can be 'population' (but I'd personally avoid increasing it per-turn,
as it can make the game too easy because it counteracts the negative effects of some of
the stats being too low). Modifying 'actions' doesn't make much sense, and because of
a backend quirk (resetting to default after turn ends), modifying 'actions_max' only
makes sense if done per-turn (but it should be done sparingly as it's a very significant
change). Modifying 'game_over' doesn't make much sense either, but it can be amusing.

The 'required_neighbor' argument makes it possible to create a building that must be
built on or next to a specified terrain feature. At the moment, those are 'Water',
'Grass', 'Forest', 'Hills' and 'Mountain'.

The 'predicate' argument allows specifying your own way of defining whether a building
can be built on a specified tile, based on the tile itself as well as its neighbor.
While BasicBuilding can be built anywhere as long as it's not on water and there are
other buildings in its neighborhood and TerrainRestrictedBuilding has an additional
restriction on neighboring terrain, this allows you to write your own condition.
The function that you pass will take two arguments: map_tile (a TerrainType object
that consists of 'name' which identifies terrain features, 'cost_modifier' which
affects prices and 'building' which tells you what has been placed here by the player)
and neighbors (a list of map_tiles next to your own), and it will return True or False.

To help you with creating a CustomBuilding, two functions were created:
```has_neighboring_buildings(neighbors)``` and ```is_on_water_tile(tile)```. They
should be self-explanatory. Keep in mind that you don't need to check if map_tile is
already taken: TerrainType enforces that you can't build on a non-empty tile, and this
behavior can't be overridden with this predicate.

### 4.2. Special actions

Special actions are very simple, as they're really just thin wrappers on events.
They work like this:

```python
from oth_core.special_actions import *

SpecialAction(
    name="This is a string",
    description="This is also a string",
    event_to_spawn=this_is_a_reference_to_an_event_object
)
SpecialAction(
    name="This is a string",
    description="This is also a string",
    event_to_spawn=this_is_a_reference_to_an_event_object,
    limit=1  # this is an int
)
```
The only thing you need to know now is that limit determines how many times
the player can use this action. Everything else is described in the section
about events.

5. Events
---------

The basics of events were described in section 3. but before we proceed, let's
recap:

+ events are text-based sections of the game in which the player reads event's
description and picks an appropriate action based on that
+ events can be random or non-random
+ random events can be active or inactive; only active events can be randomly picked
when turns begin, and transitions between active and inactive state happen based on
predicates
+ events can modify the game state by changing the player's stats, unlocking buildings
and actions and spawning other events

Now, let's start discussing details.

### 5.1. Understanding event's lifecycle

#### 5.1.1. Non-random events

The lifecycle of a non-random event is simple: once it gets added into the game, it will
**always** be spawned if its condition is satisfied after the turn ends (the event is
not discarded after being triggered). This behavior is not always desired, so you should
be aware of that when setting both conditions and effects (timers and flags are your
friends). Many of the non-random events are designed to only occur on a one specific turn
so this isn't really a big issue for them.

#### 5.1.2. Random events

Random events are a bit more complex because of a distinction between Basic, Unlockable
abd Conditional types. Once added, Basic events will always be active, Unlockable ones
will only become active after a condition is met and never become inactive, and Conditional
ones will switch between active and inactive state depending on the condition.

Events are added to the game by other events or at the beginning of a different stage of
the game: early-game, mid-game and any of the stories. The first two of the stages define
their own subtypes of ```ConditionalEvent```: ```EarlyGameEvent``` and ```MidGameEvent```,
that will become inactive once that part of the game is over. Stories don't define such
types because once you finish them, you get the ending and you're done with this game
session.

Now, the distinction between 'adding' an event and 'unlocking' it might seem academic,
but there is a performance-related difference: once an event is added, its lock/unlock
condition will be checked each turn, until discarded. This is probably not too important
but if you add a lot of events and the game becomes slow between turn, maybe think
about refactoring it so that event chains work by having one event add another instead
of one event setting flags and another checking conditions. Don't go out of your way
to make sure that it's always done this way if performance is good and readability would
suffer if you made those changes though.

Random events are discarded after they're handled, and they will not happen again.

//TODO: actual technical details about events and stories