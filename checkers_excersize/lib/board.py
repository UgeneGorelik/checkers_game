from copy import deepcopy
from typing import List

from lib.checkers_config import INIT_BOARD, WHITE, COLOR_NUM_DICT


class Board(object):
    """
    class for checkers board

    Attributes:
        board (2*2 matrix): a checkers board in format
        [[0, -1, 0, -1, 0, -1, 0, -1],
              [-1, 0, -1, 0, -1, 0, -1, 0],
              [0, -1, 0, -1, 0, -1, 0, -1],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [1, 0, 1, 0, 1, 0, 1, 0],
              [0, 1, 0, 1, 0, 1, 0, 1],
              [1, 0, 1, 0, 1, 0, 1, 0]
              ]
        white_pieces (int): number of white pieces.
        black_pieces (black_pieces): number of black pieces.


    """

    def __init__(self):
        self.board: List[List] = None
        self.white_pieces: int = 0
        self.black_pieces: int = 0

    def set_pieces(self):
        """
        init setup :
         [[0, -1, 0, -1, 0, -1, 0, -1],
              [-1, 0, -1, 0, -1, 0, -1, 0],
              [0, -1, 0, -1, 0, -1, 0, -1],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [1, 0, 1, 0, 1, 0, 1, 0],
              [0, 1, 0, 1, 0, 1, 0, 1],
              [1, 0, 1, 0, 1, 0, 1, 0]
              ]


        """
        self.board = deepcopy(INIT_BOARD)
        self.white_pieces = 12
        self.black_pieces = 12

    def find_pieces_of_color(self, color) -> List[List]:
        """
        find the positions of all the pieces of given color
        :param color: color
        :return: list of lists
        """
        find_spots: List = []
        num_to_find = COLOR_NUM_DICT[color]

        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i][j] == num_to_find:
                    find_spots.append([i, j])

        return find_spots

    def check_for_nearby_capture_locations(self, color: str, location=None) -> List[List]:
        """
        get all the spots for specific color that adjacent places can be jumped
        :param color: color
        :param location: check specific location
        :return: list of possible jumps
        """
        if location:
            pieces = [location]
        else:
            pieces: List[List] = self.find_pieces_of_color(color)
        opposite_color: int = - COLOR_NUM_DICT[color]
        potential_jums_list: List[List] = []
        for piece in pieces:
            pos_x: int = piece[0]
            pos_y: int = piece[1]
            if color is WHITE:
                if pos_x < 2:
                    continue
                if pos_y == 7:
                    if self.board[pos_x - 1][pos_y - 1] == opposite_color:
                        potential_jums_list.append([piece[0], piece[1], pos_x - 2, pos_y - 2])

                if pos_y == 0:
                    if self.board[pos_x - 1][pos_y + 1] == opposite_color:
                        potential_jums_list.append([piece[0], piece[1], pos_x - 2, pos_y + 2])

                if not pos_y == 7 and not pos_y == 0:
                    if self.board[pos_x - 1][pos_y + 1] == opposite_color:
                        potential_jums_list.append([piece[0], piece[1], pos_x - 2, pos_y + 2])

                    if self.board[pos_x - 1][pos_y - 1] == opposite_color:
                        potential_jums_list.append([piece[0], piece[1], pos_x - 2, pos_y - 2])

            else:
                if pos_x > 6:
                    continue

                if pos_y == 7:
                    if self.board[pos_x + 1][pos_y - 1] == opposite_color:
                        potential_jums_list.append([piece[0], piece[1], pos_x + 2, pos_y - 2])
                        continue

                if pos_y == 0:
                    if self.board[pos_x + 1][pos_y + 1] == opposite_color:
                        potential_jums_list.append([piece[0], piece[1], pos_x + 2, pos_y + 2])
                        continue
                if not pos_y == 7 and not pos_y == 0:
                    if self.board[pos_x + 1][pos_y + 1] == opposite_color:
                        potential_jums_list.append([piece[0], piece[1], pos_x + 2, pos_y + 2])
                    if self.board[pos_x + 1][pos_y - 1] == opposite_color:
                        potential_jums_list.append([piece[0], piece[1], pos_x + 2, pos_y - 2])
        return potential_jums_list

    def get_move_locations(self, color: str) -> List[List]:
        """
        get all possible move locations for specified color
        :param color: color
        :return:
        """
        move_locations: List[List] = []
        pieces: List[List] = self.find_pieces_of_color(color)
        opposite_color: int = - COLOR_NUM_DICT[color]
        for piece in pieces:
            pos_x: int = piece[0]
            pos_y: int = piece[1]
            if color is WHITE:

                if pos_x == 0:
                    continue
                if pos_y == 0:
                    if self.board[pos_x - 1][pos_y + 1] != opposite_color:
                        move_locations.append([piece[0], piece[1], pos_x - 1, pos_y + 1])
                    continue

                if pos_y == 7:
                    if self.board[pos_x - 1][pos_y - 1] != opposite_color:
                        move_locations.append([piece[0], piece[1], pos_x - 1, pos_y - 1])
                    continue
                if self.board[pos_x - 1][pos_y + 1] != opposite_color:
                    move_locations.append([piece[0], piece[1], pos_x - 1, pos_y + 1])
                if self.board[pos_x - 1][pos_y - 1] != opposite_color:
                    move_locations.append([piece[0], piece[1], pos_x - 1, pos_y - 1])

            else:
                if pos_x == 7:
                    continue
                if pos_y == 0:
                    if self.board[pos_x + 1][pos_y + 1] != opposite_color:
                        move_locations.append([piece[0], piece[1], pos_x + 1, pos_y + 1])
                    continue

                if pos_y == 7:
                    if self.board[pos_x + 1][pos_y - 1] != opposite_color:
                        move_locations.append([piece[0], piece[1], pos_x + 1, pos_y - 1])
                    continue

                if self.board[pos_x + 1][pos_y + 1] != opposite_color:
                    move_locations.append([piece[0], piece[1], pos_x + 1, pos_y + 1])
                if self.board[pos_x + 1][pos_y - 1] != opposite_color:
                    move_locations.append([piece[0], piece[1], pos_x + 1, pos_y - 1])

        return move_locations
