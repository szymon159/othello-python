from abc import abstractmethod
from collections import defaultdict
import copy
from random import Random
import numpy as np
from othello_utils import PlayerColor, MCTSVersion
from state import AlphaBetaState, State

class Node:
    def __init__(self, state: State, color: PlayerColor, parent = None, parent_action: tuple[int, int, PlayerColor] = None):
        self.state = state
        self.player_color = color
        self.parent = parent
        self.parent_action = parent_action

    @abstractmethod
    def best_action(self, simulation_count: int) -> tuple[int, int]:
        '''
        Returns best action for node
        '''
        raise NotImplementedError('Method \"best_action\" is not implemented for base class. Use derived class instead')

    def valuate(self) -> int:
        '''
        Returns node value
        '''
        return self.state.game_result()

    def is_terminal_node(self) -> bool:
        '''
        Returns True if current node is terminal (is a leaf node)
        '''
        return self.state.is_game_over()

class MCTSNode(Node):
    def __init__(self, state: State, color: PlayerColor, seed: int, parent=None, parent_action: tuple[int, int, PlayerColor] = None, version: MCTSVersion = MCTSVersion.UCT):
        super().__init__(state, color, parent, parent_action)
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
        self._random_seed = seed
        self._random = Random(self._random_seed)

    def best_action(self, simulation_count: int) -> tuple[int, int]:
        '''
        Returns best action for node
        '''
        for _ in range(simulation_count):
            #print(f'Iteration {i}')
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        action = self.best_child_simple().parent_action
        return (action[0], action[1])

    def valuate(self) -> int:
        '''
        Returns a difference between the amount of wins and losses
        '''
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def untried_actions(self) -> list[tuple[int, int, PlayerColor]]:
        '''
        Returns all untried actions from this node's state
        '''
        self._untried_actions = self.state.get_legal_actions()
        if len(self._untried_actions) == 0:
            self.state.change_color()
            self._untried_actions = self.state.get_legal_actions()

        return self._untried_actions

    def n(self) -> int:
        '''
        Returns an amount of times the node was visited
        '''
        return self._number_of_visits

    def expand(self) -> "MCTSNode":
        '''
        Expands the tree towards a random unexplored child
        '''
        col, row, move_color = self._untried_actions.pop()
        board, color= self.state.move(col, row)
        child_node = MCTSNode(State(board, color), self.player_color, self._random_seed, parent=self, parent_action=(col, row, move_color))

        self._children.append(child_node)
        return child_node

    def rollout(self) -> int:
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

        return current_rollout_state.game_result(self.player_color)

    def backpropagate(self, result):
        '''
        Backpropagates through visited nodes and updates statistics
        '''
        if self.state.current_color != self.player_color:
            result = -result
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self) -> bool:
        '''
        Returns True if all children of node have been expanded
        '''
        return len(self._untried_actions) == 0

    def best_child(self, c_param=1) -> "MCTSNode":
        '''
        Returns the most promising child using the formula specified by version
        '''
        if self.version == MCTSVersion.UCT:
            choices_weights = [(c.valuate() / c.n()) + c_param * np.sqrt((np.log(self.n()) / c.n())) for c in self._children]
        return self._children[np.argmax(choices_weights)]

    def best_child_simple(self) -> "MCTSNode":
        '''
        Returns the best child using simple formula
        '''
        choices_weights = [(c.valuate() / c.n())  for c in self._children]
        return self._children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves: list[tuple[int, int, PlayerColor]]) -> tuple[int, int, PlayerColor]:
        '''
        Returns random move
        '''
        return possible_moves[self._random.randint(0, len(possible_moves) - 1)]

    def _tree_policy(self) -> "MCTSNode":
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

class AlphaBetaNode(Node):
    def __init__(self, state: AlphaBetaState, player_color: PlayerColor, max_depth: int, alpha: int, beta: int, parent: Node = None, parent_action: tuple[int, int, PlayerColor] = None):
        super().__init__(state, player_color, parent, parent_action)
        self.level = parent.level + 1 if isinstance(parent, AlphaBetaNode) else 0
        self.best_child = None
        self.__max_depth = max_depth
        self.__alpha = alpha
        self.__beta = beta

    def best_action(self, _: int = 1) -> tuple[int, int]:
        self.valuate()
        return (self.best_child.parent_action[0], self.best_child.parent_action[1])

    def valuate(self) -> int:
        if self.is_terminal_node():
            return self.state.game_result(self.state.current_color)

        if not self.state.can_move():
            self.state.change_color()

        is_max_node = self.state.current_color == self.player_color
        for col, row, move_color in self.state.get_legal_actions():
            board, color = self.state.move(col, row)
            child_node = AlphaBetaNode(AlphaBetaState(board, color), self.player_color, self.__max_depth, self.__alpha, self.__beta, self, [col, row, move_color])
            child_result = child_node.valuate()
            if is_max_node:
                if child_result > self.__alpha:
                    self.__alpha = child_result
                    self.best_child = child_node
                if self.__alpha >= self.__beta:
                    return self.__beta
            else:
                if child_result < self.__beta:
                    self.__beta = child_result
                    self.best_child = child_node
                if self.__beta <= self.__alpha:
                    return self.__alpha

        return self.__alpha if is_max_node else self.__beta

    def is_terminal_node(self) -> bool:
        return self.level + 1 >= self.__max_depth or super().is_terminal_node()
