from abc import abstractmethod
import random
import time

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
            col, row = random.randint(0, board.COLS - 1), random.randint(0, board.ROWS - 1)
            if board.evaluate_move(col, row, self.color) > 0:
                time.sleep(2)
                return (col, row)
