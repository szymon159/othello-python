from os import stat
from pyparsing import White
from board import Board
from othello_utils import PlayerColor
from state import State
from player import Player
from collections import defaultdict
import numpy as np
import copy

class Node:
    def __init__(self, state: State, color: PlayerColor, parent=None, parent_action=None):
        self.state = state
        self.player_color = color
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[0] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()

    '''
    Returns all untried actions from this node's state
    '''
    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    '''
    Returns a difference between the amount of wins and losses
    '''
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    '''
    Returns an amount of times the node was visited
    '''
    def n(self):
        return self._number_of_visits

    '''
    Expands the three towards a random unexplored child 
    '''
    def expand(self):
        col, row, move_color = self._untried_actions.pop()
        board, color= self.state.move(col, row)
        child_node = Node(State(board, color), self.player_color, parent=self, parent_action=(col, row, move_color))

        self.children.append(child_node)
        return child_node     

    '''
    Returns True if current node is terminal (is a leaf node)
    '''
    def is_terminal_node(self):
        return self.state.is_game_over()

    '''
    Simulate the game from node
    '''
    def rollout(self):
        current_rollout_state = copy.deepcopy(self.state)

        while current_rollout_state.can_move():
            # if not current_rollout_state.can_move():
            #     current_rollout_state.change_color()

            possible_moves = current_rollout_state.get_legal_actions()
            col, row, _ = self.rollout_policy(possible_moves)
            board, color = current_rollout_state.move(col, row)
            current_rollout_state = State(board, color)

        return current_rollout_state.game_result(self.player_color)

    '''
    Backpropagates through visited nodes and updates statistics
    '''
    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result) 

    '''
    Returns True if all children of node have been expanded
    '''
    def is_fully_expanded(self):
        return len(self._untried_actions) == 0       

    '''
    Returns the most promising child using the UCT formula
    '''
    def best_child(self, c_param=1.3):     
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]     

    '''
    Returns random move
    '''
    def rollout_policy(self, possible_moves): 
        return possible_moves[np.random.randint(len(possible_moves))]

    '''
    Follows best children of nodes until reaching a node that wasn't fully expanded. 
    Then proceeds to expand that node.
    '''
    def _tree_policy(self):

        current_node = self
        while current_node.state.can_move():
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()

        return current_node    

    '''
    Returns best action for node
    '''
    def best_action(self, simulation_count):        
        for i in range(simulation_count):
            #print(f'Iteration {i}')
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        
        return self.best_child(c_param=0.)           
