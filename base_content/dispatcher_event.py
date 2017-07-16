from oth_core import text_events
from random import randint


def dispatch(stories):
    def action(state):
        for get_story, predicate in stories:
            if predicate(state):
                text_events.spawn_after_n_turns(state, get_story(), randint(12, 24))
                return
    return action


class DispatcherEvent(text_events.TextEventPrototype):
    def __init__(self, stories):
        super(DispatcherEvent, self).__init__()
        self.title = "Prophetic Dreams?"
        self.description = """One morning, you wake up with the feeling that the dream you had that night was
        not merely a dream but a detailed and vivid vision of the future. Unfortunately, all those details vanish
        from your mind as soon as you leave your bed. You remember only two things - first of all, the coming years
        will bring great changes to your city, remaking it into something you couldn't have possibly imagined when
        you founded it. The second is that after the city's fate is decided, you won't remain in charge."""
        self.actions = {'OK': dispatch(stories)}
        self.should_be_activated = lambda state: True if state.turn == 600 else False
