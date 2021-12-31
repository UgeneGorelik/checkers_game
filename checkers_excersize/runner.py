import argparse

from lib.game import Game
from lib.utils import file_to_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input moves file', required=True)
    args = parser.parse_args()
    commands_list = file_to_list(args.input)
    g = Game(commands_list)
    g.start_game()
