from typing import List

from lib.board import Board
from lib.checkers_constants import GAME_NOT_STARTED, \
    ILLIEGAL_MOVE, WHITE, WHITE_WIN, BLACK_WIN, TIE, BLACK, GAME_IN_PROGRESS, \
    INCOMPLETE_GAME, GAME_RESULT_DICT
from lib.move import Move
from lib.utils import convert_move_entry_to_2d_matrix


class Game(object):
    """
    class for the game of checkers itself rsponsible for managing the board
    moving pieces and discovering the game result

     Attributes:
        board (2*2matrix): checkers board
        game_status (str): game status ( white win ...)
        current_move_colour (str): current_move_colour
        current_move_entry (str): current_move_entry
        line_counter (str): line_counter
        moves (list of lists): list of moves

    """

    def __init__(self, moves: List, board=None):
        self.board: Board = board
        self.game_status: str = GAME_NOT_STARTED
        self.moves: List[List] = moves
        self.current_move_colour: str = WHITE
        self.current_move_entry: List[str] = None
        self.line_counter: int = 0

    def play_game(self):
        """
        play the game itself
        while there are available moves and game not concluded
        pick new move check if it is legal and make the move

        """
        self.game_status = GAME_IN_PROGRESS
        while self.moves and self.game_status \
                not in [WHITE_WIN, BLACK_WIN, TIE, ILLIEGAL_MOVE]:
            self.current_move_entry: List[str] = self.moves.pop(0)
            self.line_counter += 1

            matrix_move_entry: List[int] = convert_move_entry_to_2d_matrix(self.current_move_entry)
            # we are operating on 2*2 matrix and the moves are given as checkers moves
            # we need to transform the moves to 2*2 coordinates
            # ex given 0,1- > 6,7

            move: Move = Move(color=self.current_move_colour,
                              source_x=matrix_move_entry[0],
                              source_y=matrix_move_entry[1],
                              target_x=matrix_move_entry[2],
                              target_y=matrix_move_entry[3],
                              board=self.board,
                              )

            if not move.legal_move():
                self.game_status = ILLIEGAL_MOVE

            else:
                # check if we must jump next move if so then the same color will move next
                # if not we change the color that must run next
                move.make_move()
                player_must_jump: bool = move.check_for_must_jump()
                if self.current_move_colour == WHITE:
                    if self.board.black_pieces == 0:
                        self.game_status = WHITE_WIN
                    elif move.jump_status and player_must_jump:
                        self.current_move_colour = WHITE
                    elif move.jump_status and not player_must_jump:
                        self.current_move_colour = BLACK
                    else:
                        self.current_move_colour = BLACK
                else:
                    if self.board.white_pieces == 0:
                        self.game_status = BLACK_WIN
                    elif move.jump_status and player_must_jump:
                        self.current_move_colour = BLACK
                    elif move.jump_status and not player_must_jump:
                        self.current_move_colour = WHITE
                    else:
                        self.current_move_colour = WHITE
            if move.check_for_tie():
                self.game_status = TIE

        if self.game_status == GAME_IN_PROGRESS and not self.moves:
            self.game_status = INCOMPLETE_GAME

    def print_result(self):
        """
        print  game result
        """
        if self.game_status is ILLIEGAL_MOVE:
            result_str: str = self.generate_incorrect_result_string()
        else:
            result_str: str = GAME_RESULT_DICT[self.game_status]

        print(result_str)

    def generate_incorrect_result_string(self) -> str:
        """
        generate incorrect result string to print
        ex: line 15 illegal move: 1,0,0,5
        :return:
        """
        string_ints: List[str] = [str(x) for x in self.current_move_entry]
        illiegal_move_str: str = ",".join(string_ints)
        result_str: str = f'line {self.line_counter} illegal move: {illiegal_move_str}'
        return result_str

    def start_game(self):
        """
        start the game
        set the board
        init play
        """
        if not self.board:
            self.board: Board = Board()
            self.board.set_pieces()
        self.play_game()
        self.print_result()

