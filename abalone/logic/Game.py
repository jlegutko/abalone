import pickle
from time import time
from math import fabs
from . import Board
from . import PlayerBlack
from . import PlayerWhite


class Game:

    def __init__(self, game_id, name, creator):

        self.name = name
        self.game_id = game_id
        self.timestamp = 0
        self.creator = creator
        self.guest = False
        self.turn = creator
        self.save_timestamp()
        self.board = Board.Board()
        self.rows = self.board.rows
        self.columns = self.board.columns
        self.player_black = PlayerBlack.PlayerBlack()
        self.player_white = PlayerWhite.PlayerWhite()
        self.borders_of_board = {(0, 0, 4), (0, 1, 5), (0, 2, 6), (0, 3, 7), (0, 4, 8), (1, 5, 8), (2, 6, 8), (3, 7, 8),
                                 (4, 8, 8), (5, 8, 7), (6, 8, 6), (7, 8, 5), (8, 8, 4), (8, 7, 3), (8, 6, 2), (8, 5, 1),
                                 (8, 4, 0), (7, 3, 0), (6, 2, 0), (5, 1, 0), (4, 0, 0), (3, 0, 1), (2, 0, 2), (1, 0, 3),
                                 (0, 0, 4)}
        self.borders_of_board_for_x = {(0, 0, 4), (0, 4, 8), (1, 5, 8), (2, 6, 8), (3, 7, 8), (4, 8, 8), (5, 8, 7),
                                       (6, 8, 6), (7, 8, 5), (8, 8, 4), (8, 4, 0), (7, 3, 0), (6, 2, 0), (5, 1, 0),
                                       (4, 0, 0), (3, 0, 1), (2, 0, 2), (1, 0, 3), (0, 0, 4)}
        self.points_for_black = 0
        self.points_for_white = 0
        self.finish = 0

    def save_game(self):
        try:
            pickle.dump(self, open('games/' + self.game_id + '.p', 'wb'))
            return True
        except:
            return False

    def change_turn(self):
        """
        This method changes the turn of the game.
        It returns False if something's wrong. Should not happen.
        :return boolean:
        """
        ok = False

        if self.turn == self.creator:
            self.turn = self.guest
            ok = True
        elif self.turn == self.guest:
            self.turn = self.creator
            ok = True

        if ok:
            self.save_timestamp()

        return ok

    def set_guest(self, guest_id):
        """
        Allows to set guest user ID for use in turns.
        :param int guest_id: Guest user ID
        :return boolean:
        """
        if type(guest_id) is int:
            self.guest = guest_id
            return True
        else:
            return False

    def save_timestamp(self):
        """
        This functions firstly generates a timestamp, and then cuts off the part after the dot.
        This works by converting the stamp to string, and then doing the operation.
        That leaves only 10 first numbers and they are in a string, like this: '1517177788'.
        The string then gets converted back to integer and saved to a Game instance.
        :return:
        """
        timestamp = str(time()).split('.')[0]
        self.timestamp = int(timestamp)
        return

    def get_timestamp(self):
        """
        This simple function returns a timestamp saved in a Game instance.
        :return string: Timestamp as a string.
        """
        return self.timestamp

    def select(self, coordinate_x, coordinate_y, coordinate_z, current_user_id):
        if self.turn == self.creator and self.creator == current_user_id and self.finish == 0:
            if (coordinate_x, coordinate_y, coordinate_z) in self.player_black.positions:
                return True
            return False
        elif self.turn == self.guest and self.guest == current_user_id and self.finish == 0:
            if (coordinate_x, coordinate_y, coordinate_z) in self.player_white.positions:
                return True
            return False
        return False

    def select_multiple(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, current_user_id):
        if self.turn == self.creator and self.creator == current_user_id and self.finish == 0:
            # Checking whether double select is not into the same piece
            if coordinate_x == second_x and coordinate_y == second_y and coordinate_z == second_z:
                return False
            else:
                # Checking whether select piece is a piece
                if (coordinate_x, coordinate_y, coordinate_z) in self.player_black.positions \
                        and (second_x, second_y, second_z) in self.player_black.positions:
                    return True
                return False
        elif self.turn == self.guest and self.guest == current_user_id and self.finish == 0:
            # Checking whether double select is not into the same piece
            if coordinate_x == second_x and coordinate_y == second_y and coordinate_z == second_z:
                return False
            else:
                # Checking whether select piece is a piece
                if (coordinate_x, coordinate_y, coordinate_z) in self.player_white.positions \
                        and (second_x, second_y, second_z) in self.player_white.positions:
                    return True
                return False

    # Function used in views
    def move(self, coordinate_x, coordinate_y, coordinate_z, to_x, to_y, to_z):
        # Checking in which places ball can move (should be in another function)
        # For white
        if self.turn == self.creator:
            if (to_x, to_y, to_z) not in self.player_black.positions and \
                ((fabs(coordinate_x - to_x) == 1 and (fabs(coordinate_y - to_y) == 1 or
                                                      fabs(coordinate_z - to_z) == 1) and
                  (coordinate_y == to_y or coordinate_z == to_z))) \
                or ((fabs(coordinate_y - to_y) == 1 and (fabs(coordinate_x - to_x) == 1 or
                                                         fabs(coordinate_z - to_z) == 1) and
                     (coordinate_x == to_x or coordinate_z == to_z))) \
                or ((fabs(coordinate_z - to_z) == 2 and (fabs(coordinate_y - to_y) == 1
                                                         or fabs(coordinate_x - to_x) == 1) and
                     (coordinate_y == to_y or coordinate_x == to_x))):
                if (coordinate_x, coordinate_y, coordinate_z) in self.player_black.positions:
                    return self.change_position_for_one(coordinate_x, coordinate_y, coordinate_z, to_x, to_y, to_z)

        # Checking in which places ball can move (should be in another function)
        # For black
        elif self.turn == self.guest:
            if (to_x, to_y, to_z) not in self.player_white.positions and \
                ((fabs(coordinate_x - to_x) == 1 and (fabs(coordinate_y - to_y) == 1 or
                                                      fabs(coordinate_z - to_z) == 1) and
                  (coordinate_y == to_y or coordinate_z == to_z))) \
                or ((fabs(coordinate_y - to_y) == 1 and (fabs(coordinate_x - to_x) == 1 or
                                                         fabs(coordinate_z - to_z) == 1) and
                     (coordinate_x == to_x or coordinate_z == to_z))) \
                or ((fabs(coordinate_z - to_z) == 2 and (fabs(coordinate_y - to_y) == 1
                                                         or fabs(coordinate_x - to_x) == 1) and
                     (coordinate_y == to_y or coordinate_x == to_x))):
                if (coordinate_x, coordinate_y, coordinate_z) in self.player_white.positions:
                    return self.change_position_for_one(coordinate_x, coordinate_y, coordinate_z, to_x, to_y, to_z)

    def change_position_for_one(self, coordinate_x, coordinate_y, coordinate_z, to_x, to_y, to_z):
        if (coordinate_x, coordinate_y, coordinate_z) in self.player_white.positions:
            self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
            self.player_white.positions.add((to_x, to_y, to_z))
            return True
        elif (coordinate_x, coordinate_y, coordinate_z) in self.player_black.positions:
            self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
            self.player_black.positions.add((to_x, to_y, to_z))
            return True
        return False

    # Function used in views
    def move_multiple(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x, to_y, to_z):
        # checking whether both or three balls are one's player (should be in other function)
        # For black
        if self.turn == self.creator:
            if (coordinate_x, coordinate_y, coordinate_z) in self.player_black.positions and \
                    (second_x, second_y, second_z) in self.player_black.positions:
                # checking whether move is double
                if (second_x == coordinate_x - 1 and second_z == coordinate_z + 1) \
                        or (second_y == coordinate_y + 1 and second_z == coordinate_z + 1) \
                        or (second_x == coordinate_x + 1 and second_y == coordinate_y + 1) \
                        or (second_x == coordinate_x + 1 and second_z == coordinate_z - 1) \
                        or (second_y == coordinate_y - 1 and second_z == coordinate_z - 1) \
                        or (second_x == coordinate_x - 1 and second_y == coordinate_y - 1):
                    return self.move_double(coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z,
                                            to_x, to_y, to_z)
                # checking whether move is triple
                elif (second_x == coordinate_x - 2 and second_z == coordinate_z + 2) \
                        or (second_y == coordinate_y + 2 and second_z == coordinate_z + 2) \
                        or (second_x == coordinate_x + 2 and second_y == coordinate_y + 2) \
                        or (second_x == coordinate_x + 2 and second_z == coordinate_z - 2) \
                        or (second_y == coordinate_y - 2 and second_z == coordinate_z - 2) \
                        or (second_x == coordinate_x - 2 and second_y == coordinate_y - 2):
                    return self.move_triple(coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z,
                                            to_x, to_y, to_z)
        # For white
        elif self.turn == self.guest:
            if (coordinate_x, coordinate_y, coordinate_z) in self.player_white.positions and \
                    (second_x, second_y, second_z) in self.player_white.positions:
                # checking whether move is double
                if (second_x == coordinate_x - 1 and second_z == coordinate_z + 1) \
                        or (second_y == coordinate_y + 1 and second_z == coordinate_z + 1) \
                        or (second_x == coordinate_x + 1 and second_y == coordinate_y + 1) \
                        or (second_x == coordinate_x + 1 and second_z == coordinate_z - 1) \
                        or (second_y == coordinate_y - 1 and second_z == coordinate_z - 1) \
                        or (second_x == coordinate_x - 1 and second_y == coordinate_y - 1):
                    return self.move_double(coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z,
                                            to_x, to_y, to_z)
                # checking whether move is triple
                elif (second_x == coordinate_x - 2 and second_z == coordinate_z + 2) \
                        or (second_y == coordinate_y + 2 and second_z == coordinate_z + 2) \
                        or (second_x == coordinate_x + 2 and second_y == coordinate_y + 2) \
                        or (second_x == coordinate_x + 2 and second_z == coordinate_z - 2) \
                        or (second_y == coordinate_y - 2 and second_z == coordinate_z - 2) \
                        or (second_x == coordinate_x - 2 and second_y == coordinate_y - 2):
                    return self.move_triple(coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z,
                                            to_x, to_y, to_z)
            return False

    def move_double(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x, to_y, to_z):
        if ((coordinate_x, coordinate_y, coordinate_z) in self.player_white.positions and
                (second_x, second_y, second_z) in self.player_white.positions):
            # for equal x
            if coordinate_x == second_x:
                # checking if move is broadside
                if to_x != coordinate_x and (to_x, to_y, to_z) not in self.player_black.positions and (to_x, to_y, to_z) not in self.player_white.positions:
                    return self.move_double_broadside_for_x(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                            second_y, second_z, to_x, to_y, to_z)
                # checking if move is inline
                elif to_x == coordinate_x and (to_x, to_y, to_z) not in self.player_white.positions:
                    return self.move_multiple_inline_for_x(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                           second_y, second_z, to_x, to_y, to_z)
            # for equal y
            elif coordinate_y == second_y:
                # checking if move is broadside
                if to_y != coordinate_y and (to_x, to_y, to_z) not in self.player_black.positions and (to_x, to_y, to_z) not in self.player_white.positions:
                    return self.move_double_broadside_for_y(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                            second_y, second_z, to_x, to_y, to_z)
                # checking if move is inline
                elif to_y == coordinate_y and (to_x, to_y, to_z) not in self.player_white.positions:
                    return self.move_multiple_inline_for_y(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                           second_y, second_z, to_x, to_y, to_z)
            # for equal z
            elif coordinate_z == second_z:
                # checking if move is broadside
                if to_z != coordinate_z and (to_x, to_y, to_z) not in self.player_black.positions and (to_x, to_y, to_z) not in self.player_white.positions:
                    return self.move_double_broadside_for_z(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                            second_y, second_z, to_x, to_y, to_z)
                # checking if move is inline
                elif to_z == coordinate_z and (to_x, to_y, to_z) not in self.player_white.positions:
                    return self.move_multiple_inline_for_z(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                           second_y, second_z, to_x, to_y, to_z)
        elif ((coordinate_x, coordinate_y, coordinate_z) in self.player_black.positions and
                (second_x, second_y, second_z) in self.player_black.positions):
            # for equal x
            if coordinate_x == second_x:
                # checking if move is broadside
                if to_x != coordinate_x and (to_x, to_y, to_z) not in self.player_black.positions and (to_x, to_y, to_z) not in self.player_white.positions:
                    return self.move_double_broadside_for_x(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                            second_y, second_z, to_x, to_y, to_z)
                # checking if move is inline
                elif to_x == coordinate_x and (to_x, to_y, to_z) not in self.player_black.positions:
                    return self.move_multiple_inline_for_x(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                           second_y, second_z, to_x, to_y, to_z)
            # for equal y
            elif coordinate_y == second_y:
                # checking if move is broadside
                if to_y != coordinate_y and (to_x, to_y, to_z) not in self.player_black.positions and (to_x, to_y, to_z) not in self.player_white.positions:
                    return self.move_double_broadside_for_y(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                            second_y, second_z, to_x, to_y, to_z)
                # checking if move is inline
                elif to_y == coordinate_y and (to_x, to_y, to_z) not in self.player_black.positions:
                    return self.move_multiple_inline_for_y(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                           second_y, second_z, to_x, to_y, to_z)
            # for equal z
            elif coordinate_z == second_z:
                # checking if move is broadside
                if to_z != coordinate_z and (to_x, to_y, to_z) not in self.player_black.positions and (to_x, to_y, to_z) not in self.player_white.positions:
                    return self.move_double_broadside_for_z(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                            second_y, second_z, to_x, to_y, to_z)
                # checking if move is inline
                elif to_z == coordinate_z and (to_x, to_y, to_z) not in self.player_black.positions:
                    return self.move_multiple_inline_for_z(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                           second_y, second_z, to_x, to_y, to_z)
        return False

    def move_double_broadside_for_x(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                    to_y, to_z):
        if (to_x == coordinate_x + 1 and to_y == coordinate_y and to_z == coordinate_z - 1
            and (second_x + 1, second_y, second_z - 1) not in self.player_black.positions
            and (second_x + 1, second_y, second_z - 1) not in self.player_white.positions) or \
                (to_x == second_x + 1 and to_y == second_y and to_z == second_z - 1
                 and (coordinate_x + 1, coordinate_y, coordinate_z - 1) not in self.player_black.positions
                 and (coordinate_x + 1, coordinate_y, coordinate_z - 1) not in self.player_white.positions):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x + 1, coordinate_y, coordinate_z - 1,
                                                   second_x + 1, second_y, second_z - 1)
            return True

        elif (to_x == coordinate_x + 1 and to_y == coordinate_y + 1 and to_z == coordinate_z
              and (second_x + 1, second_y + 1, second_z) not in self.player_black.positions
              and (second_x + 1, second_y + 1, second_z) not in self.player_white.positions) or \
                (to_x == second_x + 1 and to_y == second_y + 1 and to_z == second_z
                 and (coordinate_x + 1, coordinate_y + 1, coordinate_z) not in self.player_black.positions
                 and (coordinate_x + 1, coordinate_y + 1, coordinate_z) not in self.player_white.positions):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x + 1, coordinate_y + 1, coordinate_z,
                                                   second_x + 1, second_y + 1, second_z)
            return True

        elif (to_x == coordinate_x - 1 and to_y == coordinate_y and to_z == coordinate_z + 1
              and (second_x - 1, second_y, second_z + 1) not in self.player_black.positions
              and (second_x - 1, second_y, second_z + 1) not in self.player_white.positions) or \
                (to_x == second_x - 1 and to_y == second_y and to_z == second_z + 1
                 and (coordinate_x - 1, coordinate_y, coordinate_z + 1) not in self.player_black.positions
                 and (coordinate_x - 1, coordinate_y, coordinate_z + 1) not in self.player_white.positions):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x - 1, coordinate_y, coordinate_z + 1,
                                                   second_x - 1, second_y, second_z + 1)
            return True

        elif (to_x == coordinate_x - 1 and to_y == coordinate_y - 1 and to_z == coordinate_z
              and (second_x - 1, second_y - 1, second_z) not in self.player_black.positions
              and (second_x - 1, second_y - 1, second_z) not in self.player_white.positions) or \
                (to_x == second_x - 1 and to_y == second_y - 1 and to_z == second_z
                 and (coordinate_x - 1, coordinate_y - 1, coordinate_z) not in self.player_black.positions
                 and (coordinate_x - 1, coordinate_y - 1, coordinate_z) not in self.player_white.positions):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x - 1, coordinate_y - 1, coordinate_z,
                                                   second_x - 1, second_y - 1, second_z)
            return True
        return False

    def move_multiple_inline_for_x(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                   to_y, to_z):
        if (coordinate_x, coordinate_y, coordinate_z) in self.player_black.positions and \
                    (second_x, second_y, second_z) in self.player_black.positions:
            if (to_y == coordinate_y + 1 and to_z == coordinate_z + 1) \
                    or (to_y == second_y + 1 and to_z == second_z + 1) \
                    or (to_y == coordinate_y - 1 and to_z == coordinate_z - 1) \
                    or (to_y == second_y - 1 and to_z == second_z - 1):
                if fabs(to_y - coordinate_y) < fabs(to_y - second_y) and \
                        fabs(to_z - coordinate_z) < fabs(to_z - second_z):
                    if (to_x, to_y, to_z) not in self.player_white.positions:
                        self.player_black.positions.remove((second_x, second_y, second_z))
                        self.player_black.positions.add((to_x, to_y, to_z))
                        return True
                    # sumito
                    elif (to_x, to_y, to_z) in self.player_white.positions:
                        self.black_sumito_for_coord_x(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                      second_z, to_x, to_y, to_z)
                        return True
                elif fabs(to_y - second_y) < fabs(to_y - coordinate_y) and \
                        fabs(to_z - second_z) < fabs(to_z - coordinate_z):
                    if (to_x, to_y, to_z) not in self.player_white.positions:
                        self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                        self.player_black.positions.add((to_x, to_y, to_z))
                        return True
                    # sumito
                    elif (to_x, to_y, to_z) in self.player_white.positions:
                        self.black_sumito_for_sec_x(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                    second_z, to_x, to_y, to_z)
                        return True

        elif (coordinate_x, coordinate_y, coordinate_z) in self.player_white.positions and \
                    (second_x, second_y, second_z) in self.player_white.positions:
            if (to_y == coordinate_y + 1 and to_z == coordinate_z + 1) \
                    or (to_y == second_y + 1 and to_z == second_z + 1) \
                    or (to_y == coordinate_y - 1 and to_z == coordinate_z - 1) \
                    or (to_y == second_y - 1 and to_z == second_z - 1):
                if fabs(to_y - coordinate_y) < fabs(to_y - second_y) and \
                        fabs(to_z - coordinate_z) < fabs(to_z - second_z):
                    if (to_x, to_y, to_z) not in self.player_black.positions:
                        self.player_white.positions.remove((second_x, second_y, second_z))
                        self.player_white.positions.add((to_x, to_y, to_z))
                        return True
                    # sumito
                    elif (to_x, to_y, to_z) in self.player_black.positions:
                        self.white_sumito_for_coord_x(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                      second_z, to_x, to_y, to_z)
                        return True
                elif fabs(to_y - second_y) < fabs(to_y - coordinate_y) and \
                        fabs(to_z - second_z) < fabs(to_z - coordinate_z):
                    if (to_x, to_y, to_z) not in self.player_black.positions:
                        self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                        self.player_white.positions.add((to_x, to_y, to_z))
                        return True
                    # sumito
                    elif (to_x, to_y, to_z) in self.player_black.positions:
                        self.white_sumito_for_sec_x(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                    second_z, to_x, to_y, to_z)
                        return True
        return False

    def move_double_broadside_for_y(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                    to_y, to_z):
        if (to_x == coordinate_x - 1 and to_y == coordinate_y - 1 and to_z == coordinate_z
            and (second_x - 1, second_y - 1, second_z) not in self.player_black.positions
            and (second_x - 1, second_y - 1, second_z) not in self.player_white.positions) or \
                (to_x == second_x - 1 and to_y == second_y - 1 and to_z == second_z
                 and (coordinate_x - 1, coordinate_y - 1, coordinate_z) not in self.player_black.positions
                 and (coordinate_x - 1, coordinate_y - 1, coordinate_z) not in self.player_white.positions):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x - 1, coordinate_y - 1, coordinate_z,
                                                   second_x - 1, second_y - 1, second_z)
            return True

        elif (to_x == coordinate_x and to_y == coordinate_y - 1 and to_z == coordinate_z - 1
              and (second_x, second_y - 1, second_z - 1) not in self.player_black.positions
              and (second_x, second_y - 1, second_z - 1) not in self.player_white.positions) or \
                (to_x == second_x and to_y == second_y - 1 and to_z == second_z - 1
                 and (coordinate_x, coordinate_y - 1, coordinate_z - 1) not in self.player_black.positions
                 and (coordinate_x, coordinate_y - 1, coordinate_z - 1) not in self.player_white.positions):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x, coordinate_y - 1, coordinate_z - 1,
                                                   second_x, second_y - 1, second_z - 1)
            return True

        elif (to_x == coordinate_x + 1 and to_y == coordinate_y + 1 and to_z == coordinate_z
              and (second_x + 1, second_y + 1, second_z) not in self.player_black.positions
              and (second_x + 1, second_y + 1, second_z) not in self.player_white.positions) or \
                (to_x == second_x + 1 and to_y == second_y + 1 and to_z == second_z
                 and (coordinate_x + 1, coordinate_y + 1, coordinate_z) not in self.player_black.positions
                 and (coordinate_x + 1, coordinate_y + 1, coordinate_z) not in self.player_white.positions):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x + 1, coordinate_y + 1, coordinate_z,
                                                   second_x + 1, second_y + 1, second_z)
            return True

        elif (to_x == coordinate_x and to_y == coordinate_y + 1 and to_z == coordinate_z + 1
              and (second_x, second_y + 1, second_z + 1) not in self.player_black.positions
              and (second_x, second_y + 1, second_z + 1) not in self.player_white.positions) or \
                (to_x == second_x and to_y == second_y + 1 and to_z == second_z + 1
                 and (coordinate_x, coordinate_y + 1, coordinate_z + 1) not in self.player_black.positions
                 and (coordinate_x, coordinate_y + 1, coordinate_z + 1) not in self.player_white.positions):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x, coordinate_y + 1, coordinate_z + 1,
                                                   second_x, second_y + 1, second_z + 1)
            return True
        return False

    def move_multiple_inline_for_y(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z,
                                   to_x, to_y, to_z):
        if (coordinate_x, coordinate_y, coordinate_z) in self.player_black.positions and \
             (second_x, second_y, second_z) in self.player_black.positions:
            if (to_x == coordinate_x + 1 and to_z == coordinate_z - 1) \
                    or (to_x == second_x + 1 and to_z == second_z - 1) \
                    or (to_x == coordinate_x - 1 and to_z == coordinate_z + 1) \
                    or (to_x == second_x - 1 and to_z == second_z + 1):
                if fabs(to_x - coordinate_x) < fabs(to_x - second_x) and \
                        fabs(to_z - coordinate_z) < fabs(to_z - second_z):
                    if (to_x, to_y, to_z) not in self.player_white.positions:
                        self.player_black.positions.remove((second_x, second_y, second_z))
                        self.player_black.positions.add((to_x, to_y, to_z))
                        return True
                    # sumito
                    elif (to_x, to_y, to_z) in self.player_white.positions:
                        self.black_sumito_for_coord_y(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                      second_z, to_x, to_y, to_z)
                    return True
                elif fabs(to_x - second_x) < fabs(to_x - coordinate_x) and \
                        fabs(to_z - second_z) < fabs(to_z - coordinate_z):
                    if (to_x, to_y, to_z) not in self.player_white.positions:
                        self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                        self.player_black.positions.add((to_x, to_y, to_z))
                        return True
                    # sumito
                    elif (to_x, to_y, to_z) in self.player_white.positions:
                        self.black_sumito_for_sec_y(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                    second_z, to_x, to_y, to_z)
                        return True
        elif (coordinate_x, coordinate_y, coordinate_z) in self.player_white.positions and \
             (second_x, second_y, second_z) in self.player_white.positions:
            if (to_x == coordinate_x + 1 and to_z == coordinate_z - 1) \
                    or (to_x == second_x + 1 and to_z == second_z - 1) \
                    or (to_x == coordinate_x - 1 and to_z == coordinate_z + 1) \
                    or (to_x == second_x - 1 and to_z == second_z + 1):
                if fabs(to_x - coordinate_x) < fabs(to_x - second_x) and \
                        fabs(to_z - coordinate_z) < fabs(to_z - second_z):
                    if (to_x, to_y, to_z) not in self.player_black.positions:
                        self.player_white.positions.remove((second_x, second_y, second_z))
                        self.player_white.positions.add((to_x, to_y, to_z))
                        return True
                    # sumito
                    elif (to_x, to_y, to_z) in self.player_black.positions:
                        self.white_sumito_for_coord_y(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                      second_z, to_x, to_y, to_z)
                        return True
                elif fabs(to_x - second_x) < fabs(to_x - coordinate_x) and \
                        fabs(to_z - second_z) < fabs(to_z - coordinate_z):
                    if (to_x, to_y, to_z) not in self.player_black.positions:
                        self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                        self.player_white.positions.add((to_x, to_y, to_z))
                        return True
                    # sumito
                    elif (to_x, to_y, to_z) in self.player_black.positions:
                        self.white_sumito_for_sec_y(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                    second_z, to_x, to_y, to_z)
                        return True
        return False

    def move_double_broadside_for_z(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                    to_y, to_z):
        if (to_x == coordinate_x - 1 and to_y == coordinate_y and to_z == coordinate_z + 1
            and (second_x - 1, second_y, second_z + 1) not in self.player_black.positions
            and (second_x - 1, second_y, second_z + 1) not in self.player_white.positions) or \
                (to_x == second_x - 1 and to_y == second_y and to_z == second_z + 1
                 and (coordinate_x - 1, coordinate_y, coordinate_z + 1) not in self.player_black.positions
                 and (coordinate_x - 1, coordinate_y, coordinate_z + 1) not in self.player_white.positions):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x - 1, coordinate_y, coordinate_z + 1,
                                                   second_x - 1, second_y, second_z + 1)
            return True

        elif (to_x == coordinate_x + 1 and to_y == coordinate_y and to_z == coordinate_z - 1
              and (second_x + 1, second_y, second_z - 1) not in self.player_black.positions
              and (second_x + 1, second_y, second_z - 1) not in self.player_white.positions) or \
                (to_x == second_x + 1 and to_y == second_y and to_z == second_z - 1
                 and (coordinate_x + 1, coordinate_y, coordinate_z - 1) not in self.player_black.positions
                 and (coordinate_x + 1, coordinate_y, coordinate_z - 1) not in self.player_white.positions):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x + 1, coordinate_y, coordinate_z - 1,
                                                   second_x + 1, second_y, second_z - 1)
            return True

        elif (to_x == coordinate_x and to_y == coordinate_y + 1 and to_z == coordinate_z + 1
              and (second_x, second_y + 1, second_z + 1) not in self.player_black.positions
              and (second_x, second_y + 1, second_z + 1) not in self.player_white.positions) or \
                (to_x == second_x and to_y == second_y + 1 and to_z == second_z + 1
                 and (coordinate_x, coordinate_y + 1, coordinate_z + 1) not in self.player_black.positions
                 and (coordinate_x, coordinate_y + 1, coordinate_z + 1) not in self.player_white.positions):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x, coordinate_y + 1, coordinate_z + 1,
                                                   second_x, second_y + 1, second_z + 1)
            return True

        elif (to_x == coordinate_x and to_y == coordinate_y - 1 and to_z == coordinate_z - 1
              and (second_x, second_y - 1, second_z - 1) not in self.player_black.positions
              and (second_x, second_y - 1, second_z - 1) not in self.player_white.positions) or \
                (to_x == second_x and to_y == second_y - 1 and to_z == second_z - 1
                 and (coordinate_x, coordinate_y - 1, coordinate_z - 1) not in self.player_black.positions
                 and (coordinate_x, coordinate_y - 1, coordinate_z - 1) not in self.player_white.positions):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x, coordinate_y - 1, coordinate_z - 1,
                                                   second_x, second_y - 1, second_z - 1)
            return True
        return False

    def move_multiple_inline_for_z(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                   to_y, to_z):
        if (coordinate_x, coordinate_y, coordinate_z) in self.player_black.positions and \
             (second_x, second_y, second_z) in self.player_black.positions:
            if (to_x == coordinate_x + 1 and to_y == coordinate_y + 1) \
                    or (to_x == second_x + 1 and to_y == second_y + 1) \
                    or (to_x == coordinate_x - 1 and to_y == coordinate_y - 1) \
                    or (to_x == second_x - 1 and to_y == second_y - 1):
                if fabs(to_x - coordinate_x) < fabs(to_x - second_x) and \
                        fabs(to_y - coordinate_y) < fabs(to_y - second_y):
                    if (to_x, to_y, to_z) not in self.player_white.positions:
                        self.player_black.positions.remove((second_x, second_y, second_z))
                        self.player_black.positions.add((to_x, to_y, to_z))
                        return True
                    # sumito
                    elif (to_x, to_y, to_z) in self.player_white.positions:
                        self.black_sumito_for_coord_z(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                      second_z, to_x, to_y, to_z)
                elif fabs(to_x - second_x) < fabs(to_x - coordinate_x) and \
                        fabs(to_y - second_y) < fabs(to_y - coordinate_y):
                    if (to_x, to_y, to_z) not in self.player_white.positions:
                        self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                        self.player_black.positions.add((to_x, to_y, to_z))
                        return True
                    # sumito
                    elif (to_x, to_y, to_z) in self.player_white.positions:
                        self.black_sumito_for_sec_z(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                    second_z, to_x, to_y, to_z)
                        return True
        elif (coordinate_x, coordinate_y, coordinate_z) in self.player_white.positions and \
             (second_x, second_y, second_z) in self.player_white.positions:
            if (to_x == coordinate_x + 1 and to_y == coordinate_y + 1) \
                    or (to_x == second_x + 1 and to_y == second_y + 1) \
                    or (to_x == coordinate_x - 1 and to_y == coordinate_y - 1) \
                    or (to_x == second_x - 1 and to_y == second_y - 1):
                if fabs(to_x - coordinate_x) < fabs(to_x - second_x) and \
                        fabs(to_y - coordinate_y) < fabs(to_y - second_y):
                    if (to_x, to_y, to_z) not in self.player_black.positions:
                        self.player_white.positions.remove((second_x, second_y, second_z))
                        self.player_white.positions.add((to_x, to_y, to_z))
                        return True
                    # sumito
                    elif (to_x, to_y, to_z) in self.player_black.positions:
                        self.white_sumito_for_coord_z(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                      second_z, to_x, to_y, to_z)
                        return True
                elif fabs(to_x - second_x) < fabs(to_x - coordinate_x) and \
                        fabs(to_y - second_y) < fabs(to_y - coordinate_y):
                    if (to_x, to_y, to_z) not in self.player_black.positions:
                        self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                        self.player_white.positions.add((to_x, to_y, to_z))
                        return True
                    # sumito
                    elif (to_x, to_y, to_z) in self.player_black.positions:
                        self.white_sumito_for_sec_z(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                    second_z, to_x, to_y, to_z)
                        return True
        return False

    def change_double_broadside_positions(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                          second_z, new_coordinate_x, new_coordinate_y, new_coordinate_z,
                                          new_second_x, new_second_y, new_second_z):
        if (coordinate_x, coordinate_y, coordinate_z) in self.player_black.positions and \
             (second_x, second_y, second_z) in self.player_black.positions:
            # checking if new positions are not in other pieces
            if (new_coordinate_x, new_coordinate_y, new_coordinate_z) not in self.player_black.positions \
                    and (new_second_x, new_second_y, new_second_z) not in self.player_black.positions:
                self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                self.player_black.positions.remove((second_x, second_y, second_z))
                self.player_black.positions.add((new_coordinate_x, new_coordinate_y, new_coordinate_z))
                self.player_black.positions.add((new_second_x, new_second_y, new_second_z))
                return True
        elif (coordinate_x, coordinate_y, coordinate_z) in self.player_white.positions and \
             (second_x, second_y, second_z) in self.player_white.positions:
            # checking if new positions are not in other pieces
            if (new_coordinate_x, new_coordinate_y, new_coordinate_z) not in self.player_white.positions \
                    and (new_second_x, new_second_y, new_second_z) not in self.player_white.positions:
                self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                self.player_white.positions.remove((second_x, second_y, second_z))
                self.player_white.positions.add((new_coordinate_x, new_coordinate_y, new_coordinate_z))
                self.player_white.positions.add((new_second_x, new_second_y, new_second_z))
                return True
        return False

    def move_triple(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x, to_y, to_z):
        if (coordinate_x, coordinate_y, coordinate_z) in self.player_black.positions and \
             (second_x, second_y, second_z) in self.player_black.positions:
            # for equal x
            if coordinate_x == second_x:
                # checking whether between balls is the third ball(probably another function)
                if (coordinate_x, (coordinate_y + second_y) / 2, (coordinate_z + second_z) / 2) in self.player_black.positions:
                    middle_x = coordinate_x
                    middle_y = (coordinate_y + second_y) / 2
                    middle_z = (coordinate_z + second_z) / 2
                    # checking if move is broadside
                    if to_x != coordinate_x and (to_x, to_y, to_z) not in self.player_black.positions and (to_x, to_y, to_z) not in self.player_white.positions:
                        return self.move_triple_broadside_for_x(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                                second_y, second_z, middle_x, middle_y, middle_z,
                                                                to_x, to_y, to_z)
                    # checking if move is inline
                    elif to_x == coordinate_x and (to_x, to_y, to_z) not in self.player_black.positions:
                        return self.move_multiple_inline_for_x(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                               second_y, second_z, to_x, to_y, to_z)
            # for equal y
            elif coordinate_y == second_y:
                # checking whether between balls is the third ball(probably another function)
                if ((coordinate_x + second_x) / 2, coordinate_y, (coordinate_z + second_z) / 2) in self.player_black.positions:
                    middle_x = (coordinate_x + second_x) / 2
                    middle_y = coordinate_y
                    middle_z = (coordinate_z + second_z) / 2
                    # checking if move is broadside
                    if to_y != coordinate_y and (to_x, to_y, to_z) not in self.player_black.positions and (to_x, to_y, to_z) not in self.player_white.positions:
                        return self.move_triple_broadside_for_y(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                                second_y, second_z, middle_x, middle_y, middle_z,
                                                                to_x, to_y, to_z)
                    # checking if move is inline
                    elif to_y == coordinate_y and (to_x, to_y, to_z) not in self.player_black.positions:
                        return self.move_multiple_inline_for_y(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                               second_y, second_z, to_x, to_y, to_z)
            # for equal z
            elif coordinate_z == second_z:
                # checking whether between balls is the third ball(probably another function)
                if ((coordinate_x + second_x) / 2, (coordinate_y + second_y) / 2, coordinate_z) in self.player_black.positions:
                    middle_x = (coordinate_x + second_x) / 2
                    middle_y = (coordinate_y + second_y) / 2
                    middle_z = coordinate_z
                    # checking if move is broadside
                    if to_z != coordinate_z and (to_x, to_y, to_z) not in self.player_black.positions and (to_x, to_y, to_z) not in self.player_white.positions:
                        return self.move_triple_broadside_for_z(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                                second_y, second_z, middle_x, middle_y, middle_z,
                                                                to_x, to_y, to_z)
                    # checking if move is inline
                    elif to_z == coordinate_z and (to_x, to_y, to_z) not in self.player_black.positions:
                        return self.move_multiple_inline_for_z(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                               second_y, second_z, to_x, to_y, to_z)
        elif (coordinate_x, coordinate_y, coordinate_z) in self.player_white.positions and \
             (second_x, second_y, second_z) in self.player_white.positions:
            # for equal x
            if coordinate_x == second_x:
                # checking whether between balls is the third ball(probably another function)
                if (coordinate_x, (coordinate_y + second_y) / 2, (coordinate_z + second_z) / 2) in self.player_white.positions:
                    middle_x = coordinate_x
                    middle_y = (coordinate_y + second_y) / 2
                    middle_z = (coordinate_z + second_z) / 2
                    # checking if move is broadside
                    if to_x != coordinate_x and (to_x, to_y, to_z) not in self.player_black.positions and (to_x, to_y, to_z) not in self.player_white.positions:
                        return self.move_triple_broadside_for_x(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                                second_y, second_z, middle_x, middle_y, middle_z,
                                                                to_x, to_y, to_z)
                    # checking if move is inline
                    elif to_x == coordinate_x and (to_x, to_y, to_z) not in self.player_white.positions:
                        return self.move_multiple_inline_for_x(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                               second_y, second_z, to_x, to_y, to_z)
            # for equal y
            elif coordinate_y == second_y:
                # checking whether between balls is the third ball(probably another function)
                if ((coordinate_x + second_x) / 2, coordinate_y, (coordinate_z + second_z) / 2) in self.player_white.positions:
                    middle_x = (coordinate_x + second_x) / 2
                    middle_y = coordinate_y
                    middle_z = (coordinate_z + second_z) / 2
                    # checking if move is broadside
                    if to_y != coordinate_y and (to_x, to_y, to_z) not in self.player_black.positions and (to_x, to_y, to_z) not in self.player_white.positions:
                        return self.move_triple_broadside_for_y(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                                second_y, second_z, middle_x, middle_y, middle_z,
                                                                to_x, to_y, to_z)
                    # checking if move is inline
                    elif to_y == coordinate_y and (to_x, to_y, to_z) not in self.player_white.positions:
                        return self.move_multiple_inline_for_y(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                               second_y, second_z, to_x, to_y, to_z)
            # for equal z
            elif coordinate_z == second_z:
                # checking whether between balls is the third ball(probably another function)
                if ((coordinate_x + second_x) / 2, (coordinate_y + second_y) / 2, coordinate_z) in self.player_white.positions:
                    middle_x = (coordinate_x + second_x) / 2
                    middle_y = (coordinate_y + second_y) / 2
                    middle_z = coordinate_z
                    # checking if move is broadside
                    if to_z != coordinate_z and (to_x, to_y, to_z) not in self.player_black.positions and (to_x, to_y, to_z) not in self.player_white.positions:
                        return self.move_triple_broadside_for_z(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                                second_y, second_z, middle_x, middle_y, middle_z,
                                                                to_x, to_y, to_z)
                    # checking if move is inline
                    elif to_z == coordinate_z and (to_x, to_y, to_z) not in self.player_white.positions:
                        return self.move_multiple_inline_for_z(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                               second_y, second_z, to_x, to_y, to_z)
        return False

    def move_triple_broadside_for_x(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z,
                                    middle_x, middle_y, middle_z, to_x, to_y, to_z):
        if (to_x == coordinate_x + 1 and to_y == coordinate_y and to_z == coordinate_z - 1
            and (second_x + 1, second_y, second_z - 1) not in self.player_black.positions
            and (second_x + 1, second_y, second_z - 1) not in self.player_white.positions
            and (middle_x + 1, middle_y, middle_z - 1) not in self.player_black.positions
            and (middle_x + 1, middle_y, middle_z - 1) not in self.player_white.positions) or \
                (to_x == second_x + 1 and to_y == second_y and to_z == second_z - 1
                 and (coordinate_x + 1, coordinate_y, coordinate_z - 1) not in self.player_black.positions
                 and (coordinate_x + 1, coordinate_y, coordinate_z - 1) not in self.player_white.positions
                 and (middle_x + 1, middle_y, middle_z - 1) not in self.player_black.positions
                 and (middle_x + 1, middle_y, middle_z - 1) not in self.player_white.positions):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x + 1,
                                                   coordinate_y, coordinate_z - 1, second_x + 1, second_y, second_z - 1,
                                                   middle_x + 1, middle_y, middle_z - 1)
            return True

        elif (to_x == coordinate_x + 1 and to_y == coordinate_y + 1 and to_z == coordinate_z
              and (second_x + 1, second_y + 1, second_z) not in self.player_black.positions
              and (second_x + 1, second_y + 1, second_z) not in self.player_white.positions
              and (middle_x + 1, middle_y + 1, middle_z) not in self.player_black.positions
              and (middle_x + 1, middle_y + 1, middle_z) not in self.player_white.positions) or \
                (to_x == second_x + 1 and to_y == second_y + 1 and to_z == second_z
                 and (coordinate_x + 1, coordinate_y + 1, coordinate_z) not in self.player_black.positions
                 and (coordinate_x + 1, coordinate_y + 1, coordinate_z) not in self.player_white.positions
                 and (middle_x + 1, middle_y + 1, middle_z) not in self.player_black.positions
                 and (middle_x + 1, middle_y + 1, middle_z) not in self.player_white.positions):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x + 1,
                                                   coordinate_y + 1, coordinate_z, second_x + 1, second_y + 1, second_z,
                                                   middle_x + 1, middle_y + 1, middle_z)
            return True

        elif (to_x == coordinate_x - 1 and to_y == coordinate_y and to_z == coordinate_z + 1
              and (second_x - 1, second_y, second_z + 1) not in self.player_black.positions
              and (second_x - 1, second_y, second_z + 1) not in self.player_white.positions
              and (middle_x - 1, middle_y, middle_z + 1) not in self.player_black.positions
              and (middle_x - 1, middle_y, middle_z + 1) not in self.player_white.positions) or \
                (to_x == second_x - 1 and to_y == second_y and to_z == second_z + 1
                 and (coordinate_x - 1, coordinate_y, coordinate_z + 1) not in self.player_black.positions
                 and (coordinate_x - 1, coordinate_y, coordinate_z + 1) not in self.player_white.positions
                 and (middle_x - 1, middle_y, middle_z + 1) not in self.player_black.positions
                 and (middle_x - 1, middle_y, middle_z + 1) not in self.player_white.positions):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x - 1,
                                                   coordinate_y, coordinate_z + 1, second_x - 1, second_y, second_z + 1,
                                                   middle_x - 1, middle_y, middle_z + 1)
            return True

        elif (to_x == coordinate_x - 1 and to_y == coordinate_y - 1 and to_z == coordinate_z
              and (second_x - 1, second_y - 1, second_z) not in self.player_black.positions
              and (second_x - 1, second_y - 1, second_z) not in self.player_white.positions
              and (middle_x - 1, middle_y - 1, middle_z) not in self.player_black.positions
              and (middle_x - 1, middle_y - 1, middle_z) not in self.player_white.positions) or \
                (to_x == second_x - 1 and to_y == second_y - 1 and to_z == second_z
                 and (coordinate_x - 1, coordinate_y - 1, coordinate_z) not in self.player_black.positions
                 and (coordinate_x - 1, coordinate_y - 1, coordinate_z) not in self.player_white.positions
                 and (middle_x - 1, middle_y - 1, middle_z) not in self.player_black.positions
                 and (middle_x - 1, middle_y - 1, middle_z) not in self.player_white.positions):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x - 1,
                                                   coordinate_y - 1, coordinate_z, second_x - 1, second_y - 1, second_z,
                                                   middle_x - 1, middle_y - 1, middle_z)
            return True
        return False

    def move_triple_broadside_for_y(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z,
                                    middle_x, middle_y, middle_z, to_x, to_y, to_z):
        if (to_x == coordinate_x - 1 and to_y == coordinate_y - 1 and to_z == coordinate_z
            and (second_x - 1, second_y - 1, second_z) not in self.player_black.positions
            and (second_x - 1, second_y - 1, second_z) not in self.player_white.positions
            and (middle_x - 1, middle_y - 1, middle_z) not in self.player_black.positions
            and (middle_x - 1, middle_y - 1, middle_z) not in self.player_white.positions) or \
                (to_x == second_x - 1 and to_y == second_y - 1 and to_z == second_z
                 and (coordinate_x - 1, coordinate_y - 1, coordinate_z) not in self.player_black.positions
                 and (coordinate_x - 1, coordinate_y - 1, coordinate_z) not in self.player_white.positions
                 and (middle_x - 1, middle_y - 1, middle_z) not in self.player_black.positions
                 and (middle_x - 1, middle_y - 1, middle_z) not in self.player_white.positions):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x - 1,
                                                   coordinate_y - 1, coordinate_z, second_x - 1, second_y - 1, second_z,
                                                   middle_x - 1, middle_y - 1, middle_z)
            return True

        elif (to_x == coordinate_x and to_y == coordinate_y - 1 and to_z == coordinate_z - 1
              and (second_x, second_y - 1, second_z - 1) not in self.player_black.positions
              and (second_x, second_y - 1, second_z - 1) not in self.player_white.positions
              and (middle_x, middle_y - 1, middle_z - 1) not in self.player_black.positions
              and (middle_x, middle_y - 1, middle_z - 1) not in self.player_white.positions) or \
                (to_x == second_x and to_y == second_y - 1 and to_z == second_z - 1
                 and (coordinate_x, coordinate_y - 1, coordinate_z - 1) not in self.player_black.positions
                 and (coordinate_x, coordinate_y - 1, coordinate_z - 1) not in self.player_white.positions
                 and (middle_x, middle_y - 1, middle_z - 1) not in self.player_black.positions
                 and (middle_x, middle_y - 1, middle_z - 1) not in self.player_white.positions):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x, coordinate_y - 1,
                                                   coordinate_z - 1, second_x, second_y - 1, second_z - 1,
                                                   middle_x, middle_y - 1, middle_z - 1)
            return True

        elif (to_x == coordinate_x + 1 and to_y == coordinate_y + 1 and to_z == coordinate_z
              and (second_x + 1, second_y + 1, second_z) not in self.player_black.positions
              and (second_x + 1, second_y + 1, second_z) not in self.player_white.positions
              and (middle_x + 1, middle_y + 1, middle_z) not in self.player_black.positions
              and (middle_x + 1, middle_y + 1, middle_z) not in self.player_white.positions) or \
                (to_x == second_x + 1 and to_y == second_y + 1 and to_z == second_z
                 and (coordinate_x + 1, coordinate_y + 1, coordinate_z) not in self.player_black.positions
                 and (coordinate_x + 1, coordinate_y + 1, coordinate_z) not in self.player_white.positions
                 and (middle_x + 1, middle_y + 1, middle_z) not in self.player_black.positions
                 and (middle_x + 1, middle_y + 1, middle_z) not in self.player_white.positions):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x + 1,
                                                   coordinate_y + 1, coordinate_z, second_x + 1, second_y + 1,
                                                   second_z, middle_x + 1, middle_y + 1, middle_z)
            return True

        elif (to_x == coordinate_x and to_y == coordinate_y + 1 and to_z == coordinate_z + 1
              and (second_x, second_y + 1, second_z + 1) not in self.player_black.positions
              and (second_x, second_y + 1, second_z + 1) not in self.player_white.positions
              and (middle_x, middle_y + 1, middle_z + 1) not in self.player_black.positions
              and (middle_x, middle_y + 1, middle_z + 1) not in self.player_white.positions) or \
                (to_x == second_x and to_y == second_y + 1 and to_z == second_z + 1
                 and (coordinate_x, coordinate_y + 1, coordinate_z + 1) not in self.player_black.positions
                 and (coordinate_x, coordinate_y + 1, coordinate_z + 1) not in self.player_white.positions
                 and (middle_x, middle_y + 1, middle_z + 1) not in self.player_black.positions
                 and (middle_x, middle_y + 1, middle_z + 1) not in self.player_white.positions):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x,
                                                   coordinate_y + 1, coordinate_z + 1, second_x, second_y + 1,
                                                   second_z + 1, middle_x, middle_y + 1, middle_z + 1)
            return True
        return False

    def move_triple_broadside_for_z(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z,
                                    middle_x, middle_y, middle_z, to_x, to_y, to_z):
        if (to_x == coordinate_x - 1 and to_y == coordinate_y and to_z == coordinate_z + 1
            and (second_x - 1, second_y, second_z + 1) not in self.player_black.positions
            and (second_x - 1, second_y, second_z + 1) not in self.player_white.positions
            and (middle_x - 1, middle_y, middle_z + 1) not in self.player_black.positions
            and (middle_x - 1, middle_y, middle_z + 1) not in self.player_white.positions) or \
                (to_x == second_x - 1 and to_y == second_y and to_z == second_z + 1
                 and (coordinate_x - 1, coordinate_y, coordinate_z + 1) not in self.player_black.positions
                 and (coordinate_x - 1, coordinate_y, coordinate_z + 1) not in self.player_white.positions
                 and (middle_x - 1, middle_y, middle_z + 1) not in self.player_black.positions
                 and (middle_x - 1, middle_y, middle_z + 1) not in self.player_white.positions):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x - 1,
                                                   coordinate_y, coordinate_z + 1, second_x - 1, second_y,
                                                   second_z + 1, middle_x - 1, middle_y, middle_z + 1)
            return True

        elif (to_x == coordinate_x + 1 and to_y == coordinate_y and to_z == coordinate_z - 1
              and (second_x + 1, second_y, second_z - 1) not in self.player_black.positions
              and (second_x + 1, second_y, second_z - 1) not in self.player_white.positions
              and (middle_x + 1, middle_y, middle_z - 1) not in self.player_black.positions
              and (middle_x + 1, middle_y, middle_z - 1) not in self.player_white.positions) or \
                (to_x == second_x + 1 and to_y == second_y and to_z == second_z - 1
                 and (coordinate_x + 1, coordinate_y, coordinate_z - 1) not in self.player_black.positions
                 and (coordinate_x + 1, coordinate_y, coordinate_z - 1) not in self.player_white.positions
                 and (middle_x + 1, middle_y, middle_z - 1) not in self.player_black.positions
                 and (middle_x + 1, middle_y, middle_z - 1) not in self.player_white.positions):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x + 1,
                                                   coordinate_y, coordinate_z - 1, second_x + 1, second_y,
                                                   second_z - 1, middle_x + 1, middle_y, middle_z - 1)
            return True

        elif (to_x == coordinate_x and to_y == coordinate_y + 1 and to_z == coordinate_z + 1
              and (second_x, second_y + 1, second_z + 1) not in self.player_black.positions
              and (second_x, second_y + 1, second_z + 1) not in self.player_white.positions
              and (middle_x, middle_y + 1, middle_z + 1) not in self.player_black.positions
              and (middle_x, middle_y + 1, middle_z + 1) not in self.player_white.positions) or \
                (to_x == second_x and to_y == second_y + 1 and to_z == second_z + 1
                 and (coordinate_x, coordinate_y + 1, coordinate_z + 1) not in self.player_black.positions
                 and (coordinate_x, coordinate_y + 1, coordinate_z + 1) not in self.player_white.positions
                 and (middle_x, middle_y + 1, middle_z + 1) not in self.player_black.positions
                 and (middle_x, middle_y + 1, middle_z + 1) not in self.player_white.positions):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x,
                                                   coordinate_y + 1, coordinate_z + 1, second_x, second_y + 1,
                                                   second_z + 1, middle_x, middle_y + 1, middle_z + 1)
            return True

        elif (to_x == coordinate_x and to_y == coordinate_y - 1 and to_z == coordinate_z - 1
              and (second_x, second_y - 1, second_z - 1) not in self.player_black.positions
              and (second_x, second_y - 1, second_z - 1) not in self.player_white.positions
              and (middle_x, middle_y - 1, middle_z - 1) not in self.player_black.positions
              and (middle_x, middle_y - 1, middle_z - 1) not in self.player_white.positions) or \
                (to_x == second_x and to_y == second_y - 1 and to_z == second_z - 1
                 and (coordinate_x, coordinate_y - 1, coordinate_z - 1) not in self.player_black.positions
                 and (coordinate_x, coordinate_y - 1, coordinate_z - 1) not in self.player_white.positions
                 and (middle_x, middle_y - 1, middle_z - 1) not in self.player_black.positions
                 and (middle_x, middle_y - 1, middle_z - 1) not in self.player_white.positions):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x,
                                                   coordinate_y - 1, coordinate_z - 1, second_x, second_y - 1,
                                                   second_z - 1, middle_x, middle_y - 1, middle_z - 1)
            return True
        return False

    def change_triple_broadside_positions(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                          second_z, middle_x, middle_y, middle_z, new_coordinate_x, new_coordinate_y,
                                          new_coordinate_z, new_second_x, new_second_y, new_second_z, new_middle_x,
                                          new_middle_y, new_middle_z):
        if (coordinate_x, coordinate_y, coordinate_z) in self.player_black.positions and \
             (second_x, second_y, second_z) in self.player_black.positions:
            # checking if new positions are not on other pieces
            if (new_coordinate_x, new_coordinate_y, new_coordinate_z) not in self.player_black.positions \
                    and (new_second_x, new_second_y, new_second_z) not in self.player_black.positions \
                    and (new_middle_x, new_middle_y, new_middle_z) not in self.player_black.positions:
                self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                self.player_black.positions.remove((middle_x, middle_y, middle_z))
                self.player_black.positions.remove((second_x, second_y, second_z))
                self.player_black.positions.add((new_coordinate_x, new_coordinate_y, new_coordinate_z))
                self.player_black.positions.add((new_middle_x, new_middle_y, new_middle_z))
                self.player_black.positions.add((new_second_x, new_second_y, new_second_z))
                return True
        elif (coordinate_x, coordinate_y, coordinate_z) in self.player_white.positions and \
             (second_x, second_y, second_z) in self.player_white.positions:
            # checking if new positions are not on other pieces
            if (new_coordinate_x, new_coordinate_y, new_coordinate_z) not in self.player_white.positions \
                    and (new_second_x, new_second_y, new_second_z) not in self.player_white.positions \
                    and (new_middle_x, new_middle_y, new_middle_z) not in self.player_white.positions:
                self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                self.player_white.positions.remove((middle_x, middle_y, middle_z))
                self.player_white.positions.remove((second_x, second_y, second_z))
                self.player_white.positions.add((new_coordinate_x, new_coordinate_y, new_coordinate_z))
                self.player_white.positions.add((new_middle_x, new_middle_y, new_middle_z))
                self.player_white.positions.add((new_second_x, new_second_y, new_second_z))
                return True
        return False

    def black_sumito_for_coord_x(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                 to_y, to_z):
        if to_y == coordinate_y + 1 and to_z == coordinate_z + 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x, to_y + 1, to_z + 1) in self.player_white.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x, to_y + 2, to_z + 2) in self.player_white.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x, to_y + 2, to_z + 2) not in self.player_white.positions and (to_x, to_y + 2, to_z +2) \
                    not in self.player_black.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_x == second_x and fabs(coordinate_y-second_y) == 2 and fabs(coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x, to_y + 1, to_z + 1) in self.borders_of_board_for_x:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.remove((second_x, second_y, second_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                            self.points_for_black += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x, to_y + 1, to_z + 1) not in self.borders_of_board_for_x:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.add((to_x, to_y + 2, to_z + 2))
                            self.player_black.positions.remove((second_x, second_y, second_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                    # jest po równo dwie kule
                    elif coordinate_x == second_x and fabs(coordinate_y-second_y) == 1 and fabs(coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x, to_y + 1, to_z + 1) not in self.player_white.positions and \
                (to_x, to_y + 1, to_z + 1) not in self.player_black.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board_for_x:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.remove((second_x, second_y, second_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
                    self.points_for_black += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board_for_x:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.add((to_x, to_y + 1, to_z + 1))
                    self.player_black.positions.remove((second_x, second_y, second_z))
                    self.player_black.positions.add((to_x, to_y, to_z))

        elif to_y == coordinate_y - 1 and to_z == coordinate_z - 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x, to_y - 1, to_z - 1) in self.player_white.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x, to_y - 2, to_z - 2) in self.player_white.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x, to_y - 2, to_z - 2) not in self.player_white.positions and (to_x, to_y - 2, to_z - 2) \
                        not in self.player_black.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_x == second_x and fabs(coordinate_y - second_y) == 2 and fabs(
                       coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x, to_y - 1, to_z - 1) in self.borders_of_board_for_x:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.remove((second_x, second_y, second_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                            self.points_for_black += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x, to_y - 1, to_z - 1) not in self.borders_of_board_for_x:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.add((to_x, to_y - 2, to_z - 2))
                            self.player_black.positions.remove((second_x, second_y, second_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                        # jest po równo dwie kule
                    elif coordinate_x == second_x and fabs(coordinate_y - second_y) == 1 and fabs(
                          coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x, to_y - 1, to_z - 1) not in self.player_white.positions and \
                    (to_x, to_y - 1, to_z - 1) not in self.player_black.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board_for_x:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.remove((second_x, second_y, second_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
                    self.points_for_black += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board_for_x:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.add((to_x, to_y - 1, to_z - 1))
                    self.player_black.positions.remove((second_x, second_y, second_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
        return False

    def black_sumito_for_sec_x(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                               to_y, to_z):
        if to_y == second_y + 1 and to_z == second_z + 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x, to_y + 1, to_z + 1) in self.player_white.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x, to_y + 2, to_z +2) in self.player_white.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x, to_y + 2, to_z +2) not in self.player_white.positions and (to_x, to_y + 2, to_z +2) \
                    not in self.player_black.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_x == second_x and fabs(coordinate_y-second_y) == 2 and fabs(coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x, to_y + 1, to_z + 1) in self.borders_of_board_for_x:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                            self.points_for_black += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x, to_y + 1, to_z + 1) not in self.borders_of_board_for_x:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.add((to_x, to_y + 2, to_z + 2))
                            self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                    # jest po równo dwie kule
                    elif coordinate_x == second_x and fabs(coordinate_y-second_y) == 1 and fabs(coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x, to_y + 1, to_z + 1) not in self.player_white.positions and \
                (to_x, to_y + 1, to_z + 1) not in self.player_black.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board_for_x:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
                    self.points_for_black += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board_for_x:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.add((to_x, to_y + 1, to_z + 1))
                    self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_black.positions.add((to_x, to_y, to_z))

        elif to_y == second_y - 1 and to_z == second_z - 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x, to_y - 1, to_z - 1) in self.player_white.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x, to_y - 2, to_z - 2) in self.player_white.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x, to_y - 2, to_z - 2) not in self.player_white.positions and (to_x, to_y - 2, to_z - 2) \
                        not in self.player_black.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_x == second_x and fabs(coordinate_y - second_y) == 2 and fabs(
                       coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x, to_y - 1, to_z - 1) in self.borders_of_board_for_x:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                            self.points_for_black += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x, to_y - 1, to_z - 1) not in self.borders_of_board_for_x:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.add((to_x, to_y - 2, to_z - 2))
                            self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                        # jest po równo dwie kule
                    elif coordinate_x == second_x and fabs(coordinate_y - second_y) == 1 and fabs(
                          coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x, to_y - 1, to_z - 1) not in self.player_white.positions and \
                    (to_x, to_y - 1, to_z - 1) not in self.player_black.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board_for_x:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
                    self.points_for_black += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board_for_x:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.add((to_x, to_y - 1, to_z - 1))
                    self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
        return False

    def white_sumito_for_coord_x(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                 to_y, to_z):
        if to_y == coordinate_y + 1 and to_z == coordinate_z + 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x, to_y + 1, to_z + 1) in self.player_black.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x, to_y + 2, to_z +2) in self.player_black.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x, to_y + 2, to_z +2) not in self.player_black.positions and (to_x, to_y + 2, to_z +2) \
                    not in self.player_white.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_x == second_x and fabs(coordinate_y-second_y) == 2 and fabs(coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x, to_y + 1, to_z + 1) in self.borders_of_board_for_x:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.remove((second_x, second_y, second_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                            self.points_for_white += 1
                            # punkt dla białych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x, to_y + 1, to_z + 1) not in self.borders_of_board_for_x:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.add((to_x, to_y + 2, to_z + 2))
                            self.player_white.positions.remove((second_x, second_y, second_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                    # jest po równo dwie kule
                    elif coordinate_x == second_x and fabs(coordinate_y-second_y) == 1 and fabs(coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x, to_y + 1, to_z + 1) not in self.player_black.positions and \
                (to_x, to_y + 1, to_z + 1) not in self.player_white.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board_for_x:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.remove((second_x, second_y, second_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
                    self.points_for_white += 1
                    # punkt dla białych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board_for_x:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.add((to_x, to_y + 1, to_z + 1))
                    self.player_white.positions.remove((second_x, second_y, second_z))
                    self.player_white.positions.add((to_x, to_y, to_z))

        elif to_y == coordinate_y - 1 and to_z == coordinate_z - 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x, to_y - 1, to_z - 1) in self.player_black.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x, to_y - 2, to_z - 2) in self.player_black.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x, to_y - 2, to_z - 2) not in self.player_black.positions and (to_x, to_y - 2, to_z - 2) \
                        not in self.player_white.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_x == second_x and fabs(coordinate_y - second_y) == 2 and fabs(
                       coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x, to_y - 1, to_z - 1) in self.borders_of_board_for_x:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.remove((second_x, second_y, second_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                            self.points_for_white += 1
                            # punkt dla białych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x, to_y - 1, to_z - 1) not in self.borders_of_board_for_x:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.add((to_x, to_y - 2, to_z - 2))
                            self.player_white.positions.remove((second_x, second_y, second_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                        # jest po równo dwie kule
                    elif coordinate_x == second_x and fabs(coordinate_y - second_y) == 1 and fabs(
                          coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x, to_y - 1, to_z - 1) not in self.player_black.positions and \
                    (to_x, to_y - 1, to_z - 1) not in self.player_white.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board_for_x:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.remove((second_x, second_y, second_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
                    self.points_for_white += 1
                    # punkt dla białych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board_for_x:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.add((to_x, to_y - 1, to_z - 1))
                    self.player_white.positions.remove((second_x, second_y, second_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
        return False

    def white_sumito_for_sec_x(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                               to_y, to_z):
        if to_y == second_y + 1 and to_z == second_z + 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x, to_y + 1, to_z + 1) in self.player_black.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x, to_y + 2, to_z +2) in self.player_black.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x, to_y + 2, to_z +2) not in self.player_black.positions and (to_x, to_y + 2, to_z +2) \
                    not in self.player_white.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_x == second_x and fabs(coordinate_y-second_y) == 2 and fabs(coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x, to_y + 1, to_z + 1) in self.borders_of_board_for_x:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                            self.points_for_white += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x, to_y + 1, to_z + 1) not in self.borders_of_board_for_x:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.add((to_x, to_y + 2, to_z + 2))
                            self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                    # jest po równo dwie kule
                    elif coordinate_x == second_x and fabs(coordinate_y-second_y) == 1 and fabs(coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x, to_y + 1, to_z + 1) not in self.player_black.positions and \
                (to_x, to_y + 1, to_z + 1) not in self.player_white.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board_for_x:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
                    self.points_for_white += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board_for_x:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.add((to_x, to_y + 1, to_z + 1))
                    self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_white.positions.add((to_x, to_y, to_z))

        elif to_y == second_y - 1 and to_z == second_z - 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x, to_y - 1, to_z - 1) in self.player_black.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x, to_y - 2, to_z - 2) in self.player_black.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x, to_y - 2, to_z - 2) not in self.player_black.positions and (to_x, to_y - 2, to_z - 2) \
                        not in self.player_white.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_x == second_x and fabs(coordinate_y - second_y) == 2 and fabs(
                       coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x, to_y - 1, to_z - 1) in self.borders_of_board_for_x:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                            self.points_for_white += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x, to_y - 1, to_z - 1) not in self.borders_of_board_for_x:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.add((to_x, to_y - 2, to_z - 2))
                            self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                        # jest po równo dwie kule
                    elif coordinate_x == second_x and fabs(coordinate_y - second_y) == 1 and fabs(
                          coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x, to_y - 1, to_z - 1) not in self.player_black.positions and \
                    (to_x, to_y - 1, to_z - 1) not in self.player_white.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board_for_x:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
                    self.points_for_white += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board_for_x:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.add((to_x, to_y - 1, to_z - 1))
                    self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
        return False

    def black_sumito_for_coord_y(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                 to_y, to_z):
        if to_x == coordinate_x + 1 and to_z == coordinate_z - 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x + 1, to_y, to_z - 1) in self.player_white.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x + 2, to_y, to_z - 2) in self.player_white.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x + 2, to_y, to_z - 2) not in self.player_white.positions and (to_x + 2, to_y, to_z - 2) \
                        not in self.player_black.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_y == second_y and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x + 1, to_y, to_z - 1) in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.remove((second_x, second_y, second_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                            self.points_for_black += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x + 1, to_y, to_z - 1) not in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.add((to_x + 2, to_y, to_z - 2))
                            self.player_black.positions.remove((second_x, second_y, second_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                    # jest po równo dwie kule
                    elif coordinate_y == second_y and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x + 1, to_y, to_z - 1) not in self.player_white.positions and \
                    (to_x + 1, to_y, to_z - 1) not in self.player_black.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.remove((second_x, second_y, second_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
                    self.points_for_black += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.add((to_x + 1, to_y, to_z - 1))
                    self.player_black.positions.remove((second_x, second_y, second_z))
                    self.player_black.positions.add((to_x, to_y, to_z))

        elif to_x == coordinate_x - 1 and to_z == coordinate_z + 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x - 1, to_y, to_z + 1) in self.player_white.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x - 2, to_y, to_z + 2) in self.player_white.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x - 2, to_y, to_z + 2) not in self.player_white.positions and (to_x - 2, to_y, to_z + 2) \
                        not in self.player_black.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_y == second_y and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x - 1, to_y, to_z + 1) in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.remove((second_x, second_y, second_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                            self.points_for_black += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x - 1, to_y, to_z + 1) not in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.add((to_x - 2, to_y, to_z + 2))
                            self.player_black.positions.remove((second_x, second_y, second_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                        # jest po równo dwie kule
                    elif coordinate_y == second_y and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x - 1, to_y, to_z + 1) not in self.player_white.positions and \
                    (to_x - 1, to_y, to_z + 1) not in self.player_black.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.remove((second_x, second_y, second_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
                    self.points_for_black += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.add((to_x - 1, to_y, to_z + 1))
                    self.player_black.positions.remove((second_x, second_y, second_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
        return False

    def black_sumito_for_sec_y(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                               to_y, to_z):
        if to_x == second_x + 1 and to_z == second_z - 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x + 1, to_y, to_z - 1) in self.player_white.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x + 2, to_y, to_z - 2) in self.player_white.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x + 2, to_y, to_z - 2) not in self.player_white.positions and (to_x + 2, to_y, to_z - 2) \
                        not in self.player_black.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_y == second_y and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x + 1, to_y, to_z - 1) in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                            self.points_for_black += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x + 1, to_y, to_z - 1) not in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.add((to_x + 2, to_y, to_z - 2))
                            self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                    # jest po równo dwie kule
                    elif coordinate_y == second_y and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x + 1, to_y, to_z - 1) not in self.player_white.positions and \
                    (to_x + 1, to_y, to_z - 1) not in self.player_black.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
                    self.points_for_black += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.add((to_x + 1, to_y, to_z - 1))
                    self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_black.positions.add((to_x, to_y, to_z))

        elif to_x == second_x - 1 and to_z == second_z + 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x - 1, to_y, to_z + 1) in self.player_white.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x - 2, to_y, to_z + 2) in self.player_white.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x - 2, to_y, to_z + 2) not in self.player_white.positions and (to_x - 2, to_y, to_z + 2) \
                        not in self.player_black.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_y == second_y and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x - 1, to_y, to_z + 1) in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                            self.points_for_black += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x - 1, to_y, to_z + 1) not in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.add((to_x - 2, to_y, to_z + 2))
                            self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                        # jest po równo dwie kule
                    elif coordinate_y == second_y and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x - 1, to_y, to_z + 1) not in self.player_white.positions and \
                    (to_x - 1, to_y, to_z + 1) not in self.player_black.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
                    self.points_for_black += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.add((to_x - 1, to_y, to_z + 1))
                    self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
        return False

    def white_sumito_for_coord_y(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                 to_y, to_z):
        if to_x == coordinate_x + 1 and to_z == coordinate_z - 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x + 1, to_y, to_z - 1) in self.player_black.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x + 2, to_y, to_z - 2) in self.player_black.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x + 2, to_y, to_z - 2) not in self.player_black.positions and (to_x + 2, to_y, to_z - 2) \
                        not in self.player_white.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_y == second_y and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x + 1, to_y, to_z - 1) in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.remove((second_x, second_y, second_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                            self.points_for_white += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x + 1, to_y, to_z - 1) not in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.add((to_x + 2, to_y, to_z - 2))
                            self.player_white.positions.remove((second_x, second_y, second_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                    # jest po równo dwie kule
                    elif coordinate_y == second_y and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x + 1, to_y, to_z - 1) not in self.player_black.positions and \
                    (to_x + 1, to_y, to_z - 1) not in self.player_white.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.remove((second_x, second_y, second_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
                    self.points_for_white += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.add((to_x + 1, to_y, to_z - 1))
                    self.player_white.positions.remove((second_x, second_y, second_z))
                    self.player_white.positions.add((to_x, to_y, to_z))

        elif to_x == coordinate_x - 1 and to_z == coordinate_z + 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x - 1, to_y, to_z + 1) in self.player_black.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x - 2, to_y, to_z + 2) in self.player_black.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x - 2, to_y, to_z + 2) not in self.player_black.positions and (to_x - 2, to_y, to_z + 2) \
                        not in self.player_white.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_y == second_y and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x - 1, to_y, to_z + 1) in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.remove((second_x, second_y, second_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                            self.points_for_white += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x - 1, to_y, to_z + 1) not in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.add((to_x - 2, to_y, to_z + 2))
                            self.player_white.positions.remove((second_x, second_y, second_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                        # jest po równo dwie kule
                    elif coordinate_y == second_y and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x - 1, to_y, to_z + 1) not in self.player_black.positions and \
                    (to_x - 1, to_y, to_z + 1) not in self.player_white.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.remove((second_x, second_y, second_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
                    self.points_for_white += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.add((to_x - 1, to_y, to_z + 1))
                    self.player_white.positions.remove((second_x, second_y, second_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
        return False

    def white_sumito_for_sec_y(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                               to_y, to_z):
        if to_x == second_x + 1 and to_z == second_z - 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x + 1, to_y, to_z - 1) in self.player_black.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x + 2, to_y, to_z - 2) in self.player_black.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x + 2, to_y, to_z - 2) not in self.player_black.positions and (to_x + 2, to_y, to_z - 2) \
                        not in self.player_white.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_y == second_y and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x + 1, to_y, to_z - 1) in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                            self.points_for_white += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x + 1, to_y, to_z - 1) not in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.add((to_x + 2, to_y, to_z - 2))
                            self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                    # jest po równo dwie kule
                    elif coordinate_y == second_y and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x + 1, to_y, to_z - 1) not in self.player_black.positions and \
                    (to_x + 1, to_y, to_z - 1) not in self.player_white.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
                    self.points_for_white += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.add((to_x + 1, to_y, to_z - 1))
                    self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_white.positions.add((to_x, to_y, to_z))

        elif to_x == second_x - 1 and to_z == second_z + 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x - 1, to_y, to_z + 1) in self.player_black.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x - 2, to_y, to_z + 2) in self.player_black.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x - 2, to_y, to_z + 2) not in self.player_black.positions and (to_x - 2, to_y, to_z + 2) \
                        not in self.player_white.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_y == second_y and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_z - second_z) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x - 1, to_y, to_z + 1) in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                            self.points_for_white += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x - 1, to_y, to_z + 1) not in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.add((to_x - 2, to_y, to_z + 2))
                            self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                        # jest po równo dwie kule
                    elif coordinate_y == second_y and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_z - second_z) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x - 1, to_y, to_z + 1) not in self.player_black.positions and \
                    (to_x - 1, to_y, to_z + 1) not in self.player_white.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
                    self.points_for_white += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.add((to_x - 1, to_y, to_z + 1))
                    self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
        return False

    def black_sumito_for_coord_z(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                 to_y, to_z):
        if to_x == coordinate_x + 1 and to_y == coordinate_y + 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x + 1, to_y + 1, to_z) in self.player_white.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x + 2, to_y + 2, to_z) in self.player_white.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x + 2, to_y + 2, to_z) not in self.player_white.positions and (to_x + 2, to_y + 2, to_z) \
                        not in self.player_black.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_z == second_z and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_y - second_y) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x + 1, to_y + 1, to_z) in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.remove((second_x, second_y, second_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                            self.points_for_black += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x + 1, to_y + 1, to_z) not in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.add((to_x + 2, to_y + 2, to_z))
                            self.player_black.positions.remove((second_x, second_y, second_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                    # jest po równo dwie kule
                    elif coordinate_z == second_z and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_y - second_y) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x + 1, to_y + 1, to_z) not in self.player_white.positions and \
                    (to_x + 1, to_y + 1, to_z) not in self.player_black.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.remove((second_x, second_y, second_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
                    self.points_for_black += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.add((to_x + 1, to_y + 1, to_z))
                    self.player_black.positions.remove((second_x, second_y, second_z))
                    self.player_black.positions.add((to_x, to_y, to_z))

        elif to_x == coordinate_x - 1 and to_y == coordinate_y - 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x - 1, to_y - 1, to_z) in self.player_white.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x - 2, to_y - 2, to_z) in self.player_white.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x - 2, to_y - 2, to_z) not in self.player_white.positions and (to_x - 2, to_y - 2, to_z) \
                        not in self.player_black.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_z == second_z and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_y - second_y) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x - 1, to_y - 1, to_z) in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.remove((second_x, second_y, second_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                            self.points_for_black += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x - 1, to_y - 1, to_z) not in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.add((to_x - 2, to_y - 2, to_z))
                            self.player_black.positions.remove((second_x, second_y, second_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                        # jest po równo dwie kule
                    elif coordinate_z == second_z and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_y - second_y) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x - 1, to_y - 1, to_z) not in self.player_white.positions and \
                    (to_x - 1, to_y - 1, to_z) not in self.player_black.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.remove((second_x, second_y, second_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
                    self.points_for_black += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.add((to_x - 1, to_y - 1, to_z))
                    self.player_black.positions.remove((second_x, second_y, second_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
        return False

    def black_sumito_for_sec_z(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                               to_y, to_z):
        if to_x == second_x + 1 and to_y == second_y + 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x + 1, to_y + 1, to_z) in self.player_white.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x + 2, to_y + 2, to_z) in self.player_white.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x + 2, to_y + 2, to_z) not in self.player_white.positions and (to_x + 2, to_y + 2, to_z) \
                        not in self.player_black.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_z == second_z and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_y - second_y) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x + 1, to_y + 1, to_z) in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                            self.points_for_black += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x + 1, to_y + 1, to_z) not in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.add((to_x + 2, to_y + 2, to_z))
                            self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                    # jest po równo dwie kule
                    elif coordinate_z == second_z and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_y - second_y) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x + 1, to_y + 1, to_z) not in self.player_white.positions and \
                    (to_x + 1, to_y + 1, to_z) not in self.player_black.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
                    self.points_for_black += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.add((to_x + 1, to_y + 1, to_z))
                    self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_black.positions.add((to_x, to_y, to_z))

        elif to_x == second_x - 1 and to_y == second_y - 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x - 1, to_y - 1, to_z) in self.player_white.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x - 2, to_y - 2, to_z) in self.player_white.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x - 2, to_y - 2, to_z) not in self.player_white.positions and (to_x - 2, to_y - 2, to_z) \
                        not in self.player_black.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_z == second_z and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_y - second_y) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x - 1, to_y - 1, to_z) in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                            self.points_for_black += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x - 1, to_y - 1, to_z) not in self.borders_of_board:
                            self.player_white.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.add((to_x - 2, to_y - 2, to_z))
                            self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_black.positions.add((to_x, to_y, to_z))
                        # jest po równo dwie kule
                    elif coordinate_z == second_z and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_y - second_y) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x - 1, to_y - 1, to_z) not in self.player_white.positions and \
                    (to_x - 1, to_y - 1, to_z) not in self.player_black.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
                    self.points_for_black += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_white.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.add((to_x - 1, to_y - 1, to_z))
                    self.player_black.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_black.positions.add((to_x, to_y, to_z))
        return False

    def white_sumito_for_coord_z(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                 to_y, to_z):
        if to_x == coordinate_x + 1 and to_y == coordinate_y + 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x + 1, to_y + 1, to_z) in self.player_black.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x + 2, to_y + 2, to_z) in self.player_black.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x + 2, to_y + 2, to_z) not in self.player_black.positions and (to_x + 2, to_y + 2, to_z) \
                        not in self.player_white.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_z == second_z and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_y - second_y) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x + 1, to_y + 1, to_z) in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.remove((second_x, second_y, second_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                            self.points_for_white += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x + 1, to_y + 1, to_z) not in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.add((to_x + 2, to_y + 2, to_z))
                            self.player_white.positions.remove((second_x, second_y, second_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                    # jest po równo dwie kule
                    elif coordinate_z == second_z and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_y - second_y) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x + 1, to_y + 1, to_z) not in self.player_black.positions and \
                    (to_x + 1, to_y + 1, to_z) not in self.player_white.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.remove((second_x, second_y, second_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
                    self.points_for_white += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.add((to_x + 1, to_y + 1, to_z))
                    self.player_white.positions.remove((second_x, second_y, second_z))
                    self.player_white.positions.add((to_x, to_y, to_z))

        elif to_x == coordinate_x - 1 and to_y == coordinate_y - 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x - 1, to_y - 1, to_z) in self.player_black.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x - 2, to_y - 2, to_z) in self.player_black.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x - 2, to_y - 2, to_z) not in self.player_black.positions and (to_x - 2, to_y - 2, to_z) \
                        not in self.player_white.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_z == second_z and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_y - second_y) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x - 1, to_y - 1, to_z) in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.remove((second_x, second_y, second_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                            self.points_for_white += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x - 1, to_y - 1, to_z) not in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.add((to_x - 2, to_y - 2, to_z))
                            self.player_white.positions.remove((second_x, second_y, second_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                        # jest po równo dwie kule
                    elif coordinate_z == second_z and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_y - second_y) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x - 1, to_y - 1, to_z) not in self.player_black.positions and \
                    (to_x - 1, to_y - 1, to_z) not in self.player_white.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.remove((second_x, second_y, second_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
                    self.points_for_white += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.add((to_x - 1, to_y - 1, to_z))
                    self.player_white.positions.remove((second_x, second_y, second_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
        return False

    def white_sumito_for_sec_z(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                               to_y, to_z):
        if to_x == second_x + 1 and to_y == second_y + 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x + 1, to_y + 1, to_z) in self.player_black.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x + 2, to_y + 2, to_z) in self.player_black.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x + 2, to_y + 2, to_z) not in self.player_black.positions and (to_x + 2, to_y + 2, to_z) \
                        not in self.player_white.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_z == second_z and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_y - second_y) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x + 1, to_y + 1, to_z) in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                            self.points_for_white += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x + 1, to_y + 1, to_z) not in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.add((to_x + 2, to_y + 2, to_z))
                            self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                    # jest po równo dwie kule
                    elif coordinate_z == second_z and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_y - second_y) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x + 1, to_y + 1, to_z) not in self.player_black.positions and \
                    (to_x + 1, to_y + 1, to_z) not in self.player_white.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
                    self.points_for_white += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.add((to_x + 1, to_y + 1, to_z))
                    self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_white.positions.add((to_x, to_y, to_z))

        elif to_x == second_x - 1 and to_y == second_y - 1:
            # sytuacja kiedy jest więcej niż jedna kulka przeciwnika
            if (to_x - 1, to_y - 1, to_z) in self.player_black.positions:
                # sytuacja kiedy są trzy kulki przeciwnika (na pewno nie da sie zbic)
                if (to_x - 2, to_y - 2, to_z) in self.player_black.positions:
                    return False
                # sytuacja kiedy są dwie kulki przeciwnika
                elif (to_x - 2, to_y - 2, to_z) not in self.player_black.positions and (to_x - 2, to_y - 2, to_z) \
                        not in self.player_white.positions:
                    # funkcja sprawdzajaca przewage liczebna(czy był select trzech kul czyli sprawdz jaka roznica miedzy coord i second)
                    if coordinate_z == second_z and fabs(coordinate_x - second_x) == 2 and fabs(
                            coordinate_y - second_y) == 2:
                        # sytuacja kiedy są dwie kule przeciwnika i jedna jest na granicy planszy
                        if (to_x - 1, to_y - 1, to_z) in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                            self.points_for_white += 1
                            # punkt dla czarnych
                        # sytuacja kiedy nie jest na granicy
                        elif (to_x - 1, to_y - 1, to_z) not in self.borders_of_board:
                            self.player_black.positions.remove((to_x, to_y, to_z))
                            self.player_black.positions.add((to_x - 2, to_y - 2, to_z))
                            self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                            self.player_white.positions.add((to_x, to_y, to_z))
                        # jest po równo dwie kule
                    elif coordinate_z == second_z and fabs(coordinate_x - second_x) == 1 and fabs(
                            coordinate_y - second_y) == 1:
                        return False
            # sytuacja kiedy jest jedna kulka przeciwnika i za nią nie stoi nasza, na pewno do zbicia
            elif (to_x - 1, to_y - 1, to_z) not in self.player_black.positions and \
                    (to_x - 1, to_y - 1, to_z) not in self.player_white.positions:
                # sprawdzenie czy jest na granicy
                if (to_x, to_y, to_z) in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
                    self.points_for_white += 1
                    # punkt dla czarnych
                # jeśli nie jest na granicy
                elif (to_x, to_y, to_z) not in self.borders_of_board:
                    self.player_black.positions.remove((to_x, to_y, to_z))
                    self.player_black.positions.add((to_x - 1, to_y - 1, to_z))
                    self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                    self.player_white.positions.add((to_x, to_y, to_z))
        return False

    def check_end_of_game(self, points_for_black, points_for_white):
        if points_for_black == 6:
            self.finish = 1
            return True
        elif points_for_white == 6:
            self.finish = 2
            return True
        elif points_for_black == points_for_white == 6:
            self.finish = 3
            return True
        return False

# warunki co do new_x , zeby bylo wolne niezastawione przez jakis pion
# zabezpieczenia co do ruchu trzema kulami(nie moze stac kula innego gracza, nie moze stac kula tego samego)
# bicia do debugingu