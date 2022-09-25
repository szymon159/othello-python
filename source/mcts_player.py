from board import Board
from othello_utils import PlayerColor, MCTSVersion
from state import State, GroupingGraphState
from node import MCTSNode, GroupingGraphNode
from player import Player

class MCTSPlayer(Player):
    '''
    Class representing a player using one of the implemented verions of MCTS algorithm.
    '''
    def __init__(self, color: PlayerColor, seed: int = 10, simulation_count: int = 500, version: MCTSVersion = MCTSVersion.UCT) -> None:
        super().__init__(color)
        self.simulation_count = simulation_count
        self.version = version
        self.seed = seed
        self.state_dict = {}

    def get_next_move(self, board_copy: Board) -> tuple[int, int]:
        version_tmp = self.version
        if version_tmp == MCTSVersion.UCT_GROUPING:
            if board_copy.points[PlayerColor.BLACK] + board_copy.points[PlayerColor.WHITE] < 15:
                state = GroupingGraphState(board_copy, self.color)
                state_to_str = state.to_string()
                self.state_dict[state_to_str] = state

                tree_root = GroupingGraphNode(GroupingGraphState(board_copy, self.color), self.color, state_dict = self.state_dict, seed = self.seed)
                best_action = tree_root.best_action(int(self.simulation_count/2))
                col, row, _  = best_action.parent_action
            else:
                version_tmp = MCTSVersion.UCT

        if version_tmp != MCTSVersion.UCT_GROUPING:
            tree_root = MCTSNode(State(board_copy, self.color), self.color, self.seed, version = version_tmp)
            best_action = tree_root.best_action(self.simulation_count)
            col, row, _  = best_action.parent_action

        return (col, row)

    def __str__(self) -> str:
        return f'{type(self).__name__}-{self.version.name} ({self.color.name.lower()})'
