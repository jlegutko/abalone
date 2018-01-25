from . import Board
from . import PlayerBlack
from . import PlayerWhite


class Game:
    def __init__(self, name):
        self.name = name
        self.board = Board.Board()
        self.rows = self.board.rows
        self.columns = self.board.columns
        self.player_black = PlayerBlack.PlayerBlack()
        self.player_white = PlayerWhite.PlayerWhite()

