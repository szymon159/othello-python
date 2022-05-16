import math
import pygame
from board import Board

class OthelloGame:
    def __init__(self) -> None:
        self.__points_black = self.__points_white = 0
        self.__current_player = -1 # -1 for black, 1 for white
        self.__accept_input = True # TODO: Parametrize it - set to true only if PvP or PvE with player's turn
        self.__board = Board()
        pygame.init()
        pygame.display.set_caption("Othello")
        self.__font = pygame.font.SysFont('comicsans', 30)
        self.__window = pygame.display.set_mode((self.__board.WIDTH, self.__board.HEIGHT))

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONUP and self.__accept_input:
                    pass
            self.draw()

    def draw(self) -> None:
        self.__window.fill(self.__board.BG_COLOR)
        self.__draw_board()
        self.__draw_results()
        pygame.display.update()

    # def try_move(self, x, y) -> bool:
    #     if self.__board.evaluate_move(x, y, self.__current_player) < 0:
    #         return False
    #     self.__move(x, y, self.__current_player)
    #     return True

    def __draw_board(self) -> None:
        size = self.__board.HEIGHT / self.__board.ROWS
        radius = math.ceil((size - 10) / 2)
        left, right = self.__board.WIDTH - self.__board.HEIGHT, self.__board.WIDTH
        top, bottom = 0, self.__board.HEIGHT
        pygame.draw.line(self.__window, 'black', (left, top), (left, bottom), 4)
        for i in range(self.__board.COLS):
            field_x = left + i * size
            pygame.draw.line(self.__window, 'black', (field_x, top), (field_x, bottom), 2)
        for i in range(self.__board.ROWS):
            field_y = top + i * size
            pygame.draw.line(self.__window, 'black', (left, field_y), (right, field_y))
        for i in range(self.__board.COLS):
            field_x = left + i * size
            for j in range(self.__board.ROWS):
                value = self.__board[i, j]
                if value == 0:
                    continue
                field_y = j * size
                color = 'black' if value == -1 else 'white'
                pygame.draw.circle(self.__window, color, (field_x + radius + 5, field_y + radius + 5), radius)

    def __draw_results(self) -> None:
        self.__update_result()
        self.__window.blit(self.__font.render(f'White: {self.__points_white}', 1, 'white'), (10, self.__board.HEIGHT // 2 - 45))
        self.__window.blit(self.__font.render(f'Black: {self.__points_black}', 1, 'black'), (10, self.__board.HEIGHT // 2))

    def __move(self, row, col, player) -> None:
        self.__board[row, col] = player

    def __update_result(self):
        self.__points_black = self.__points_white = 0
        for i in range(self.__board.COLS):
            for j in range(self.__board.ROWS):
                if self.__board[i,j] == -1:
                    self.__points_black += 1
                elif self.__board[i,j] == 1:
                    self.__points_white += 1
