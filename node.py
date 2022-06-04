from collections import defaultdict
import copy
import numpy as np
from othello_utils import PlayerColor, MCTSVersion
from state import State

class Node:
    def __init__(self, state: State, color: PlayerColor, parent=None, parent_action=None, version: MCTSVersion = MCTSVersion.UCT):
        self.state = state
        self.uct_player_color = color
        self.parent = parent
        self.parent_action = parent_action
        self.version = version
        self._children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[0] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        self._reward_list = []

    def untried_actions(self):
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
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        '''
        Returns an amount of times the node was visited
        '''
        return self._number_of_visits

    def expand(self):
        '''
        Expands the three towards a random unexplored child 
        '''
        col, row, move_color = self._untried_actions.pop()
        board, color= self.state.move(col, row)
        child_node = Node(State(board, color), self.uct_player_color, parent=self, parent_action=(col, row, move_color))

        self._children.append(child_node)
        return child_node     

    def is_terminal_node(self):
        '''
        Returns True if current node is terminal (is a leaf node)
        '''
        return self.state.is_game_over()

    def rollout(self):
        '''
        Simulate the game from node
        '''
        current_rollout_state = copy.deepcopy(self.state)

        while not current_rollout_state.is_game_over():
            if not current_rollout_state.can_move():
                current_rollout_state.change_color()

            possible_moves = current_rollout_state.get_legal_actions()
            col, row, _ = self.rollout_policy(possible_moves)
            board, color = current_rollout_state.move(col, row)
            current_rollout_state = State(board, color)

        return current_rollout_state.game_result(self.uct_player_color)

    def backpropagate(self, result):
        '''
        Backpropagates through visited nodes and updates statistics
        '''
        if self.state.current_color != self.uct_player_color:
            result = -result
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result) 

    def is_fully_expanded(self):
        '''
        Returns True if all children of node have been expanded
        '''
        return len(self._untried_actions) == 0       

    def best_child(self, c_param=1):     
        '''
        Returns the most promising child using the formula specified by version
        '''
        if self.version == MCTSVersion.UCT:
            choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((np.log(self.n()) / c.n())) for c in self._children]
        return self._children[np.argmax(choices_weights)]     

    def best_child_simple(self):     
        '''
        Returns the best child using simple formula
        '''
        choices_weights = [(c.q() / c.n())  for c in self._children]
        return self._children[np.argmax(choices_weights)]   

    def rollout_policy(self, possible_moves): 
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
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child(c_param= np.sqrt(2))

        return current_node    

    def best_action(self, simulation_count):        
        '''
        Returns best action for node
        '''
        for i in range(simulation_count):
            # print(f'Iteration {i}')
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        
        return self.best_child_simple()           
