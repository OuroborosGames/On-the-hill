from random import randint

from oth_core.game_errors import GameplayError
from oth_core.perlin import SimplexNoise
from functools import partial


class TerrainType(object):
    def __init__(self, name, cost_modifier):
        self.name = name
        self.cost_modifier = cost_modifier
        self.building = None


class MapPrototype(object):
    """Map of the game area. Contains methods for adding (as long as the field is unoccupied) and removing buildings
    as well as getters for specific fields.

    WARNING: This class should only be used for testing purposes as it doesn't have any actual terrain or procedural
    generation."""

    def __init__(self, h, w):
        self.heigth = h
        self.width = w
        self._map_internal = self._generate_map(h, w)

    def add_building(self, building, x, y):
        if self._map_internal[x][y].building:
            raise GameplayError("There is already a building here!")
        self._map_internal[x][y].building = building
        building.price *= self._map_internal[x][y].cost_modifier

    def remove_building(self, x, y):
        self._map_internal[x][y].building = None

    def get_field_by_coordinates(self, x, y):
        return self._map_internal[x][y]

    def get_neighbors(self, x, y):
        ret = []
        for i in range(-1, 1):
            for j in range(-1, 1):
                if x+i >= 0 and y+j >= 0:
                    ret.append(self.get_field_by_coordinates(x+i, y+j))
        return ret

    def get_terrain_layer(self):
        return [[field.name for field in row] for row in self._map_internal]

    def get_buildings_layer(self):
        return [[field.building for field in row]
                for row in self._map_internal]

    @classmethod
    def _generate_map(cls, h, w):
        return [[TerrainType("Test", 1) for x in range(w)] for y in range(h)]


class SimplexNoiseMap(MapPrototype):
    """Procedurally generated map based on simplex noise algorithm"""

    water     = partial(TerrainType, "Water",     1)
    grass     = partial(TerrainType, "Grass",     1)
    forest    = partial(TerrainType, "Forest",    1.5)
    hills     = partial(TerrainType, "Hills",     1.2)
    mountains = partial(TerrainType, "Mountains", 2)
    
    @classmethod
    def _generate_map(cls, h, w):
        noise = SimplexNoise(randint_function=randint)
        return [[cls.get_terrain_from_noise(noise.noise2(x, y)) for x in range(w)] for y in range(h)]
    
    @classmethod
    def get_terrain_from_noise(cls, value):
        if value < -0.5:
            return cls.water()
        elif value < 0:
            return cls.grass()
        elif value < 0.2:
            return cls.forest()
        elif value < 0.5:
            return cls.hills()
        return cls.mountains()


# def get_terrain_from_noise(value):
#     if value < -0.5:
#         return TerrainType("Water", 1)
#     elif value < 0:
#         return TerrainType("Grass", 1)
#     elif value < 0.2:
#         return TerrainType("Forest", 1.5)
#     elif value < 0.5:
#         return TerrainType("Hills", 1.2)
#     return TerrainType("Mountains", 2)
