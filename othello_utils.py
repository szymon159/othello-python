from enum import Enum, auto

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