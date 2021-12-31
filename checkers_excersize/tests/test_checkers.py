import unittest

import lib.utils as ut
import tests.repo_for_tests as rp
from lib.board import Board
from lib.checkers_constants import WHITE, BLACK, WHITE_WIN, BLACK_WIN, TIE, \
    INCOMPLETE_GAME, ILLIEGAL_MOVE
from lib.game import Game
from lib.move import Move
from tests.first_test import WHITE_FULL_GAME
from tests.illiegal_game_move import ILLIEGAL_MOVE_GAME
from tests.incomplete_game import INCOMPLETE_GAME_MOVES
from tests.second_test import BLACK_FULL_GAME


class TestCheckers(unittest.TestCase):
    def test_correct_move_white(self):
        moves = [[4, 4, 5, 5]]
        board = Board()
        board.board = rp.WHITE_SINGLE_BOARD
        game = Game(moves=moves, board=board)
        game.play_game()
        comparation_result = ut.compare_lists(game.board.board, rp.TEST_SIMPLE_CORRECT_MOVE_END_WHITE)
        assert not comparation_result

    def test_missing_piece_white(self):
        move = [1, 2, 3, 4]
        board = Board()
        board.board = rp.WHITE_SINGLE_BOARD
        move = Move(color=WHITE,
                    source_x=move[0],
                    source_y=move[1],
                    target_x=move[2],
                    target_y=move[3],
                    board=board
                    )
        assert not move.legal_move()

    def test_incorrect_order_turn_white(self):
        move = [3, 3, 4, 4]
        board = Board()
        board.board = rp.WHITE_SINGLE_BOARD
        move = Move(color=WHITE,
                    source_x=move[0],
                    source_y=move[1],
                    target_x=move[2],
                    target_y=move[3],
                    board=board
                    )
        assert not move.legal_move()

    def test_incorrect_move_because_taget_is_taken(self):
        move = [3, 3, 2, 4]
        board = Board()
        board.board = rp.TEST_PLACE_TAKEN
        move = Move(color=WHITE,
                    source_x=move[0],
                    source_y=move[1],
                    target_x=move[2],
                    target_y=move[3],
                    board=board
                    )
        assert not move.legal_move()

    def test_correct_jump_white_up_right(self):
        move = [3, 3, 1, 5]
        board = Board()
        board.board = rp.TEST_CORRECT_JUMP_WHITE_UP_RIGHT_START
        move = Move(color=WHITE,
                    source_x=move[0],
                    source_y=move[1],
                    target_x=move[2],
                    target_y=move[3],
                    board=board
                    )
        assert move.legal_move()
        move.make_move()
        comparation_result = ut.compare_lists(move.board.board, rp.TEST_CORRECT_JUMP_WHITE_UP_RIGHT_END)
        assert not comparation_result

    def test_incorrect_jump_white_up_right_no_jump_piece(self):
        move = [3, 3, 1, 5]
        board = Board()
        board.board = rp.WHITE_SINGLE_BOARD
        move = Move(color=WHITE,
                    source_x=move[0],
                    source_y=move[1],
                    target_x=move[2],
                    target_y=move[3],
                    board=board
                    )
        assert not move.legal_move()

    def test_correct_jump_white_up_left(self):
        move = [3, 3, 1, 1]
        board = Board()
        board.board = rp.TEST_CORRECT_JUMP_WHITE_UP_LEFT_START
        move = Move(color=WHITE,
                    source_x=move[0],
                    source_y=move[1],
                    target_x=move[2],
                    target_y=move[3],
                    board=board
                    )
        assert move.legal_move()
        move.make_move()
        comparation_result = ut.compare_lists(move.board.board, rp.TEST_CORRECT_JUMP_WHITE_UP_LEFT_END)
        assert not comparation_result

    def test_correct_jump_white_down_left(self):
        move = [3, 3, 5, 1]
        board = Board()
        board.board = rp.TEST_CORRECT_JUMP_DOWN_LEFT_START
        move = Move(color=WHITE,
                    source_x=move[0],
                    source_y=move[1],
                    target_x=move[2],
                    target_y=move[3],
                    board=board
                    )
        assert not move.legal_move()

    def test_correct_jump_black_down_left(self):
        move = [3, 3, 5, 1]
        board = Board()
        board.board = rp.TEST_CORRECT_JUMP_DOWN_LEFT_START_BLACK
        move = Move(color=BLACK,
                    source_x=move[0],
                    source_y=move[1],
                    target_x=move[2],
                    target_y=move[3],
                    board=board
                    )
        assert move.legal_move()
        move.make_move()
        comparation_result = ut.compare_lists(move.board.board, rp.TEST_CORRECT_JUMP_DOWN_LEFT_END_BLACK)
        assert not comparation_result

    def test_correct_jump_white_down_right(self):
        move = [3, 3, 5, 6]
        board = Board()
        board.board = rp.TEST_CORRECT_JUMP_DOWN_RIGHT_START
        move = Move(color=WHITE,
                    source_x=move[0],
                    source_y=move[1],
                    target_x=move[2],
                    target_y=move[3],
                    board=board
                    )
        assert not move.legal_move()
        move.make_move()
        comparation_result = ut.compare_lists(move.board.board, rp.TEST_CORRECT_JUMP_DOWN_RIGHT_END)
        assert not comparation_result

    def test_must_jump_spots_white(self):
        move = [3, 3, 5, 6]
        board = Board()
        board.board = rp.TEST_FIND_MUST_JUMP_WHITE
        move = Move(color=WHITE,
                    source_x=move[0],
                    source_y=move[1],
                    target_x=move[2],
                    target_y=move[3],
                    board=board
                    )
        jump_locations = move.check_for_must_jump()
        expected_result = [[3, 6, 1, 4], [5, 3, 3, 1], [5, 7, 3, 5]]
        comparation_result = ut.compare_lists(jump_locations, expected_result)
        assert not comparation_result

    def test_must_jump_spots_black(self):
        move = [3, 3, 5, 6]
        board = Board()
        board.board = rp.TEST_FIND_MUST_JUMP_BLACK
        move = Move(color=BLACK,
                    source_x=move[0],
                    source_y=move[1],
                    target_x=move[2],
                    target_y=move[3],
                    board=board
                    )
        jump_locations = move.check_for_must_jump()
        expected_result = [[0, 1, 2, 3], [2, 5, 4, 7], [3, 3, 5, 5]]
        comparation_result = ut.compare_lists(jump_locations, expected_result)
        assert not comparation_result

    def test_find_correct_move_locations_white(self):
        move = [3, 3, 5, 6]
        board = Board()
        board.board = rp.TEST_CORRECT_MOVE_LOCATIONS_WHITE
        move = Move(color=WHITE,
                    source_x=move[0],
                    source_y=move[1],
                    target_x=move[2],
                    target_y=move[3],
                    board=board
                    )
        locations = move.get_correct_move_locations()
        expected_result = [[1, 7, 0, 6], [2, 0, 1, 1], [6, 1, 5, 2], [6, 1, 5, 0], [7, 2, 6, 3], [6, 4, 5, 3]]
        comparation_result = ut.compare_lists(locations, expected_result)
        assert not comparation_result

    def test_find_correct_move_locations_black(self):
        move = [3, 3, 5, 6]
        board = Board()
        board.board = rp.TEST_CORRECT_MOVE_LOCATIONS_BLACK
        move = Move(color=BLACK,
                    source_x=move[0],
                    source_y=move[1],
                    target_x=move[2],
                    target_y=move[3],
                    board=board
                    )
        locations = move.get_correct_move_locations()
        expected_result = [[0, 0, 1, 1], [3, 4, 4, 5], [3, 4, 4, 3], [6, 7, 7, 6]]
        comparation_result = ut.compare_lists(locations, expected_result)
        assert not comparation_result

    def test_whites_win(self):
        game = Game(moves=WHITE_FULL_GAME)
        game.board = Board()
        game.board.set_pieces()
        game.play_game()
        assert game.game_status == WHITE_WIN

    def test_black_win(self):
        game = Game(moves=BLACK_FULL_GAME)
        game.board = Board()
        game.board.set_pieces()
        game.play_game()
        assert game.game_status == BLACK_WIN

    def test_tie(self):
        moves = [[1, 6, 0, 7]]
        board = Board()
        board.board = rp.TEST_TIE
        game = Game(moves=moves, board=board)
        game.play_game()
        assert game.game_status == TIE

    def test_incomplete_game(self):
        moves = INCOMPLETE_GAME_MOVES
        game = Game(moves=moves)
        game.start_game()
        assert game.game_status == INCOMPLETE_GAME

    def test_illiegal_move(self):
        moves = ILLIEGAL_MOVE_GAME
        game = Game(moves=moves)
        game.start_game()
        assert game.game_status == ILLIEGAL_MOVE


if __name__ == '__main__':
    unittest.main()
