from typing import Generator
from othello_utils import Direction, PlayerColor

class Board:
    BG_COLOR = (0,100,0)
    WIDTH, HEIGHT = 800, 600
    ROWS, COLS = 8, 8

    def __init__(self) -> None:
        self.__init_board()

    def evaluate_move(self, row: int, col: int, color: PlayerColor) -> int:
        if self.__field[row][col] != 0:
            return -1
        value = 0
        for direction in Direction:
            val = self.__evaluate_capture(row, col, direction, color)
            if val > 0:
                value += val
        return value if value > 0 else -1

    def refresh_result(self):
        self.points[PlayerColor.BLACK] = self.points[PlayerColor.WHITE] = 0
        for i in range(self.COLS):
            for j in range(self.ROWS):
                if self.__field[i][j] != 0:
                    self.points[PlayerColor(self.__field[i][j])] += 1

    def __init_board(self) -> None:
        self.__field = [[0 for _ in range(self.ROWS)] for _ in range (self.COLS)]
        center_row, center_col = self.ROWS // 2, self.COLS // 2
        self.__field[center_row - 1][center_col - 1] = self.__field[center_row][center_col] = 1
        self.__field[center_row - 1][center_col] = self.__field[center_row][center_col - 1] = -1
        self.points = { PlayerColor.BLACK: 2, PlayerColor.WHITE: 2}

    def __evaluate_capture(self, row: int, col: int, direction: Direction, player: PlayerColor) -> int:
        value = 0
        for field in self.__get_fields_in_direction(row, col, direction):
            if field == 0:
                return -1
            if field == player:
                return value
            value += 1
        return -1

    def __get_fields_in_direction(self, start_row: int, start_col: int, direction: Direction) -> Generator[int, None, None]:
        if direction == Direction.NORTH:
            for i in range(0, start_row):
                yield self.__field[i][start_col]
        elif direction == Direction.EAST:
            for i in range(start_col + 1, self.COLS):
                yield self.__field[start_row][i]
        elif direction == Direction.SOUTH:
            for i in range(start_row + 1, self.ROWS):
                yield self.__field[i][start_col]
        elif direction == Direction.WEST:
            for i in range(0, start_col):
                yield self.__field[start_row][i]
        elif direction == Direction.NORTH_EAST:
            counter = min(start_row + 1, self.COLS - start_col)
            for i in range(1, counter):
                yield self.__field[start_row - i, start_col + i]
        elif direction == Direction.SOUTH_EAST:
            counter = min(self.ROWS - start_row, self.COLS - start_col)
            for i in range(1, counter):
                yield self.__field[start_row + i, start_col + i]
        elif direction == Direction.SOUTH_WEST:
            counter = min(self.ROWS - start_row, start_col + 1)
            for i in range(1, counter):
                yield self.__field[start_row + i][start_col - i]
        elif direction == Direction.NORTH_WEST:
            counter = min(start_row + 1, start_col + 1)
            for i in range(1, counter):
                yield self.__field[start_row - i][start_col - i]

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.__field[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        self.__field[key[0]][key[1]] = value
        self.refresh_result()

    def __delitem__(self, key: tuple[int, int]) -> None:
        self.__field[key[0]][key[1]] = 0
