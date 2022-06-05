from importlib_metadata import version
from board import Board
from grouping.graph_node import GraphNode
from grouping.graph_state import GraphState
from othello_utils import PlayerColor, MCTSVersion, check_if_in_dictionary
from state import State
from node import Node
import player

class UCTPlayer(player.Player):
    def __init__(self, color: PlayerColor, simulation_count: int = 500, version: MCTSVersion = MCTSVersion.UCT) -> None:
        super().__init__(color)
        self.simulation_count = simulation_count
        self.version = version
        self._state_dict = {}

    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        if self.version != MCTSVersion.UCT_GROUPING:
            tree_root = Node(State(board_copy, self.color), self.color, version = self.version)
            best_action = tree_root.best_action(self.simulation_count)
            col, row, _  = best_action.parent_action
        else:
            state = GraphState(board_copy, self.color)
            state_to_str = state.to_string()
            if check_if_in_dictionary(state, self._state_dict):
                state = self._state_dict[state_to_str]       
            else:
                self._state_dict[state_to_str] = state  

            tree_root = GraphNode(GraphState(board_copy, self.color), self.color, state_dict = self._state_dict)
            best_action = tree_root.best_action(150)
            col, row, _  = best_action.parent_action

        return (col, row)