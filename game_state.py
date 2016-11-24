import buildings
import text_events
import terrain
import special_actions
from copy import copy
from game_errors import GameplayError, InternalError, GameOver
from collections import deque
from random import randint, shuffle
from timers_and_counters import Counter
from math import floor


class Game:
    """Facade class used as an interface to control the game backend"""

    def __init__(self):
        self.city_name = "Test City"
        self.game_over = False

        # turn number
        self.turn = 1

        # set main stats
        self.money = 1000
        self.population = 100

        # set additional stats
        self.prestige = 0
        self.safety = 0
        self.technology = 0
        self.food = 0
        self.health = 0

        # make map
        MAP_WIDTH = 100
        MAP_HEIGTH = 100
        # self.map = [[0 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGTH)]
        # self.map = terrain.MapPrototype(MAP_HEIGTH,MAP_WIDTH)
        self.map = terrain.SimplexNoiseMap(MAP_HEIGTH,MAP_WIDTH)

        # actions per turn
        self._actions_max = 3
        self.actions = self._actions_max

        # list of buildings on the map (so we don't have to iterate through the whole map to apply per-turn effects)
        self.buildings_on_map = []

        # list of buildings that the player can construct
        self.buildings_deck = buildings.get_initial_buildings()

        # events that must be handled before taking an action or ending a turn (with get_next_event() method)
        self._event_queue = deque()

        # available random events (each turn, there is a chance that one of them will be added to _event_queue)
        self._event_active_deck = deque(text_events.get_basic_random_events())

        # random events not yet unlocked
        self._event_inactive_deck = []

        # special actions that the player can perform
        self.special_actions = special_actions.get_basic_actions()

        # list of timers
        self.timers = []

        # count in-game objects
        self.counter = Counter()

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
        if self.money < self.buildings_deck[number].base_price:
            self.actions += 1
            raise GameplayError("You don't have enough money to create this building.")
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
        if self._event_queue:
            raise GameplayError("You still have unhandled events.")
        if self.game_over:
            raise GameOver()
        self.actions = self._actions_max
        self.turn += 1
        if self.population <= 0:
            self.game_over = True

        for x in self.buildings_on_map:
            # self.money -= x.upkeep_cost
            x.on_next_turn(self)

        # lock/unlock random events depending on conditions
        move_between_lists(self._event_inactive_deck, self._event_active_deck, lambda a: a.should_be_activated(self))
        move_between_lists(self._event_active_deck, self._event_inactive_deck, lambda a: a.should_be_deactivated(self))

        if self._event_active_deck:
            # print("aaaaaa")
            if randint(1, 10) == 10:
                shuffle(self._event_active_deck)
                self._event_queue.append(self._event_active_deck.popleft())
                # print(self._event_queue[0])

        # if self.timers:
        for t in self.timers:
            try:
                t.next(self)
            except InternalError:
                self.timers.remove(t)
        # per-turn stat modifications
        self._modify_stats()

    def _try_performing_action(self):
        # common functionality for all actions
        if self.game_over:
            raise GameOver()
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
            self.technology = 4
        else:
            self.technology = 5

        self.population += floor(self.population*(modifier/100))


def move_between_lists(source, dest, func):
    temp = filter(func, source)
    for t in temp:
        source.remove(t)
        dest.append(t)
