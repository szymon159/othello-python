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
