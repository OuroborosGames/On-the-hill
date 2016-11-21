from game_errors import InternalError


class BasicTimer:
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
            self._end(state)

    def _end(self, state):
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


class Counter:
    def __init__(self):
        self._counter = {}

    def increment(self, key):
        if key in self._counter:
            self._counter[key] += 1
        else:
            self._counter.update({key: 1})

    def decrement(self, key):
        if key not in self._counter:
            return
        if self._counter[key] <= 0:
            return
        self._counter[key] -=1
        
    def get_count(self, key):
        if key not in self._counter:
            return 0
        return self._counter[key]
