from board import Board
from othello_utils import PlayerColor
from state import State
from node import Node
import player
import numpy as np

class SimpleHeuristicPlayer(player.Player):
    def __init__(self, color: PlayerColor) -> None:
        super().__init__(color)
        self.weights = [[120, -20,  20,  5,  5,  20, -20, 120],
                        [-20, -40,  -5, -5, -5,  -5, -30, -20],
                        [ 20,  -5,  15,  3,  3,  15,  -5,  20],
                        [  5,  -5,   3,  3,  3,   3,  -5,   5],
                        [  5,  -5,   3,  3,  3,   3,  -5,   5],
                        [ 20,  -5,  15,  3,  3,  15,  -5,  20],
                        [-20, -40,  -5, -5, -5,  -5, -30, -20],
                        [120, -20,  20,  5,  5,  20, -20, 120]]

    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        moves = []
        for i in range(board_copy.COLS):
            for j in range(board_copy.ROWS):
                if board_copy.evaluate_move(i, j, self.color) > 0:
                    moves.append((i,j))
        moves_values = [self.weights[col][row] for col, row in moves]

        return moves[np.argmax(moves_values)]
