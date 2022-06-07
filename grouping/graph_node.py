from othello_utils import PlayerColor, check_if_in_dictionary
from grouping.graph_state import GraphState
from node import MCTSNode

class GraphNode(MCTSNode):
    def __init__(self, state: GraphState, color: PlayerColor, state_dict, seed: int = 10, parent=None, parent_action=None):
        super().__init__(state, color, seed, parent, parent_action)
        self.state_dictionary = state_dict

    def valuate(self) -> int:
        '''
        Returns a difference between the amount of wins and losses
        '''
        wins = self.state.results[1]
        loses = self.state.results[-1]
        return wins - loses

    def n(self) -> int:
        '''
        Returns an amount of times the node was visited
        '''
        return self.state.number_of_visits

    def _expand(self) -> "GraphNode":
        '''
        Expands the three towards a random unexplored child
        '''
        col, row, move_color = self._untried_actions.pop()
        board, color= self.state.move(col, row)
        state = GraphState(board, color)
        state_to_str = state.to_string()

        if check_if_in_dictionary(state, self.state_dictionary):
            state = self.state_dictionary[state.to_string()]
        else:
            self.state_dictionary[state_to_str] = state

        child_node = GraphNode(state, self.player_color, self.state_dictionary, parent=self, parent_action=(col, row, move_color))
        self._children.append(child_node)
        return child_node


    def _backpropagate(self, result):
        '''
        Backpropagates through visited nodes and updates statistics
        '''
        if self.state.current_color != self.player_color:
            result = -result
        self.state.number_of_visits += 1.
        self.state.results[result] += 1.
        if self.parent:
            self.parent._backpropagate(result)


