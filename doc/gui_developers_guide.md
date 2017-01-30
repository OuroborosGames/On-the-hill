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

### 5.1. Text-based events

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

//todo: everything else