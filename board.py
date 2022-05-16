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

    def __init_board(self) -> None:
        self.__field = [[0 for i in range(self.ROWS)] for _ in range (self.COLS)]
        center_row, center_col = self.ROWS // 2, self.COLS // 2
        self.__field[center_row - 1][center_col - 1] = self.__field[center_row][center_col] = 1
        self.__field[center_row - 1][center_col] = self.__field[center_row][center_col - 1] = -1

    def __evaluate_capture(self, row: int, col: int, direction: Direction, player: PlayerColor) -> int:
        value = 0
        if direction == Direction.NORTH:
            if col == 0:
                return -1
            for i in range(0, col - 1):
                if self.__field[row][i] == 0:
                    return -1
                if self.__field[row][i] == -player:
                    value += 1
                else:
                    return value
        # TODO: All other directions
        return -1

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.__field[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        self.__field[key[0]][key[1]] = value

    def __delitem__(self, key: tuple[int, int]) -> None:
        self.__field[key[0]][key[1]] = 0
