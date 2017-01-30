On The Hill GUI Developer's Guide
=================================

1. Introduction
---------------

This is a guide to writing GUI code for On The Hill. It is **not**
a comprehensive API reference but it should be enough to get you
familiarized with the public interface exposed by the backend. It should
also help the developer understand how the player is supposed to
interact with the game, which is crucial to creating a good GUI.

2. Starting the game
---------------------------------

Before we do anything, we must first create an object to hold the game's
backend. You can do it this way:

```python
import oth_core
backend = oth_core.GameBackend()
```

Now, we must create an actual game. A user should be able to start from
scratch or continue a previously saved game.

```python
# start a game; name of the city MUST be provided by the user
# height and width of the map SHOULD be provided by the user (although
# your implementation may restrict the choice to a range you consider
# sensible)
backend.new_game(city_name, height, width)

# (...)

# start a game in mapless mode (keep on reading for explanation)
# name of the city MUST be provided by the user
backend.new_mapless_game(city_name)

# (...)

# load a previously saved game; user's choice MAY be restricted to
# predefined save-slots but if the GUI developer decides otherwise,
# choice of saveifles SHOULD be restricted to predefined directories
# and/or file extensions
backend.load_game(filename + '.sav')
```

Keep in mind that load_game() method will deserialize Python objects.
While this should not be a problem if the user runs the game on his
own machine (after all, if savefiles can be modified maliciously then
so can be the game's script), **it will cause vulnerabilities if the
game is run on a server and the user can upload his own savefiles**.
Keep that in mind if you want to make a web frontend (but I don't know
why you would do that given that so far it's a single-player game).

3. Stopping the game
--------------------

The backend will not allow you to create a game when there is one
already in progress. This is because game-creating methods are
destructive: they overwrite the game already in progress. If you want
to accommodate the situation in which users want to abandon their
current game or load a previous savegame (e.g. a quicksave/quickload
feature or a pause menu), you must first call this method:

```python
# close current game; the player SHOULD be asked if he wants to save
# current progress before calling this method, unless it's executed
# through a quickload button
backend.close_game()
```

4. Displaying data to the player
--------------------------------

During the gameplay, player MUST be able to see basic stats necessary
to make strategic choices:

```python
# numerical values of following stats MUST be displayed
backend.money
backend.population
backend.population_max
backend.food

# those stats MAY be displayed in other way (e.g. graphical indicators
# or textual descriptions)
backend.prestige
backend.safety
backend.technology
backend.health
```

Additional information that SHOULD be shown to the player:
```python
backend.city_name # display value of this string

backend.turn      # either show the turn number or convert it to some
                  # other format (1 turn = 1 month)
```

Whenever possible, player SHOULD be able to see the city:
```python
city = backend.display_map()

# in normal mode, the returned map will have two layers: one for terrain
# and one for buildings
my_map_rendering_function(city[0]) # draw the terrain
my_map_rendering_function(city[1]) # draw the buildings

# in mapless mode, only the list of buildings constructed by the player
# is returned
my_background.draw_buildings(city)
```

The player MAY be shown the following items during the gameplay or they
MAY be hidden in a sub-menu:
```python
# list of buildings that the player can construct
backend.buildings_deck
## details about those buildings
building = backend.buildings_deck[i]
building.name               # string
building.description        # string
building.price              # int
building.additional_effects # dict (string:int)
building.per_turn _effects  # dict (string:int)
## more advanced features (normal mode only):
### boolean: can I put this building on that tile?
building.can_be_built(backend.map.get_field_by_coordinatea(x,y),
                      backend.map.get_neighbors(x,y))
### int: cost of building on a specific tile
building.price * backend.map.get_field_by_coordinates(x,y).cost_modifier

# list of special actions which can be executed by the user:
backend.special_actions
## details about those actions
action = backend.special_actions[i]
action.name
action.description
```

Everything else is internal data and SHOULD NOT be displayed to the
player.

5. Gameplay proper
------------------

### 5.1. Founding the city (normal mode only)

Almost all of the buildings in On The Hill must be built next to other
buildings. For that reason, right after starting the game in normal mode
the player should be given the choice of where to found the city. Any
non-water tile can be chosen, after which you must pass the tile's
coordinates to the found() method:

```python
backend.found(input_x, input_y)
```

When waiting for the player input, either the tiles on which the city
can be founded SHOULD be highlighted (e.g. by applying a green tint to
them) or the ones on which it can't SHOULD be 'hidden' (e.g. by graying
them out).

### 5.2. Text-based events

Text-based events take precedence over everything else and if they're
not handled before the player tries to execute any other action,
an InternalError will be raised.

Handling of text-based events is best done in a while loop (foreach
might have been more elegant but while seems to be a safer choice when
size of the list is mutable; I might be wrong about that though so feel
free to correct me):

```python
while backend.has_next_event():
    ev = backend.get_next_event()
    # (...)
    # display this to the player:
    ev.title                   # string
    ev.description             # string
    ev.get_actions()           # list of strings
    
    # now handle player choice:
    input = my_get_input_from_player(keys)
    backend.event_choice(ev, input)
```

Keep in mind that the result of my_get_input_from_player() must be
a valid key from ev.actions. For that reason, in your input-handling
function you should restrict user choice to those values (e.g. by
drawing a button for each key and returning which one was pressed).

### 5.3. Building and demolishing

Selecting the building from a list of buildings that can be constructed
(see point 3.) MUST allow the player to initiate building procedure,
while selecting one from the output of display_map() MUST allow the same
for demolition. The procedures depend on game mode.

#### 5.3.1. Normal mode

When the building is picked from buildings_deck, the player SHOULD be
able to see where it can be built (see point 4. for how to check
and point 5.1. for implementation suggestions). He SHOULD also be able
to see the price adjusted for terrain's cost_modifier (also see point
4.). When player picks a field on the map, call the following function
to perform the action:

```python
# pass building's index in buildings_deck and user-specified coordinates
backend.build(index, input_x, input_y)
```

When the building is picked from the output of display_map(), the player
should be given an option (e.g. by showing a button) to demolish it.
When a choice is made, call the following function:

```python
# to demolish a building, pass its coordinates to this function:
backend.demolish(input_x, input_y)
```

#### 5.3.2. Mapless mode

In mapless mode, there's no need (and no way) to show where the building
can be built or calculate new price. For this reason, it is enough to
give the player an option the same way it's done when demolishing in
normal mode:

```python
# there's no map so you don't need to pass coordinates, just index
# if you pass them, they'll be ignoted
backend.build(index)
```

Demolition works by selecting the building from the output of
display_map(), but the method you need to call is different and it takes
selection's index instead of coordinates:

```python
backend.demolish_by_index(index)
```

### 5.4. Special actions

//todo