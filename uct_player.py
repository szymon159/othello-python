from board import Board
from othello_utils import PlayerColor, MCTSVersion
from state import State
from node import Node
import player

class UCTPlayer(player.Player):
    def __init__(self, color: PlayerColor, simulation_count: int = 500, version: MCTSVersion = MCTSVersion.UCT) -> None:
        super().__init__(color)
        self.simulation_count = simulation_count
        self.version = version

    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        tree_root = Node(State(board_copy, self.color), self.color, version = self.version)
        best_action = tree_root.best_action(self.simulation_count)
        col, row, _  = best_action.parent_action

        return (col, row)