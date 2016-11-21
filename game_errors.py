class GameplayError(Exception):
    """General class for gameplay errors (e.g. you don't have enough money to perform an action)"""
    pass


class GameOver(Exception):
    """Special exception for when the game has been lost or finished"""
    pass


class InternalError(Exception):
    """Errors handled internally by the game engine"""
    pass
