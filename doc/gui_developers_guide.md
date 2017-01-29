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

//todo: everything else