import math
import pygame

from othello_utils import Direction

class OthelloGame:
    __WIDTH, __HEIGHT = 800, 600
    __BG_COLOR = (0,100,0)
    __ROWS = 8
    __COLS = 8

    def __init__(self) -> None:
        pygame.init()
        self._font = pygame.font.SysFont('comicsans', 30)
        self.__points_black = self.__points_white = 0
        self.__init_board()
        self.__current_player = -1 # -1 for black, 1 for white
        self.__window = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))
        self.__accept_input = True # TODO: Parametrize it - set to true only if PvP or PvE with player's turn
        pygame.display.set_caption("Othello")

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONUP and self.__accept_input:
                    pass

            self.draw()

    def draw(self) -> None:
        self.__window.fill(self.__BG_COLOR)
        self.__draw_board()
        self.__draw_results()
        pygame.display.update()

    def try_move(self, x, y) -> bool:
        if self.evaluate_move(x, y) < 0:
            return False
        self.__move(x, y, self.__current_player)
        return True

    def evaluate_move(self, x, y, player = None) -> int:
        if self.__board[x][y] != 0:
            return -1
        if player is None:
            player = self.__current_player

        value = 0
        for direction in Direction:
            val = self.__evaluate_capture(x, y, direction, player)
            if val > 0:
                value += val
        return value if value > 0 else -1

    def __init_board(self) -> None:
        self.__board = [[0 for i in range(self.__ROWS)] for _ in range (self.__COLS)]
        x, y = self.__ROWS // 2, self.__COLS // 2
        self.__board[x - 1][y - 1] = self.__board[x][y] = 1
        self.__board[x - 1][y] = self.__board[x][y - 1] = -1
        self.__update_result()

    def __draw_board(self) -> None:
        size = self.__HEIGHT / self.__ROWS
        radius = math.ceil((size - 10) / 2)

        x = self.__WIDTH - self.__HEIGHT
        y = 0
        pygame.draw.line(self.__window, 'black', (x, 0), (x, self.__HEIGHT), 4)
        x += size
        for _ in enumerate(self.__board):
            pygame.draw.line(self.__window, 'black', (x, 0), (x, self.__HEIGHT), 2)
            x += size
        for _ in enumerate(self.__board[0]):
            pygame.draw.line(self.__window, 'black', (self.__WIDTH - self.__HEIGHT, y), (self.__WIDTH, y), 2)
            y += size

        x = self.__WIDTH - self.__HEIGHT
        for _, col in enumerate(self.__board):
            y = 0
            for _, value in enumerate(col):
                if value == 0:
                    y += size
                    continue
                color = 'black' if value == -1 else 'white'
                pygame.draw.circle(self.__window, color, (x + radius + 5, y + radius + 5), radius)
                y += size
            x += size

    def __draw_results(self) -> None:
        self.__window.blit(self._font.render(f'White: {self.__points_white}', 1, 'white'), (10, self.__HEIGHT // 2 - 45))
        self.__window.blit(self._font.render(f'Black: {self.__points_black}', 1, 'black'), (10, self.__HEIGHT // 2))

    def __evaluate_capture(self, x, y, direction, player) -> int:
        value = 0
        if direction == Direction.NORTH:
            if y == 0:
                return -1
            for i in range(0, y - 1):
                if self.__board[x][i] == 0:
                    return -1
                if self.__board[x][i] == -player:
                    value += 1
                else:
                    return value
        # TODO: All other directions
        return -1

    def __move(self, x, y, player) -> None:
        self.__board[x][y] = player
        self.__update_result()

    def __update_result(self):
        self.__points_black = self.__points_white = 0
        for _, col in enumerate(self.__board):
            for _, value in enumerate(col):
                if value == -1:
                    self.__points_black += 1
                elif value == 1:
                    self.__points_white += 1
