from abc import abstractmethod
from random import Random

from board import Board
from othello_utils import PlayerColor

class Player:
    '''
    Base class representing a player and providing interface for fetching their next move.
    '''
    def __init__(self, color: PlayerColor) -> None:
        self.color = color

    def __str__(self) -> str:
        return f'{type(self).__name__} ({self.color.name.lower()})'

    @abstractmethod
    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        '''
        Returns (row, col)-coordinates of player's next move based on \"board_copy\"
        This method is allowed to edit \"board_copy\", copying has to be handled before calling this method.
        '''
        raise NotImplementedError('Mehtod cannot be called from abstract class')

class UserPlayer(Player):
    '''
    Class representing a player controlled by real person using mouse. Fetching next move not supported.
    '''
    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        raise NotImplementedError('Next move can be determined only for bots')

class RandomPlayer(Player):
    '''
    Class representing a player performing random moves.
    '''
    def __init__(self, color: PlayerColor, seed: int) -> None:
        super().__init__(color)
        self.__random = Random(seed)

    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        moves = board_copy.get_legal_actions(self.color)
        col, row = moves[self.__random.randint(0, len(moves) - 1)]
        return (col, row)
