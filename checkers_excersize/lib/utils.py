import csv
from typing import List, Tuple


def convert_checker_pos_to_2dmatrix_pos(pos: int) -> int:
    """
    we are operationg on 2*2 matrix
    hoverwer the moves are given in different notations
    so we must convert them
    ex 0,0 -> 7,7
    3,4 -> 3,4
    3,6 -> 1,4
    :param pos:  pos to convert
    :return:
    """
    converted_source_x = 7 - int(pos)
    return converted_source_x


def convert_move_entry_to_2d_matrix(entry: List[str]) -> List[int]:
    """
    convert entire list of moves to 2d matrix moves
    :param entry:
    :return:
    """
    if len(entry) != 4:
        raise ValueError(f"must be 4 numbers in list {entry}")

    result_map = map(convert_checker_pos_to_2dmatrix_pos, entry)
    result = list(result_map)
    result[0], result[1] = result[1], result[0]
    result[2], result[3] = result[3], result[2]
    return result


def file_to_list(file_path):
    """
    read file to list of lists
    :param file_path:
    :return:
    """
    file = open(file_path, "r")
    csv_reader = csv.reader(file)
    lists_from_csv = []
    for row in csv_reader:
        lists_from_csv.append(row)
    return lists_from_csv


def compare_lists(l1: List[List], l2: List[List]) -> set:
    """
    get difference between 2 lists of lists
    """
    z: List[Tuple] = [tuple(y) for y in l1]
    x: List[Tuple] = [tuple(y) for y in l2]
    diff = set(x) - set(z)
    diff_reverse = set(z) - set(x)
    union = set.union(diff, diff_reverse)
    return union


def check_for_list_in_list_of_lists(l1: List, list_of_lists: List[List]):
    """
    check if list of lists contains list
    :param l1:
    :param list_of_lists:
    :return:
    """
    for l in list_of_lists:
        if not compare_lists(l, l1):
            return True
    return False


def see_board_snapshot(board: List[List]):
    """
    print 2d matrix
    :param board:
    :return:
    """
    for row in board:
        print(*row)
    return True
