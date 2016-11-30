class BuildingPrototype:
    def __init__(self):
        # TODO: better constructor
        self.name = 'Test building'
        self.description = ''
        self.base_price = 100
        self.price = self.base_price
        # self.upkeep_cost = 10
        self.additional_effects = {'health': 0, 'technology': 0, 'prestige': 0, 'food': 0, 'safety': 0}
        self.per_turn_effects = {'money': - 10}  # upkeep cost moved to per_turn_effects

    @staticmethod
    def can_be_built(map_tile, neighbors):
        return True

    def on_build(self, state):
        # add semi-permanent effects when building
        self._modify_state_attributes(state, self.additional_effects, lambda x, y: x + y)
        state.counter.increment(self.name)

    def on_destroy(self, state):
        # remove semi-permanent effects when destroying
        self._modify_state_attributes(state, self.additional_effects, lambda x, y: x - y)
        state.counter.decrement(self.name)

    def on_next_turn(self, state):
        self._modify_state_attributes(state, self.per_turn_effects, lambda x, y: x + y)

    @staticmethod
    def _modify_state_attributes(state, effects, func):
        # lambdas and reflection, fuck yeah
        for effect in effects:
            setattr(state, effect, func(getattr(state, effect), effects[effect]))


class BasicBuilding(BuildingPrototype):
    def __init__(self, name, description, base_price, additional_effects, per_turn_effects):
        super(BasicBuilding, self).__init__()
        self.name = name
        self.description = description
        self.base_price = base_price
        self.additional_effects = additional_effects
        self.per_turn_effects = per_turn_effects

    @staticmethod
    def can_be_built(map_tile, neighbors):
        return has_neighboring_buildings(neighbors) and not is_on_water_tile(map_tile)


class TerrainRestrictedBuilding(BasicBuilding):
    def __init__(self, name, description, base_price, additional_effects, per_turn_effects, required_neighbor):
        super(TerrainRestrictedBuilding, self).__init__(
            name, description, base_price, additional_effects, per_turn_effects)
        self.required_tile = required_neighbor

    def can_be_built(self, map_tile, neighbors):
        if not super(TerrainRestrictedBuilding, self).can_be_built(map_tile, neighbors):
            return False
        for n in neighbors:
            if n.name == self.required_tile:
                return True
        return False


class CustomBuilding(BasicBuilding):
    def __init__(self, name, description, base_price, additional_effects, per_turn_effects, build_predicate):
        super(CustomBuilding, self).__init__(name, description, base_price, additional_effects, per_turn_effects)
        self.can_be_built = build_predicate


def get_initial_buildings():
    # TODO: make basic buildings and return a list of them
    return [BuildingPrototype()]


def has_neighboring_buildings(neighbors):
    for n in neighbors:
        if n.building:
            return True
    return False


def is_on_water_tile(tile):
    if tile.name == "Water":
        return True
    return False
