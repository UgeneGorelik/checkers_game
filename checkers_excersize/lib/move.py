from typing import List

from lib.board import Board
from lib.checkers_constants import WHITE, BLACK, DIAGONALLY_DOWN_RIGHT, \
    DIAGONALLY_UP_RIGHT, DIAGONALLY_DOWN_LEFT, DIAGONALLY_UP_LEFT


class Move(object):
    """
    class for managing the checker move itself
    checking if it is ok to make it and move the pieces
    Attributes:
        color (string): color of the player
        board (2*2matrix): checkers board
        source_x (int):
        source_y (2int):
        target_x (int):
        target_y (2int:
        move_type (2*2matrix): jump / normal
        jump_spot_x (int):
        jump_spot_y (int):
        pos_as_list (2int): list for the move
        jump_status (int): if we made jump
        jumped_locaton (int): where we jumped
        tie_status (int): if tie
        check_jumps (int): if to check jump
        must_jump_locations (int): available_jump_locations
        available_move_spots (int): available move locations

    """

    def __init__(self, color: str,
                 source_x: int,
                 source_y: int,
                 target_x: int,
                 target_y: int,
                 board: Board,
                 check_jumps: bool = True
                 ):
        self.color = color
        self.board = board
        self.source_x = source_x
        self.source_y = source_y
        self.target_x = target_x
        self.target_y = target_y
        self.move_type = None
        self.jump_spot_x = None
        self.jump_spot_y = None
        self.pos_as_list = [self.source_x, self.source_y, self.target_x, self.target_y]
        self.jump_status = False
        self.jumped_locaton = None
        self.tie_status = False
        self.check_jumps = check_jumps
        self.must_jump_locations = []
        self.available_move_spots = []
        self.get_move_type()

    def check_for_must_jump(self) -> List[List]:
        """
        find out if we have available jumps
        and we must jump
        :return:
        """
        correct_jumps: List[List] = []
        potential_jumps: List[List] = self.board.check_for_nearby_capture_locations(color=self.color,
                                                                                    location=self.jumped_locaton)
        for p_jump in potential_jumps:
            move_class = Move(color=self.color,
                              source_x=p_jump[0],
                              source_y=p_jump[1],
                              target_x=p_jump[2],
                              target_y=p_jump[3],
                              board=self.board,
                              check_jumps=False
                              )
            if move_class.legal_move():
                correct_jumps.append(p_jump)
        self.must_jump_locations = potential_jumps
        return correct_jumps

    def legal_move(self) -> bool:
        """
        check if we can actually do this move
        :return:
        """
        if self.check_jumps and not self.must_jump_and_move_is_correct_jump():
            return False
        if not self.are_move_bounds_ok():
            return False
        if not self.is_there_correct_source_piece():
            return False
        if not self.is_there_empty_space_to_move_to():
            return False
        if self.is_move_jump() and not self.there_is_piece_to_jump():
            return False
        if self.color == WHITE and self.move_type in [DIAGONALLY_UP_LEFT, DIAGONALLY_UP_RIGHT]:
            return True
        if self.color == BLACK and self.move_type in [DIAGONALLY_DOWN_RIGHT, DIAGONALLY_DOWN_LEFT]:
            return True

        return False

    def must_jump_and_move_is_correct_jump(self) -> bool:
        """
        check if we have available jumps and the given move indeed is jump
        :return:
        """
        jump_locations: List[List] = self.check_for_must_jump()

        if jump_locations and self.pos_as_list not in jump_locations:
            return False
        return True

    def make_move(self) -> bool:
        """
        make the move itself and change the pieces on board
        :return:
        """
        self.board.board[self.source_x][self.source_y] = 0

        if self.is_move_jump():
            self.jump_status = True
            self.board.board[self.jump_spot_x][self.jump_spot_y] = 0

        if self.color == WHITE:
            self.board.board[self.target_x][self.target_y] = 1
            if self.is_move_jump():
                self.board.black_pieces -= 1

        if self.color == BLACK:
            self.board.board[self.target_x][self.target_y] = -1
            if self.is_move_jump():
                self.board.white_pieces -= 1
        self.jumped_locaton = [self.target_x, self.target_y]
        return True

    def get_correct_move_locations(self) -> List[List]:
        """
        get all the possible moves for current color
        and check whether they are legal
        :return:
        """
        potential_moves = self.board.get_move_locations(color=self.color)
        correct_moves = []
        for p_jump in potential_moves:
            move_class = Move(color=self.color,
                              source_x=p_jump[0],
                              source_y=p_jump[1],
                              target_x=p_jump[2],
                              target_y=p_jump[3],
                              board=self.board,
                              check_jumps=False
                              )
            if move_class.legal_move():
                correct_moves.append(p_jump)
        return correct_moves

    def check_for_tie(self) -> bool:
        """
        check if this game is a tie
        check if this player can perform any move/jump
        """

        jump_locations = self.check_for_must_jump()
        move_spots = self.get_correct_move_locations()
        available_spots = jump_locations + move_spots
        if not available_spots:
            return True

        return False

    def are_move_bounds_ok(self) -> bool:
        """
        check whether move is not out of bounds
        :return:
        """
        if 8 > self.target_x >= 0 \
                and 8 > self.target_y >= 0 \
                and 8 > self.source_x >= 0 and 8 > self.source_y >= 0:
            return True
        return False

    def is_there_correct_source_piece(self):
        """
        check if this moves star have a piece for this color
        :return:
        """
        board_spot: int = self.board.board[self.source_x][self.source_y]

        if self.color == WHITE and board_spot == 1:
            return True

        if self.color == BLACK and board_spot == -1:
            return True

        return False

    def is_there_empty_space_to_move_to(self):
        board_spot = self.board.board[self.target_x][self.target_y]
        if board_spot == 0:
            return True
        return False

    def is_move_jump(self) -> bool:
        """
        check if this move is actualy a jump
        :return:
        """
        if abs(self.source_x - self.target_x) > 1 and abs(self.source_y - self.target_y) > 1:
            return True
        return False

    def there_is_piece_to_jump(self) -> bool:
        """
        check if the move is jump
        there is a piece to jump over
        :return:
        """
        potential_spot_x: int = None
        potential_spot_y: int = None
        if self.move_type == DIAGONALLY_UP_RIGHT:
            potential_spot_x = self.source_x - 1
            potential_spot_y = self.source_y + 1
        if self.move_type == DIAGONALLY_UP_LEFT:
            potential_spot_x = self.source_x - 1
            potential_spot_y = self.source_y - 1
        if self.move_type == DIAGONALLY_DOWN_LEFT:
            potential_spot_x = self.source_x + 1
            potential_spot_y = self.source_y - 1
        if self.move_type == DIAGONALLY_DOWN_RIGHT:
            potential_spot_x = self.source_x + 1
            potential_spot_y = self.source_y + 1
        board_spot = self.board.board[potential_spot_x][potential_spot_y]
        self.jump_spot_x = potential_spot_x
        self.jump_spot_y = potential_spot_y
        if self.color == WHITE and board_spot == -1:
            return True
        if self.color == BLACK and board_spot == 1:
            return True

        return False

    def is_move_lenght(self) -> bool:
        """
        check whether it is actually a move not a jump
        :return:
        """
        if abs(self.source_y - self.target_y) == 1:
            return True

    def get_move_type(self):
        """
        get the direction of the move
        """
        if self.source_x > self.target_x and self.source_y > self.target_y:
            self.move_type = DIAGONALLY_UP_LEFT

        if self.source_x > self.target_x and self.source_y < self.target_y:
            self.move_type = DIAGONALLY_UP_RIGHT

        if self.source_x < self.target_x and self.source_y > self.target_y:
            self.move_type = DIAGONALLY_DOWN_LEFT

        if self.source_x < self.target_x and self.source_y < self.target_y:
            self.move_type = DIAGONALLY_DOWN_RIGHT
