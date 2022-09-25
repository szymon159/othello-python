from typing import Generator
from othello_utils import Direction, PlayerColor, rotated

class Board:
    '''
    Class responsible for storing information about board and result
    This class also handles simple logic such as checking legal actions
    '''
    ROWS, COLS = 8, 8

    def __init__(self) -> None:
        self.__field = [[]]
        self.__init_board()

    def evaluate_move(self, col: int, row: int, color: PlayerColor) -> int:
        '''
        Returns number of pawns captured by placing pawn of specific color in specified row and col of the board
        If the move is illegal, returns -1
        '''
        value = len(self.get_captures(col, row, color))
        return value if value > 0 else -1

    def get_captures(self, col: int, row: int, color: PlayerColor) -> list[tuple[int, int]]:
        '''
        Returns list of (row, col)-coordinates for all pawns that will be captured by placing pawn of specific color in specified row and col of the board
        '''
        if self.__field[col][row] != 0:
            return []
        captures = []
        for direction in Direction:
            captures.extend(self.__get_captures_in_direction(col, row, direction, color))
        return captures

    def get_legal_actions(self, player_color: PlayerColor) -> list[tuple[int, int]]:
        '''
        Returns list of (row, col)-coordinates for all fields where pawn of specified color can be legally placed
        '''
        moves = []
        for i in range(self.COLS):
            for j in range(self.ROWS):
                if self.evaluate_move(i, j, player_color) > 0:
                    moves.append((i,j))
        return moves

    def refresh_result(self) -> None:
        '''
        Refreshes result stored in points array, counting pawns placed on the board
        '''
        self.points[PlayerColor.BLACK] = self.points[PlayerColor.WHITE] = 0
        for i in range(self.COLS):
            for j in range(self.ROWS):
                if self.__field[i][j] != 0:
                    self.points[PlayerColor(self.__field[i][j])] += 1

    def can_move(self, color: PlayerColor) -> bool:
        '''
        Returns boolean value indicating if there is any legal move for player with specified color
        '''
        if self.points[PlayerColor.BLACK] + self.points[PlayerColor.WHITE] == 64:
            return False

        for col in range(self.COLS):
            for row in range(self.ROWS):
                if self.__field[col][row] == 0 and self.evaluate_move(col, row, color) > 0:
                    return True
        return False

    def move(self, col: int, row: int, color: PlayerColor) -> bool:
        '''
        If legal, update board fields with results of placing a pawn of specific color in specified row and col of the board.
        Returns true if move was possible or false if it was illegal.
        Result is not updated by this method. It has to be done manually by calling refresh_result method.
        '''
        if self.evaluate_move(col, row, color) < 0:
            return False
        for capture in self.get_captures(col, row, color):
            self.__field[capture[0]][capture[1]] = color.value
        self.__field[col][row] = color.value
        return True

    def get_field(self) -> list[list[int]]:
        '''
        Returns color values of pawns placed on all fields on the board.
        '''
        return self.__field

    def rotate_board(self) -> None:
        '''
        Overwrites current board by rotating it
        '''
        self.__field = rotated(self.__field)

    def get_leader(self) -> PlayerColor:
        '''
        Return leader's color
        '''
        if self.points[PlayerColor.BLACK] == self.points[PlayerColor.WHITE]:
            return None
        if self.points[PlayerColor.BLACK] > self.points[PlayerColor.WHITE]:
            return PlayerColor.BLACK
        return PlayerColor.WHITE

    def __init_board(self) -> None:
        self.__field = [[0 for _ in range(self.ROWS)] for _ in range (self.COLS)]
        center_row, center_col = self.ROWS // 2, self.COLS // 2
        self.__field[center_col - 1][center_row - 1] = self.__field[center_col][center_row] = 1
        self.__field[center_col - 1][center_row] = self.__field[center_col][center_row - 1] = -1
        self.points = { PlayerColor.BLACK: 2, PlayerColor.WHITE: 2}

    def __get_captures_in_direction(self, col: int, row: int, direction: Direction, player: PlayerColor) -> tuple[int, int]:
        captures = []
        for field_cords in self.__get_fields_in_direction(col, row, direction):
            field = self.__field[field_cords[0]][field_cords[1]]
            if field == 0:
                return []
            if field == player.value:
                return captures
            captures.append(field_cords)
        return []

    def __get_fields_in_direction(self, start_col: int, start_row: int, direction: Direction) -> Generator[tuple[int, int], None, None]:
        if direction == Direction.NORTH:
            for i in range(start_row - 1, -1, -1):
                yield (start_col, i)
        elif direction == Direction.EAST:
            for i in range(start_col + 1, self.COLS):
                yield (i, start_row)
        elif direction == Direction.SOUTH:
            for i in range(start_row + 1, self.ROWS):
                yield (start_col, i)
        elif direction == Direction.WEST:
            for i in range(start_col -1, -1, -1):
                yield (i, start_row)
        elif direction == Direction.NORTH_EAST:
            counter = min(self.COLS - start_col, start_row + 1)
            for i in range(1, counter):
                yield (start_col + i, start_row - i)
        elif direction == Direction.SOUTH_EAST:
            counter = min(self.COLS - start_col, self.ROWS - start_row)
            for i in range(1, counter):
                yield (start_col + i, start_row + i)
        elif direction == Direction.SOUTH_WEST:
            counter = min(start_col + 1, self.ROWS - start_row)
            for i in range(1, counter):
                yield (start_col - i, start_row + i)
        elif direction == Direction.NORTH_WEST:
            counter = min(start_col + 1, start_row + 1)
            for i in range(1, counter):
                yield (start_col - i, start_row - i)

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.__field[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        self.__field[key[0]][key[1]] = value
        self.refresh_result()

    def __delitem__(self, key: tuple[int, int]) -> None:
        self.__field[key[0]][key[1]] = 0
