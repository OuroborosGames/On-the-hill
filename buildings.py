
class BuildingPrototype:
    def __init__(self):
        #TODO: better constructor
        self.name = 'Test building'
        self.base_price = 100
        self.price = self.base_price
        #self.upkeep_cost = 10
        self.additional_effects = {'health' : 0, 'technology': 0, 'prestige': 0, 'food': 0, 'safety': 0}
        self.per_turn_effects   = {'money': - 10}  # upkeep cost moved to per_turn_effects

    def can_be_built(self, map_tile, neighbors):
        return True

    def on_build(self, state):
        # add semi-permanent effects when building
        self._modify_state_attributes(state, self.additional_effects, lambda x, y: x + y)

    def on_destroy(self, state):
        # remove semi-permanent effects when destroying
        self._modify_state_attributes(state, self.additional_effects, lambda x, y: x - y)

    def on_next_turn(self, state):
        self._modify_state_attributes(state, self.per_turn_effects, lambda x, y: x + y)

    def _modify_state_attributes(self, state, effects, func):
        # lambdas and reflection, fuck yeah
        for effect in effects:
            setattr(state, effect, func(getattr(state, effect), effects[effect]))


def get_initial_buildings():
    #TODO: make basic buildings and return a list of them
    return [BuildingPrototype()]