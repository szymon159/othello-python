import math
import pygame
from board import Board
from othello_utils import PlayerColor

class OthelloGame:
    __FPS = 60
    __WIDTH, __HEIGHT = 800, 600
    __BG_COLOR = (0,100,0)

    def __init__(self) -> None:
        # self.__current_player = PlayerColor.BLACK
        self.__board = Board()
        pygame.init()
        pygame.display.set_caption("Othello")
        self.__font = pygame.font.SysFont('comicsans', 30)
        self.__window = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))

    def run_game(self) -> None:
        fps_clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                # if event.type == pygame.MOUSEBUTTONUP and self.__accept_input:
                #     pass

            self.draw()
            fps_clock.tick(self.__FPS)

    def draw(self) -> None:
        self.__window.fill(self.__BG_COLOR)
        self.__draw_board()
        self.__draw_results()
        self.__draw_moves_evaluation()
        pygame.display.update()

    # def try_move(self, x, y) -> bool:
    #     if self.__board.evaluate_move(x, y, self.__current_player) < 0:
    #         return False
    #     self.__move(x, y, self.__current_player)
    #     return True

    def __draw_board(self) -> None:
        size = self.__HEIGHT / self.__board.ROWS
        radius = math.ceil((size - 10) / 2)
        left, right = self.__WIDTH - self.__HEIGHT, self.__WIDTH
        top, bottom = 0, self.__HEIGHT
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
                pygame.draw.circle(self.__window, PlayerColor(value).name, (field_x + radius + 5, field_y + radius + 5), radius)

    def __draw_results(self) -> None:
        self.__board.refresh_result()
        self.__window.blits([
            (self.__font.render(f'White: {self.__board.points[PlayerColor.WHITE]}', 1, 'white'), (10, self.__HEIGHT // 2 - 45)),
            (self.__font.render(f'Black: {self.__board.points[PlayerColor.BLACK]}', 1, 'black'), (10, self.__HEIGHT // 2))
        ])


    def __draw_moves_evaluation(self) -> None:
        left = self.__WIDTH - self.__HEIGHT
        size = self.__HEIGHT / self.__board.ROWS

        for i in range(self.__board.COLS):
            field_x = left + i * size
            for j in range(self.__board.ROWS):
                field_y = j * size
                val = self.__board.evaluate_move(i, j, PlayerColor.BLACK)
                if val > -1:
                    self.__window.blit(self.__font.render(f'{val}', 1, 'black'), (field_x + 30, field_y + 15))
                val = self.__board.evaluate_move(i, j, PlayerColor.WHITE)
                if val > -1:
                    self.__window.blit(self.__font.render(f'{val}', 1, 'white'), (field_x + 30, field_y + 15))


    # def __move(self, row: int, col: int, player: PlayerColor) -> None:
    #     self.__board[row, col] = player
