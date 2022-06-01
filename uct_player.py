from board import Board
from othello_utils import PlayerColor
from state import State
from node import Node
import player

class UCTPlayer(player.Player):
    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        state = State(board_copy, self.color)
        tree_root = Node(state)
        best_action = tree_root.best_action()
        col, row, _  = best_action.parent_action

        return (col, row)