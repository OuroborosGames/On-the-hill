import buildings
import text_events
import terrain
from game_errors import GameplayError
from collections import deque
from random import randint

class Game:
    """Facade class used as an interface to control the game backend"""

    def __init__(self):
        #turn number
        self.turn = 1

        #set main stats
        self.money = 1000
        self.population = 100

        #set additional stats
        self.prestige = 0
        self.safety = 0
        self.technology = 0
        self.food = 0
        self.health = 0

        #make map
        MAP_WIDTH = 100
        MAP_HEIGTH = 100
        # self.map = [[0 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGTH)]
        self.map = terrain.MapPrototype(MAP_HEIGTH,MAP_WIDTH)

        #actions per turn
        self._actions_max = 3
        self.actions = self._actions_max

        #list of buildings on the map
        self.buildings_on_map = []

        #list of buildings that the player can construct
        self.buildings_deck = buildings.get_initial_buildings()

        #events that must be handled before taking an action or ending a turn (with get_next_event() method)
        self._event_queue = deque()

        #available random events (each turn, there is a chance that one of them will be added to _event_queue)
        self._event_deck = deque(text_events.get_basic_random_events())

    def build(self, number):
        if self._event_queue:
            raise  GameplayError("You still have unhandled events.")
        if not self.actions:
            raise GameplayError("You don't have enough actions left.")
        if self.money < self.buildings_deck[number].base_price:
            raise GameplayError("You don't have enough money to create this building.")
        self.actions -= 1
        self.money -= self.buildings_deck[number].base_price

    def get_next_event(self):
        if not self._event_queue:
            return
        return self._event_queue.popleft()

    def end_turn(self):
        if self._event_queue:
            raise  GameplayError("You still have unhandled events.")
        self.actions = self._actions_max
        self.turn += 1
        for x in self.buildings_on_map:
            self.money -= x.upkeep_cost
        if self._event_deck:
            # print("aaaaaa")
            if randint(1,10) == 10:
                self._event_queue.append(self._event_deck.popleft())
                # print(self._event_queue[0])
