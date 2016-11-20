from game_errors import GameplayError

class TerrainType:
    def __init__(self, name, cost_modifier):
        self.name = name
        self.cost_modifier = cost_modifier
        self.building = None

class MapPrototype:
    def __init__(self, h, w):
        self.heigth = h
        self.width = w
        self._map_internal = [[TerrainType("Test", 1) for x in range(self.width)] for y in range(self.heigth)]

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
            for j in range(-1,1):
                if x+i >= 0 and y+j >= 0:
                    ret.append(self.get_field_by_coordinates(x+i,y+j))
        return ret
