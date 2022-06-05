from board import Board
from othello_utils import PlayerColor, MCTSVersion
from player import Player
from state import State
from node import MCTSNode
import player

class UCTPlayer(player.Player):
    def __init__(self, color: PlayerColor, seed: int, simulation_count: int = 500, version: MCTSVersion = MCTSVersion.UCT) -> None:
        super().__init__(color)
        self.simulation_count = simulation_count
        self.version = version
        self.seed = seed

    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        tree_root = MCTSNode(State(board_copy, self.color), self.color, self.seed, version = self.version)
        return tree_root.best_action(self.simulation_count)
