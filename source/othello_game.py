import copy
import math
import threading
from timeit import default_timer as timer
import pygame
from board import Board
from othello_utils import PlayerColor
from player import Player, UserPlayer

class OthelloGame:
    '''
    Class representing game logic including render, input and output.
    '''
    __FPS = 60
    __WIDTH, __HEIGHT = 800, 600
    __BG_COLOR = (0,100,0)

    def __init__(self, players: list[Player], open_visualization: bool = True, print_game_events: bool = False) -> None:
        self.__players = {player.color.value: player for player in players}
        self.__current_player = self.__players[PlayerColor.BLACK.value]
        self.__is_move_in_progress = False
        self.__is_game_in_progress = False
        self.__board = Board()
        self.__field_size = self.__HEIGHT / self.__board.ROWS
        self.__is_board_displayed = open_visualization or any(isinstance(player, UserPlayer) for player in players)
        self.__print_game_events = print_game_events
        self.__move_times = {player.color: 0 for player in players}
        self.__time_start = 0
        if self.__is_board_displayed:
            # Line below is required to ignore pylint's fake-error from pygame module
            # pylint: disable=maybe-no-member
            pygame.init()
            pygame.display.set_caption("Othello")
            self.__font = pygame.font.SysFont('comicsans', 30)
            self.__window = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))

    def run_game(self) -> None:
        '''
        Runs main loop of the game
        '''
        self.__is_game_in_progress = True
        fps_clock = pygame.time.Clock()
        while True:
            # Process events, but only if board is displayed
            if self.__is_board_displayed:
                for event in pygame.event.get():\
                    # Line below is required to ignore pylint's fake-error from pygame module
                    # pylint: disable=maybe-no-member
                    if event.type == pygame.QUIT:
                        self.__is_move_in_progress = False # This will help stopping background worker if still running
                        return False
                    # Line below is required to ignore pylint's fake-error from pygame module
                    # pylint: disable=maybe-no-member
                    if event.type == pygame.MOUSEBUTTONDOWN and isinstance(self.__current_player, UserPlayer) and self.__is_move_in_progress:
                        self.__get_user_move(pygame.mouse.get_pos())
            # Check if game is finished and no move is pending
            if not self.__is_move_in_progress and not self.__is_any_move_possible():
                self.__is_game_in_progress = False
                self.__is_move_in_progress = False
                if self.__print_game_events:
                    self.__print_final_result()
                if not self.__is_board_displayed:
                    return False
            # Wait for next move, but only if game is not finished and no move is pending
            if self.__is_game_in_progress and not self.__is_move_in_progress:
                self.__get_next_move()
            # Draw, but only if board is displayed
            if self.__is_board_displayed:
                self.__draw()
            fps_clock.tick(self.__FPS)

    def get_result(self) -> dict[PlayerColor, int]:
        '''
        Returns points scored by each player
        '''
        return self.__board.points

    def get_times(self) -> dict[PlayerColor, int]:
        '''
        Returns accumulated move times for each player
        '''
        return self.__move_times

    def __is_any_move_possible(self) -> bool:
        return any(self.__board.can_move(player.color) for player in self.__players.values())

    def __draw(self) -> None:
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
        header = f'{self.__current_player.color.name.capitalize()}\'s turn' if self.__is_game_in_progress else 'Game over'
        self.__window.blits([
            (self.__font.render(header, 1, self.__current_player.color.name), (10, self.__HEIGHT // 2 - 100)),
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
        if not self.__is_move_in_progress or not self.__is_game_in_progress:
            return
        if self.__print_game_events:
            print(f'It is {self.__current_player.color.name}\'s turn now...')
        self.__time_start = timer()
        thread = threading.Thread(target=self.__get_bot_move)
        thread.start()

    def __get_bot_move(self) -> None:
        while self.__is_move_in_progress and self.__is_game_in_progress:
            col, row = self.__current_player.get_next_move(copy.deepcopy(self.__board))
            self.__move(col, row)

    def __get_user_move(self, mouse_pos: tuple[int, int]) -> None:
        if not isinstance(self.__current_player, UserPlayer):
            return
        col, row = self.__get_field_from_mouse_pos(mouse_pos)
        if col < 0 or row < 0:
            return
        self.__move(col, row)

    def __get_field_from_mouse_pos(self, mouse_pos: tuple[int, int]) -> tuple[int, int]:
        mouse_x, mouse_y = mouse_pos
        left = self.__WIDTH - self.__HEIGHT
        col = int(round(mouse_x - left) // self.__field_size)
        row = int(round(mouse_y) // self.__field_size)
        return (col, row)

    def __move(self, col: int, row: int) -> None:
        if not self.__board.move(col, row, self.__current_player.color):
            return
        if self.__print_game_events:
            print(f'Move done by {self.__current_player}: COL: {col}, ROW: {row}.')
            self.__board.refresh_result()
            print(f'Current result: BLACK : {self.__board.points[PlayerColor.BLACK]}, WHITE: {self.__board.points[PlayerColor.WHITE]}.\n')
        elif not self.__is_board_displayed:
            self.__board.refresh_result()
        self.__move_times[self.__current_player.color] += 1000 * (timer() - self.__time_start)
        if self.__board.can_move(self.__players[-self.__current_player.color.value].color):
            self.__current_player = self.__players[-self.__current_player.color.value]
        self.__is_move_in_progress = False

    def __print_final_result(self) -> None:
        print(f'Game over! Final result: BLACK : {self.__board.points[PlayerColor.BLACK]}, WHITE: {self.__board.points[PlayerColor.WHITE]}.')
        winner_color = self.__board.get_leader()
        if winner_color is None:
            print('Draw! There is not winner! Congrats for both players! \n')
        else:
            winner = self.__players[winner_color.value]
            print(f'{winner} is the winner! Congrats!\n')
