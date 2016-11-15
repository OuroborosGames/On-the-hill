"""Module for text-based/CYOA events"""
class TextEventPrototype:
    def __init__(self):
        self.title = "Test event"
        self.description = "Something happens"
        self._actions = {'OK': lambda state: None}

    def get_actions(self):
        ret = []
        for action in self._actions:
            ret.append(action)
        return ret

    def perform_action(self, action, state):
        return self._actions[action](state)

    def should_be_activated(self, state):
        return True

    def should_be_deactivated(self, state):
        return False

def get_basic_random_events():
    return [TextEventPrototype(), TextEventPrototype(), TextEventPrototype()]