"""Module for text-based/CYOA events"""
class TextEventPrototype:
    def __init__(self):
        self.title = "Test event"
        self.description = "Something happens"
        self._actions = {'OK': lambda state: None}
        self.should_be_activated   = lambda state: True
        self.should_be_deactivated = lambda state: False

    def get_actions(self):
        ret = []
        for action in self._actions:
            ret.append(action)
        return ret

    def perform_action(self, action, state):
        return self._actions[action](state)


def get_basic_random_events():
    return [TextEventPrototype(), TextEventPrototype(), TextEventPrototype()]