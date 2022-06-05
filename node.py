from collections import defaultdict
import copy
import numpy as np
from othello_utils import PlayerColor, MCTSVersion
from state import State

def myCounter():
  myCounter.counter += 1

class Node:
    def __init__(self, state: State, color: PlayerColor, parent=None, parent_action=None, version: MCTSVersion = MCTSVersion.UCT):
        self.state = state
        self.uct_player_color = color
        self.parent = parent
        self.parent_action = parent_action
        self.version = version
        self.reward_list = []
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
        myCounter.counter = 0
        for i in range(simulation_count):
            #print(f'Iteration {i}')
            myCounter()
            self._iteration_count = i + 1
            v = self._tree_policy()
            reward = v._rollout()
            v._backpropagate(reward)
        
        return self._best_child_simple()           

    def get_iteration_count(self):
        if self.parent == None:
            return self._iteration_count
        else:
            return self.get_iteration_count()
            
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
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        '''
        Returns an amount of times the node was visited
        '''
        return self._number_of_visits

    def _expand(self):
        '''
        Expands the three towards a random unexplored child 
        '''
        col, row, move_color = self._untried_actions.pop()
        board, color= self.state.move(col, row)
        child_node = Node(State(board, color), self.uct_player_color, parent=self, parent_action=(col, row, move_color), version=self.version)

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
        self._number_of_visits += 1.
        self._results[result] += 1.
        self.reward_list.append(result)
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
        if self.version == MCTSVersion.UCT:
            choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((np.log(self.n()) / c.n())) for c in self._children]
        if self.version == MCTSVersion.UCB1_TUNED:
            v = [np.sum([x**2 for x in c.reward_list])/c.n() - (c.q()/c.n())**2 + np.sqrt(2*np.log(myCounter.counter) / c.n()) for c in self._children]
            c_params = [np.sqrt(np.min([1/4, v_i])) for v_i in v]
            choices_weights = [(c.q() / c.n()) + c_params[i] * np.sqrt((2*np.log(self.n()) / c.n()))  for i, c in enumerate(self._children, start=0)]
            
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

