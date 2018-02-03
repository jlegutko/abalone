from math import fabs
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
        self.turn = 0

    def change_turn(self):
        """
        This method changes the turn from 0 to 1 or from 1 to 0.
        It returns False if something's wrong and the turn is neither 0 or 1. Should not happen.
        :return boolean:
        """
        if self.turn == 0:
            self.turn = 1
            return True
        elif self.turn == 1:
            self.turn = 0
            return True
        return False

    def move(self, coordinate_x, coordinate_y, coordinate_z, to_x, to_y, to_z):
        # Checking in which places ball can move (should be in another function)
        # For white
        if self.turn == 0:
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
        elif self.turn == 1:
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

    def move_multiple(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x, to_y, to_z):
        # checking whether both or three balls are one's player (should be in other function)
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
            # for equal x
            if coordinate_x == second_x:
                # checking if move is broadside
                if to_x != coordinate_x:
                    return self.move_double_broadside_for_x(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                            second_y, second_z, to_x, to_y, to_z)
                # checking if move is inline
                elif to_x == coordinate_x:
                    return self.move_multiple_inline_for_x(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                         second_y, second_z, to_x, to_y, to_z)
            # for equal y
            elif coordinate_y == second_y:
                # checking if move is broadside
                if to_y != coordinate_y:
                    return self.move_double_broadside_for_y(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                            second_y, second_z, to_x, to_y, to_z)
                # checking if move is inline
                elif to_y == coordinate_y:
                    return self.move_multiple_inline_for_y(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                           second_y, second_z, to_x, to_y, to_z)
            # for equal z
            elif coordinate_z == second_z:
                # checking if move is broadside
                if to_z != coordinate_z:
                    return self.move_double_broadside_for_z(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                            second_y, second_z, to_x, to_y, to_z)
                # checking if move is inline
                elif to_z == coordinate_z:
                    return self.move_multiple_inline_for_z(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                           second_y, second_z, to_x, to_y, to_z)
            return False

    def move_double_broadside_for_x(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                    to_y, to_z):
        if (to_x == coordinate_x + 1 and to_y == coordinate_y and to_z == coordinate_z - 1) or \
                (to_x == second_x + 1 and to_y == second_y and to_z == second_z - 1):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x + 1, coordinate_y, coordinate_z - 1,
                                                   second_x + 1, second_y, second_z - 1)

        elif (to_x == coordinate_x + 1 and to_y == coordinate_y + 1 and to_z == coordinate_z) or \
                (to_x == second_x + 1 and to_y == second_y + 1 and to_z == second_z):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x + 1, coordinate_y + 1, coordinate_z,
                                                   second_x + 1, second_y + 1, second_z)

        elif (to_x == coordinate_x - 1 and to_y == coordinate_y and to_z == coordinate_z + 1) or \
                (to_x == second_x - 1 and to_y == second_y and to_z == second_z + 1):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x - 1, coordinate_y, coordinate_z + 1,
                                                   second_x - 1, second_y, second_z + 1)

        elif (to_x == coordinate_x - 1 and to_y == coordinate_y - 1 and to_z == coordinate_z) or \
                (to_x == second_x - 1 and to_y == second_y - 1 and to_z == second_z):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x - 1, coordinate_y - 1, coordinate_z,
                                                   second_x - 1, second_y - 1, second_z)

    def move_multiple_inline_for_x(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x, to_y, to_z):
        if (to_y == coordinate_y + 1 and to_z == coordinate_z + 1) \
                or (to_y == second_y + 1 and to_z == second_z + 1) \
                or (to_y == coordinate_y - 1 and to_z == coordinate_z - 1) \
                or (to_y == second_y - 1 and to_z == second_z - 1):
            if fabs(to_y - coordinate_y) < fabs(to_y - second_y) and \
                    fabs(to_z - coordinate_z) < fabs(to_z - second_z):
                self.player_white.positions.remove((second_x, second_y, second_z))
                self.player_white.positions.add((to_x, to_y, to_z))
                return True
            elif fabs(to_y - second_y) < fabs(to_y - coordinate_y) and \
                    fabs(to_z - second_z) < fabs(to_z - coordinate_z):
                self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                self.player_white.positions.add((to_x, to_y, to_z))
                return True
            return False

    def move_double_broadside_for_y(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                    to_y, to_z):
        if (to_x == coordinate_x - 1 and to_y == coordinate_y - 1 and to_z == coordinate_z) or \
                (to_x == second_x - 1 and to_y == second_y - 1 and to_z == second_z):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x - 1, coordinate_y - 1, coordinate_z,
                                                   second_x - 1, second_y - 1, second_z)

        elif (to_x == coordinate_x and to_y == coordinate_y - 1 and to_z == coordinate_z - 1) or \
                (to_x == second_x and to_y == second_y - 1 and to_z == second_z - 1):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x, coordinate_y - 1, coordinate_z - 1,
                                                   second_x, second_y - 1, second_z - 1)

        elif (to_x == coordinate_x + 1 and to_y == coordinate_y + 1 and to_z == coordinate_z) or \
                (to_x == second_x + 1 and to_y == second_y + 1 and to_z == second_z):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x + 1, coordinate_y + 1, coordinate_z,
                                                   second_x + 1, second_y + 1, second_z)

        elif (to_x == coordinate_x and to_y == coordinate_y + 1 and to_z == coordinate_z + 1) or \
                (to_x == second_x and to_y == second_y + 1 and to_z == second_z + 1):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x, coordinate_y + 1, coordinate_z + 1,
                                                   second_x, second_y + 1, second_z + 1)

    def move_multiple_inline_for_y(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z,
                                   to_x, to_y, to_z):
        if (to_x == coordinate_x + 1 and to_z == coordinate_z - 1) \
                or (to_x == second_x + 1 and to_z == second_z - 1) \
                or (to_x == coordinate_x - 1 and to_z == coordinate_z + 1) \
                or (to_x == second_x - 1 and to_z == second_z + 1):
            if fabs(to_x - coordinate_x) < fabs(to_x - second_x) and \
                    fabs(to_z - coordinate_z) < fabs(to_z - second_z):
                self.player_white.positions.remove((second_x, second_y, second_z))
                self.player_white.positions.add((to_x, to_y, to_z))
            elif fabs(to_x - second_x) < fabs(to_x - coordinate_x) and \
                    fabs(to_z - second_z) < fabs(to_z - coordinate_z):
                self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                self.player_white.positions.add((to_x, to_y, to_z))
            return False

    def move_double_broadside_for_z(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x,
                                    to_y, to_z):
        if (to_x == coordinate_x - 1 and to_y == coordinate_y and to_z == coordinate_z + 1) or \
                (to_x == second_x - 1 and to_y == second_y and to_z == second_z + 1):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x - 1, coordinate_y, coordinate_z + 1,
                                                   second_x - 1, second_y, second_z + 1)

        elif (to_x == coordinate_x + 1 and to_y == coordinate_y and to_z == coordinate_z - 1) or \
                (to_x == second_x + 1 and to_y == second_y and to_z == second_z - 1):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x + 1, coordinate_y, coordinate_z - 1,
                                                   second_x + 1, second_y, second_z - 1)

        elif (to_x == coordinate_x and to_y == coordinate_y + 1 and to_z == coordinate_z + 1) or \
                (to_x == second_x and to_y == second_y + 1 and to_z == second_z + 1):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x, coordinate_y + 1, coordinate_z + 1,
                                                   second_x, second_y + 1, second_z + 1)

        elif (to_x == coordinate_x and to_y == coordinate_y - 1 and to_z == coordinate_z - 1) or \
                (to_x == second_x and to_y == second_y - 1 and to_z == second_z - 1):
            self.change_double_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, coordinate_x, coordinate_y - 1, coordinate_z - 1,
                                                   second_x, second_y - 1, second_z - 1)

    def move_multiple_inline_for_z(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z, to_x, to_y, to_z):
        if (to_x == coordinate_x + 1 and to_y == coordinate_y + 1) \
                or (to_x == second_x + 1 and to_y == second_y + 1) \
                or (to_x == coordinate_x - 1 and to_y == coordinate_y - 1) \
                or (to_x == second_x - 1 and to_y == second_y - 1):
            if fabs(to_x - coordinate_x) < fabs(to_x - second_x) and \
                    fabs(to_y - coordinate_y) < fabs(to_y - second_y):
                self.player_white.positions.remove((second_x, second_y, second_z))
                self.player_white.positions.add((to_x, to_y, to_z))
            elif fabs(to_x - second_x) < fabs(to_x - coordinate_x) and \
                    fabs(to_y - second_y) < fabs(to_y - coordinate_y):
                self.player_white.positions.remove((coordinate_x, coordinate_y, coordinate_z))
                self.player_white.positions.add((to_x, to_y, to_z))
            return False

    def change_double_broadside_positions(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                          second_z, new_coordinate_x, new_coordinate_y, new_coordinate_z,
                                          new_second_x, new_second_y, new_second_z):
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
            # for equal x
            if coordinate_x == second_x:
                # checking whether between balls is the third ball(probably another function)
                if (coordinate_x, (coordinate_y + second_y) / 2, (coordinate_z + second_z) / 2) in self.player_white.positions:
                    middle_x = coordinate_x
                    middle_y = (coordinate_y + second_y) / 2
                    middle_z = (coordinate_z + second_z) / 2
                    # checking if move is broadside
                    if to_x != coordinate_x:
                        return self.move_triple_broadside_for_x(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                                second_y, second_z, middle_x, middle_y, middle_z,
                                                                to_x, to_y, to_z)
                    # checking if move is inline
                    elif to_x == coordinate_x:
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
                    if to_y != coordinate_y:
                        return self.move_triple_broadside_for_y(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                                second_y, second_z, middle_x, middle_y, middle_z,
                                                                to_x, to_y, to_z)
                    # checking if move is inline
                    elif to_y == coordinate_y:
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
                    if to_z != coordinate_z:
                        return self.move_triple_broadside_for_z(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                                second_y, second_z, middle_x, middle_y, middle_z,
                                                                to_x, to_y, to_z)
                    # checking if move is inline
                    elif to_z == coordinate_z:
                        return self.move_multiple_inline_for_z(coordinate_x, coordinate_y, coordinate_z, second_x,
                                                               second_y, second_z, to_x, to_y, to_z)
            return False

    def move_triple_broadside_for_x(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z,
                                    middle_x, middle_y, middle_z, to_x, to_y, to_z):
        if (to_x == coordinate_x + 1 and to_y == coordinate_y and to_z == coordinate_z - 1) or \
                (to_x == second_x + 1 and to_y == second_y and to_z == second_z - 1):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x + 1,
                                                   coordinate_y, coordinate_z - 1, second_x + 1, second_y, second_z - 1,
                                                   middle_x + 1, middle_y, middle_z - 1)

        elif (to_x == coordinate_x + 1 and to_y == coordinate_y + 1 and to_z == coordinate_z) or \
                (to_x == second_x + 1 and to_y == second_y + 1 and to_z == second_z):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x + 1,
                                                   coordinate_y + 1, coordinate_z, second_x + 1, second_y + 1, second_z,
                                                   middle_x + 1, middle_y + 1, middle_z)

        elif (to_x == coordinate_x - 1 and to_y == coordinate_y and to_z == coordinate_z + 1) or \
                (to_x == second_x - 1 and to_y == second_y and to_z == second_z + 1):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x - 1,
                                                   coordinate_y, coordinate_z + 1, second_x - 1, second_y, second_z + 1,
                                                   middle_x - 1, middle_y, middle_z + 1)

        elif (to_x == coordinate_x - 1 and to_y == coordinate_y - 1 and to_z == coordinate_z) or \
                (to_x == second_x - 1 and to_y == second_y - 1 and to_z == second_z):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x - 1,
                                                   coordinate_y - 1, coordinate_z, second_x - 1, second_y - 1, second_z,
                                                   middle_x - 1, middle_y - 1, middle_z)

    def move_triple_broadside_for_y(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z,
                                    middle_x, middle_y, middle_z, to_x, to_y, to_z):
        if (to_x == coordinate_x - 1 and to_y == coordinate_y - 1 and to_z == coordinate_z) or \
                (to_x == second_x - 1 and to_y == second_y - 1 and to_z == second_z):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x - 1,
                                                   coordinate_y - 1, coordinate_z, second_x - 1, second_y - 1, second_z,
                                                   middle_x - 1, middle_y - 1, middle_z)

        elif (to_x == coordinate_x and to_y == coordinate_y - 1 and to_z == coordinate_z - 1) or \
                (to_x == second_x and to_y == second_y - 1 and to_z == second_z - 1):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x, coordinate_y - 1,
                                                   coordinate_z - 1, second_x, second_y - 1, second_z - 1,
                                                   middle_x, middle_y - 1, middle_z - 1)

        elif (to_x == coordinate_x + 1 and to_y == coordinate_y + 1 and to_z == coordinate_z) or \
                (to_x == second_x + 1 and to_y == second_y + 1 and to_z == second_z):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x + 1,
                                                   coordinate_y + 1, coordinate_z, second_x + 1, second_y + 1,
                                                   second_z, middle_x + 1, middle_y + 1, middle_z)

        elif (to_x == coordinate_x and to_y == coordinate_y + 1 and to_z == coordinate_z + 1) or \
                (to_x == second_x and to_y == second_y + 1 and to_z == second_z + 1):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x,
                                                   coordinate_y + 1, coordinate_z + 1, second_x, second_y + 1,
                                                   second_z + 1, middle_x, middle_y + 1, middle_z + 1)

    def move_triple_broadside_for_z(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y, second_z,
                                    middle_x, middle_y, middle_z, to_x, to_y, to_z):
        if (to_x == coordinate_x - 1 and to_y == coordinate_y and to_z == coordinate_z + 1) or \
                (to_x == second_x - 1 and to_y == second_y and to_z == second_z + 1):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x - 1,
                                                   coordinate_y, coordinate_z + 1, second_x - 1, second_y,
                                                   second_z + 1, middle_x - 1, middle_y, middle_z + 1)

        elif (to_x == coordinate_x + 1 and to_y == coordinate_y and to_z == coordinate_z - 1) or \
                (to_x == second_x + 1 and to_y == second_y and to_z == second_z - 1):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x + 1,
                                                   coordinate_y, coordinate_z - 1, second_x + 1, second_y,
                                                   second_z - 1, middle_x + 1, middle_y, middle_z - 1)
        elif (to_x == coordinate_x and to_y == coordinate_y + 1 and to_z == coordinate_z + 1) or \
                (to_x == second_x and to_y == second_y + 1 and to_z == second_z + 1):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x,
                                                   coordinate_y + 1, coordinate_z + 1, second_x, second_y + 1,
                                                   second_z + 1, middle_x, middle_y + 1, middle_z + 1)

        elif (to_x == coordinate_x and to_y == coordinate_y - 1 and to_z == coordinate_z - 1) or \
                (to_x == second_x and to_y == second_y - 1 and to_z == second_z - 1):
            self.change_triple_broadside_positions(coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                                   second_z, middle_x, middle_y, middle_z, coordinate_x,
                                                   coordinate_y - 1, coordinate_z - 1, second_x, second_y - 1,
                                                   second_z - 1, middle_x, middle_y - 1, middle_z - 1)

    def change_triple_broadside_positions(self, coordinate_x, coordinate_y, coordinate_z, second_x, second_y,
                                          second_z, middle_x, middle_y, middle_z, new_coordinate_x, new_coordinate_y,
                                          new_coordinate_z, new_second_x, new_second_y, new_second_z, new_middle_x,
                                          new_middle_y, new_middle_z):
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
