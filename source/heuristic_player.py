import math
import numpy as np
from board import Board
from node import AlphaBetaNode
from othello_utils import HEURISTIC_WEIGHTS, PlayerColor
from player import Player
from state import AlphaBetaState

class SimpleHeuristicPlayer(Player):
    '''
    Player performing all moves naively - by gaining the most points in one move.
    '''
    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        moves = []
        for i in range(board_copy.COLS):
            for j in range(board_copy.ROWS):
                if board_copy.evaluate_move(i, j, self.color) > 0:
                    moves.append((i,j))
        moves_values = [HEURISTIC_WEIGHTS[col][row] for col, row in moves]

        return moves[np.argmax(moves_values)]

class AlphaBetaHeuristicPlayer(SimpleHeuristicPlayer):
    '''
    Player using alpha-beta prunning to determine next move.
    '''
    def __init__(self, color: PlayerColor, simulation_depth: int = 5) -> None:
        super().__init__(color)
        self.__max_depth = simulation_depth

    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        tree_root = AlphaBetaNode(AlphaBetaState(board_copy, self.color), self.color, self.__max_depth, -math.inf, math.inf)
        return tree_root.best_action()
