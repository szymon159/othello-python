from abc import abstractmethod
from random import Random

from board import Board
from othello_utils import PlayerColor

class Player:
    def __init__(self, color: PlayerColor) -> None:
        self.color = color

    @abstractmethod
    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        raise NotImplementedError('Mehtod cannot be called from abstract class')

class UserPlayer(Player):
    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        raise NotImplementedError('Next move can be determined only for bots')

class RandomPlayer(Player):
    def __init__(self, color: PlayerColor, seed: int) -> None:
        super().__init__(color)
        self.__random = Random(seed)

    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        moves = board_copy.get_legal_actions(self.color)
        col, row = moves[self.__random.randint(0, len(moves) - 1)]
        return (col, row)
