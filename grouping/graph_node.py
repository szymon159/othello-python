from collections import defaultdict
import copy
from os import stat
import numpy as np
from othello_utils import PlayerColor, check_if_in_dictionary
from state import State
from grouping.graph_state import GraphState

class GraphNode():
    def __init__(self, state: GraphState, color: PlayerColor, state_dict, parent=None, parent_action=None):
        self.state = state
        self.uct_player_color = color
        self.state_dictionary = state_dict
        self.parent = parent
        self.parent_action = parent_action
        self._children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[0] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self._get_untried_actions()

    def best_action(self, simulation_count):
        '''
        Returns best action for node
        '''
        for i in range(simulation_count):
            #print(f'Iteration {i}')
            self._iteration_count = i + 1
            v = self._tree_policy()
            reward = v._rollout()
            v._backpropagate(reward)

        return self._best_child_simple()

    def _get_untried_actions(self):
        '''
        Returns all untried actions from this node's state
        '''
        self._untried_actions = self.state.get_legal_actions()
        if len(self._untried_actions) == 0:
            self.state.change_color()
            self._untried_actions = self.state.get_legal_actions()

        return self._untried_actions

    def q(self):
        '''
        Returns a difference between the amount of wins and losses
        '''
        wins = self.state.results[1]
        loses = self.state.results[-1]
        return wins - loses

    def n(self):
        '''
        Returns an amount of times the node was visited
        '''
        return self.state.number_of_visits

    def _expand(self):
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

        child_node = GraphNode(state, self.uct_player_color, self.state_dictionary, parent=self, parent_action=(col, row, move_color))
        self._children.append(child_node)
        return child_node

    def _is_terminal_node(self):
        '''
        Returns True if current node is terminal (is a leaf node)
        '''
        return self.state.is_game_over()

    def _rollout(self):
        '''
        Simulate the game from node
        '''
        current_rollout_state = copy.deepcopy(self.state)

        while not current_rollout_state.is_game_over():
            if not current_rollout_state.can_move():
                current_rollout_state.change_color()

            possible_moves = current_rollout_state.get_legal_actions()
            col, row, _ = self._rollout_policy(possible_moves)
            board, color = current_rollout_state.move(col, row)
            current_rollout_state = State(board, color)

        return current_rollout_state.game_result(self.uct_player_color)

    def _backpropagate(self, result):
        '''
        Backpropagates through visited nodes and updates statistics
        '''
        if self.state.current_color != self.uct_player_color:
            result = -result
        self.state.number_of_visits += 1.
        self.state.results[result] += 1.
        if self.parent:
            self.parent._backpropagate(result)

    def _is_fully_expanded(self):
        '''
        Returns True if all children of node have been expanded
        '''
        return len(self._untried_actions) == 0

    def _best_child(self, c_param=1):
        '''
        Returns the most promising child using the formula specified by version
        '''
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((np.log(self.n()) / c.n())) for c in self._children]
        return self._children[np.argmax(choices_weights)]

    def _best_child_simple(self):
        '''
        Returns the best child using simple formula
        '''
        choices_weights = [(c.q() / c.n())  for c in self._children]
        return self._children[np.argmax(choices_weights)]

    def _rollout_policy(self, possible_moves):
        '''
        Returns random move
        '''
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        '''
        Follows best children of nodes until reaching a node that wasn't fully expanded.
        Then proceeds to expand that node.
        '''
        current_node = self
        while not current_node._is_terminal_node():

            if not current_node._is_fully_expanded():
                return current_node._expand()
            else:
                current_node = current_node._best_child(c_param= np.sqrt(2))

        return current_node

