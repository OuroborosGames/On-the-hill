import buildings
import text_events
import terrain
import special_actions
import load_data
from copy import copy
from game_errors import GameplayError, InternalError, GameOver
from collections import deque
from random import randint, shuffle
from timers_and_counters import Counter
from math import floor


class GameFacade:
    """Facade class through which the GUI interfaces with the backend"""
    # TODO: create the interface
    def __init__(self, city_name, map_h=0, map_w=0):
        if map_h != 0 and map_w != 0:
            self._game = Game(city_name, map_h, map_w)
        else:
            self._game = MaplessGame(city_name)


class Game:
    """This used to be a facade but now it's game's global state"""

    def __init__(self, city_name, map_h, map_w):
        self.city_name = city_name
        self.game_over = False

        # turn number
        self.turn = 1

        # set main stats
        self.money = 1000
        self.population = 20

        # set additional stats
        self.prestige = 0
        self.safety = 0
        self.technology = 0
        self.food = 100
        self.health = 0
        self.population_max = 0

        # make map
        # MAP_WIDTH = 100
        # MAP_HEIGTH = 100
        # self.map = [[0 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGTH)]
        # self.map = terrain.MapPrototype(MAP_HEIGTH,MAP_WIDTH)
        self.map = terrain.SimplexNoiseMap(map_h, map_w)

        # actions per turn
        self._actions_max = 3
        self.actions = self._actions_max

        # list of buildings on the map (so we don't have to iterate through the whole map to apply per-turn effects)
        self.buildings_on_map = []

        # list of buildings that the player can construct
        self.buildings_deck = load_data.get_initial_buildings()

        # events that must be handled before taking an action or ending a turn (with get_next_event() method)
        self._event_queue = deque()

        # available random events (each turn, there is a chance that one of them will be added to _event_queue)
        self._event_active_deck = deque(text_events.get_basic_random_events())

        # random events not yet unlocked
        self._event_inactive_deck = []

        # special actions that the player can perform
        self.special_actions = special_actions.get_basic_actions()

        # events that will be triggered deterministically when a condition is met
        # self.nonrandom_events = load_data.get_nonrandom_events() #TODO: nonrandom.json
        self.nonrandom_events = []

        # list of timers
        self.timers = []

        # count in-game objects
        self.counter = Counter()

        # current branch in the main storyline
        self.branch = "The Founding of " + self.city_name

        # you must build town square in standard game mode
        self.founded = False

    def found(self, x, y):
        if self.founded:
            raise InternalError("Already founded")
        town_square = buildings.CustomBuilding("Town square", "Central part from which the rest of the city grows.",
                                               0, {}, {}, lambda tile: not buildings.is_on_water_tile(tile))
        if not town_square.can_be_built(self.map.get_field_by_coordinates(x, y)):
            raise GameplayError("Town square can't be built on water")
        self.map.add_building(town_square, x, y)
        self.buildings_on_map.append(town_square)
        self.founded = True

    def perform_special_action(self, number):
        self._try_performing_action()
        # spawn an event provided by a special action, remove the action if it can't be performed
        action = self.special_actions[number]
        try:
            self._event_queue.append(action.perform_action())
            if action.should_be_removed():
                raise InternalError
        except InternalError:
            self.special_actions.remove(action)

    def build(self, number, x, y):
        # initial requirements checks
        self._try_performing_action()

        if not self.buildings_deck[number].can_be_built(
               self.map.get_field_by_coordinates(x, y),
               self.map.get_neighbors(x, y)):
            self.actions += 1
            raise GameplayError("This building cannot be created here")

        new_building = copy(self.buildings_deck[number])  # buildings on map must not be references to buildings in deck
        self.map.add_building(new_building, x, y)         # so that changes to their attributes (e.g. price being
                                                          # modified depending on terrain) don't affect other instances
        if self.money < new_building.price:
            self.map.remove_building(x, y)
            self.actions += 1
            raise GameplayError("You don't have enough money to build here")

        self.buildings_on_map.append(new_building)
        self.money -= new_building.price
        # building-specific actions
        new_building.on_build(self)

    def demolish(self, x, y):
        self._try_performing_action()
        ref = self.map.get_field_by_coordinates(x, y).building
        if not ref:
            self.actions += 1
            raise GameplayError("Nothing to destroy!")
        self.map.remove_building(x, y)
        self.buildings_on_map.remove(ref)
        ref.on_destroy(self)

    def get_next_event(self):
        if not self._event_queue:
            return
        return self._event_queue.popleft()

    def end_turn(self):
        if not self.founded:
            raise InternalError("You must build a town square before doing that.")
        if self._event_queue:
            raise GameplayError("You still have unhandled events.")
        if self.game_over:
            raise GameOver()
        self.actions = self._actions_max
        self.turn += 1
        if self.population <= 0:
            self.game_over = True

        # per-turn stat modifications
        self._modify_stats()

        # upkeep/per-turn building effects
        for x in self.buildings_on_map:
            # self.money -= x.upkeep_cost
            x.on_next_turn(self)

        # perform non-random events if the condition is met
        for event in filter(lambda e: e.should_be_activated(self), self.nonrandom_events):
            self._event_queue.append(event)

        # lock/unlock random events depending on conditions
        move_between_lists(self._event_inactive_deck, self._event_active_deck, lambda a: a.should_be_activated(self))
        move_between_lists(self._event_active_deck, self._event_inactive_deck, lambda a: a.should_be_deactivated(self))

        # randomly take events from active deck
        if self._event_active_deck:
            # print("aaaaaa")
            if randint(1, 10) == 10:
                shuffle(self._event_active_deck)
                self._event_queue.append(self._event_active_deck.popleft())
                # print(self._event_queue[0])

        # countdown
        for t in self.timers:
            try:
                t.next(self)
            except InternalError:
                self.timers.remove(t)

    def _try_performing_action(self):
        # common functionality for all actions
        if self.game_over:
            raise GameOver()
        if not self.founded:
            raise InternalError("You must build a town square before doing that.")
        if self._event_queue:
            raise GameplayError("You still have unhandled events.")
        if not self.actions:
            raise GameplayError("You don't have enough actions left.")
        self.actions -= 1

    def _modify_stats(self):
        self.food -= self.population               # 1 food/person*turn
        if self.food < 0:
            self.population += floor(self.food/2)  # starvation
            self.food = 0
        modifier = 2                               # base birthrate
        modifier += self.prestige                  # people come if our city is prestigious and leave if it isn't
        if self.safety < 0:
            modifier += self.safety                # violence
        if self.health < 0:
            if self.technology < 5:
                modifier += self.health            # disease
            elif self.technology < 7:
                modifier += self.health/2          # better technology = diseases less deadly
            else:
                modifier += self.health/3
        if self.technology < 5:                    # better technology = more actions can be performed per-turn
            self._actions_max = 3
        elif self.technology < 10:
            self._actions_max = 4
        else:
            self.actions_max = 5

        self.population += floor(self.population*(modifier/100))


class MaplessGame(Game):
    """Game mode without map (experimental)"""
    def __init__(self, city_name):
        super(MaplessGame, self).__init__(city_name, 0, 0)
        self.map = None
        self.founded = True

    def build(self, number, x=0, y=0):
        self._build(number)

    def _build(self, number):
        self._try_performing_action()
        if self.money < self.buildings_deck[number].price:
            self.actions += 1
            raise GameplayError("You don't have enough money to create this building.")
        new_building = copy(self.buildings_deck[number])
        self.buildings_on_map.append(new_building)
        self.money -= new_building.price
        new_building.on_build(self)

    def demolish(self, x, y):
        raise InternalError("You can't demolish by coordinates in mapless mode!")

    def demolish_by_index(self, number):
        self._try_performing_action()
        ref = self.buildings_on_map[number]
        self.buildings_on_map.remove(ref)
        ref.on_destroy()

    def found(self, x, y):
        raise InternalError("This feature is absent from mapless mode")


def move_between_lists(source, dest, func):
    temp = filter(func, source)
    for t in temp:
        source.remove(t)
        dest.append(t)
