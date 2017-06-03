from oth_core.game_errors import InternalError


class BasicTimer(object):
    """Basic timer: executes a function after a set number of turns"""
    def __init__(self, turns_to_wait, end):
        self.turns_to_wait = turns_to_wait
        self.end = end

    def next(self, state):
        if self.turns_to_wait > 0:
            self.turns_to_wait -= 1
        elif self.turns_to_wait < 0:
            raise InternalError()
        else:
            self.end(state)


class BasicEventTimer(BasicTimer):
    """Spawns event after a set number of turns"""
    def __init__(self, turns_to_wait, event_to_spawn):
        self.turns_to_wait = turns_to_wait
        self.event_to_spawn = event_to_spawn

    def next(self, state):
        if self.turns_to_wait > 0:
            self.turns_to_wait -= 1
        elif self.turns_to_wait < 0:
            raise InternalError()
        else:
            state._event_queue.append(self.event_to_spawn)


class Counter(object):
    """A simple counter implementation, mostly meant for counting how many buildings of certain type have been built by
    the player. Text events 'know' how to communicate with the counter so it can also be used to indicate progress
    in event chains or just as a lock/unlock condition."""

    def __init__(self):
        self._counter = {}

    def get_count(self, key):
        if key not in self._counter:
            return 0
        return self._counter[key]
    
    def reset(self, key):
        if key not in self._counter:
            return
        del self._counter[key]

    def increment(self, key):
        if key not in self._counter:
            self._counter.update({key: 1})
            return
        self._counter[key] += 1

    def decrement(self, key):
        if key not in self._counter:
            return
        if self._counter[key] <= 0:
            return
        self._counter[key] -= 1


class Flags(Counter):
    """Binary flags for game state. Technically inherits from Counter but you shouldn't use Counter's methods,
    just set/unset/isset"""

    def set(self, flag):
        self.increment(flag)

    def unset(self, flag):
        self.reset(flag)

    def isset(self, flag):
        if self.get_count(flag): return True
        return False