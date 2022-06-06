from collections import defaultdict
import copy
from state import State
from board import Board
from othello_utils import PlayerColor
import numpy as np

class GraphState(State):
    def __init__(self, board: Board, color: PlayerColor):
        self.current_color = color
        self.board = board
        self.number_of_visits = 0
        self.results = defaultdict(int)
        self.results[1] = 0
        self.results[0] = 0
        self.results[-1] = 0

    def rotate_board(self) -> None:
        self.board.rotate_board()
        return self