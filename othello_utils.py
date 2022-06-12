from enum import Enum, auto

HEURISTIC_WEIGHTS = [[120, -20,  20,  5,  5,  20, -20, 120],
                    [-20, -40,  -5, -5, -5,  -5, -30, -20],
                    [ 20,  -5,  15,  3,  3,  15,  -5,  20],
                    [  5,  -5,   3,  3,  3,   3,  -5,   5],
                    [  5,  -5,   3,  3,  3,   3,  -5,   5],
                    [ 20,  -5,  15,  3,  3,  15,  -5,  20],
                    [-20, -40,  -5, -5, -5,  -5, -30, -20],
                    [120, -20,  20,  5,  5,  20, -20, 120]]

class Direction(Enum):
    NORTH = auto()
    NORTH_EAST = auto()
    EAST = auto()
    SOUTH_EAST = auto()
    SOUTH = auto()
    SOUTH_WEST = auto()
    WEST = auto()
    NORTH_WEST = auto()

class PlayerColor(Enum):
    BLACK = -1
    WHITE = 1

class MCTSVersion(Enum):
    UCT = auto()
    UCB1_TUNED = auto()
    UCT_GROUPING = auto()

def rotated(array_2d):
    list_of_tuples = zip(*array_2d[::-1])
    return [list(elem) for elem in list_of_tuples]


def check_if_in_dictionary(state, dict):
    if state.to_string() in dict:
        return True
    elif state.rotate_board().to_string() in dict:
        return True
    elif state.rotate_board().to_string() in dict:
        return True
    elif state.rotate_board().to_string() in dict:
        return True

    return False
