from typing import Dict, List

from lib.checkers_constants import WHITE, BLACK

INIT_ROWS: int = 8
INIT_COLS: int = 8
COLOR_NUM_DICT: Dict[str, int] = {
    WHITE: 1,
    BLACK: -1
}

INIT_BOARD: List[List] = [[0, -1, 0, -1, 0, -1, 0, -1],
                          [-1, 0, -1, 0, -1, 0, -1, 0],
                          [0, -1, 0, -1, 0, -1, 0, -1],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [1, 0, 1, 0, 1, 0, 1, 0],
                          [0, 1, 0, 1, 0, 1, 0, 1],
                          [1, 0, 1, 0, 1, 0, 1, 0]
                          ]
