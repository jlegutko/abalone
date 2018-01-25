from . import Player


class PlayerBlack(Player.Player):
    """
    Inherits from Player class.
    Stores data about a player playing black pieces.
    """
    def __init__(self):
        self.positions = {
            (8, 4, 0), (8, 5, 1), (8, 6, 2), (8, 7, 3), (8, 8, 4),
            (7, 3, 0), (7, 4, 1), (7, 5, 2), (7, 6, 3), (7, 7, 4), (7, 8, 5),
            (6, 4, 2), (6, 5, 3), (6, 6, 4)
        }
        self.pieces = len(self.positions)
