import math
import threading
import pygame
from board import Board
from othello_utils import PlayerColor
from player import Player, UserPlayer

class OthelloGame:
    __FPS = 60
    __WIDTH, __HEIGHT = 800, 600
    __BG_COLOR = (0,100,0)

    def __init__(self, players: list[Player]) -> None:
        self.__players = {player.color.value: player for player in players}
        self.__current_player = self.__players[PlayerColor.BLACK.value]
        self.__is_move_in_progress = False
        self.__board = Board()
        self.__field_size = self.__HEIGHT / self.__board.ROWS
        pygame.init()
        pygame.display.set_caption("Othello")
        self.__font = pygame.font.SysFont('comicsans', 30)
        self.__window = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))

    def run_game(self) -> None:
        fps_clock = pygame.time.Clock()
        while True:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__is_move_in_progress = False # This will help stopping background worker if still running
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and isinstance(self.__current_player, UserPlayer) and self.__is_move_in_progress:
                    self.__get_user_move(pygame.mouse.get_pos())
            # Get next move from AI
            if not self.__is_move_in_progress:
                self.__get_next_move()
            # Draw
            self.draw()
            fps_clock.tick(self.__FPS)

    def draw(self) -> None:
        self.__window.fill(self.__BG_COLOR)
        self.__draw_board()
        self.__draw_results()
        self.__draw_moves_evaluation()
        pygame.display.update()

    def __draw_board(self) -> None:
        radius = math.ceil((self.__field_size - 10) / 2)
        left, right = self.__WIDTH - self.__HEIGHT, self.__WIDTH
        top, bottom = 0, self.__HEIGHT
        pygame.draw.line(self.__window, 'black', (left, top), (left, bottom), 4)
        for i in range(self.__board.COLS):
            field_x = left + i * self.__field_size
            pygame.draw.line(self.__window, 'black', (field_x, top), (field_x, bottom), 2)
        for i in range(self.__board.ROWS):
            field_y = top + i * self.__field_size
            pygame.draw.line(self.__window, 'black', (left, field_y), (right, field_y))
        for i in range(self.__board.COLS):
            field_x = left + i * self.__field_size
            for j in range(self.__board.ROWS):
                value = self.__board[i, j]
                if value == 0:
                    continue
                field_y = j * self.__field_size
                pygame.draw.circle(self.__window, PlayerColor(value).name, (field_x + radius + 5, field_y + radius + 5), radius)

    def __draw_results(self) -> None:
        self.__board.refresh_result()
        self.__window.blits([
            (self.__font.render(f'White: {self.__board.points[PlayerColor.WHITE]}', 1, 'white'), (10, self.__HEIGHT // 2 - 45)),
            (self.__font.render(f'Black: {self.__board.points[PlayerColor.BLACK]}', 1, 'black'), (10, self.__HEIGHT // 2))
        ])

    def __draw_moves_evaluation(self) -> None:
        left = self.__WIDTH - self.__HEIGHT

        for i in range(self.__board.COLS):
            field_x = left + i * self.__field_size
            for j in range(self.__board.ROWS):
                field_y = j * self.__field_size
                val = self.__board.evaluate_move(i, j, PlayerColor.BLACK)
                if val > -1:
                    self.__window.blit(self.__font.render(f'{val}', 1, 'black'), (field_x + 30, field_y + 15))
                val = self.__board.evaluate_move(i, j, PlayerColor.WHITE)
                if val > -1:
                    self.__window.blit(self.__font.render(f'{val}', 1, 'white'), (field_x + 30, field_y + 15))

    def __get_next_move(self) -> None:
        self.__is_move_in_progress = True
        if isinstance(self.__current_player, UserPlayer):
            return
        thread = threading.Thread(target=self.__get_bot_move)
        thread.start()

    def __get_bot_move(self) -> None:
        while self.__is_move_in_progress:
            col, row = self.__current_player.get_next_move(self.__board)
            if self.__board.evaluate_move(col, row, self.__current_player.color) > 0:
                self.__move(col, row)

    def __get_user_move(self, mouse_pos: tuple[int, int]) -> None:
        pass

    def __move(self, col: int, row: int) -> None:
        for capture in self.__board.get_captures(col, row, self.__current_player.color):
            self.__board[capture[0], capture[1]] = self.__current_player.color.value
        self.__board[col, row] = self.__current_player.color.value
        self.__current_player = self.__players[-self.__current_player.color.value]
        self.__is_move_in_progress = False
