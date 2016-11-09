
class BuildingPrototype:

    def __init__(self):
        #TODO: better constructor
        self.name = 'Test building'
        self.base_price = 100
        self.price = self.base_price
        self.upkeep_cost = 10
        self.additional_effects = {'health' : 0, 'technology': 0, 'prestige': 0, 'food': 0, 'safety': 0}

   # def build(self, x, y, state):
   #      if not state.actions:
   #          print('Nie możesz nic zrobić w tej turze')
   #          return
   #
   #      if state.money < self.base_price:
   #          print('Nie stać cię cebulaku xd')
   #          return
   #
   #      state.money -= self.base_price
   #      state.actions -= 1
   #      state.buildings.append(self)
   #      print('Zbudowałeś')
   #      return

def get_initial_buildings():
    #TODO: make basic buildings and return a list of them
    return [BuildingPrototype()]