from abc import abstractmethod
import random

from board import Board
from othello_utils import PlayerColor

class Player:
    def __init__(self, color: PlayerColor) -> None:
        self.color = color

    @abstractmethod
    def get_next_move(self, board: Board) -> tuple[int, int]:
        raise NotImplementedError('Mehtod cannot be called from abstract class')

class UserPlayer(Player):
    def get_next_move(self, board: Board) -> tuple[int, int]:
        raise NotImplementedError('Next move can be determined only for bots')

class RandomPlayer(Player):
    def get_next_move(self, board: Board) -> tuple[int, int]:
        while True:
            row, col = random.randint(0, board.ROWS - 1), random.randint(1, board.COLS - 1)
            if board.evaluate_move(row, col, self.color) > 0:
                return (row, col)
