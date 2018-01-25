from . import Player


class PlayerWhite(Player.Player):
    """
    Inherits from Player class.
    Stores data about a player playing white pieces.
    """
    def __init__(self):
        self.positions = {
            (0, 0, 4), (0, 1, 5), (0, 2, 6), (0, 3, 7), (0, 4, 8),
            (1, 0, 3), (1, 1, 4), (1, 2, 5), (1, 3, 6), (1, 4, 7), (1, 5, 8),
            (2, 2, 4), (2, 3, 5), (2, 4, 6)
        }
        self.pieces = len(self.positions)
