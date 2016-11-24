from game_errors import InternalError


class SpecialAction:
    def __init__(self, name, description, event_to_spawn):
        self.name = name
        self.description = description
        self.event = event_to_spawn

    def perform_action(self):
        return self.event

    def should_be_removed(self):
        return False


class LimitedSpecialAction(SpecialAction):
    def __init__(self, name, description, event_to_spawn, limit):
        super(LimitedSpecialAction, self).__init__(name, description, event_to_spawn)
        self.limit = limit

    def perform_action(self):
        if self.should_be_removed():
            raise InternalError
        self.limit -= 1
        super(LimitedSpecialAction, self).perform_action()

    def should_be_removed(self):
        if self.limit <= 0:
            return True
        return False


def get_basic_actions():
    return [SpecialAction("Test action", "You do something", None)]
