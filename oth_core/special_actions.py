from oth_core.game_errors import InternalError


"""Special actions are events that can be triggered directly by the player, as opposed to being spawned randomly
or semi-randomly. Internally, they work by having an 'event' slot, which finally ends up in game state's event queue.
For this reason, it should preferably contain an instance of BasicEvent, although obviously it can be anything that
has the same interface (minus the should_be_activated() and should_be_deactivated() function as the event never ends
up in the active or inactive deck."""


class SpecialAction(object):
    def __init__(self, name, description, event_to_spawn):
        self.name = name
        self.description = description
        self.event = event_to_spawn

    def perform_action(self):
        return self.event

    def should_be_removed(self):
        return False


class LimitedSpecialAction(SpecialAction):
    """LimitedSpecialAction can be used a predetermined number of times"""

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
