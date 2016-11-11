
class BuildingPrototype:
    def __init__(self):
        #TODO: better constructor
        self.name = 'Test building'
        self.base_price = 100
        self.price = self.base_price
        self.upkeep_cost = 10
        self.additional_effects = {'health' : 0, 'technology': 0, 'prestige': 0, 'food': 0, 'safety': 0}

    def can_be_built(self, map_tile, neighbors):
        return True

    def _modify_state_attributes(self, state, func):
        # lambdas and reflection, fuck yeah
        for effect in self.additional_effects:
            setattr(state, effect, func(getattr(state, effect), self.additional_effects[effect]))

    def on_build(self, state):
        # add semi-permanent effects when building
        self._modify_state_attributes(state, lambda x, y: x + y)

    def on_destroy(self, state):
        # remove semi-permanent effects when destroying
        self._modify_state_attributes(state, lambda x, y: x - y)



def get_initial_buildings():
    #TODO: make basic buildings and return a list of them
    return [BuildingPrototype()]