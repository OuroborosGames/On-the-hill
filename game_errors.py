class GameplayError(Exception):
    """General class for gameplay errors (e.g. you don't have enough money to perform an action)"""
    pass

class InternalError(Exception):
    """Errors used internally by the game engine"""
    pass