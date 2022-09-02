import copy
from collections import defaultdict
from board import Board
from othello_utils import HEURISTIC_WEIGHTS, PlayerColor

class State:
    '''
    Base class with information about a game state inside specific node of the game tree.
    '''
    def __init__(self, board: Board, color: PlayerColor):
        self.current_color = color
        self.board = board

    def is_game_over(self):
        '''
        Returns True if game is over.
        '''
        return not (self.board.can_move(self.current_color) or self.board.can_move(PlayerColor(-self.current_color.value)))

    def can_move(self):
        '''
        Returns True if game is over.
        '''
        return self.board.can_move(self.current_color)

    def change_color(self):
        '''
        Change color if have to wait turn.
        '''
        self.current_color = PlayerColor(-self.current_color.value)

    def get_legal_actions(self) -> list[tuple[int, int, PlayerColor]]:
        '''
        Returns all legal actions for player.
        '''
        return [(col, row, self.current_color) for (col, row) in self.board.get_legal_actions(self.current_color)]

    def move(self, col, row):
        '''
        Performs a specified move on a copy of board and returns the copy and color of next moving player.
        '''
        board_copy = copy.deepcopy(self.board)
        board_copy.move(col, row, self.current_color)
        board_copy.refresh_result()
        return board_copy, PlayerColor(-self.current_color.value)

    def game_result(self, player_color: PlayerColor) -> int:
        '''
        Returns 1 if game's result is players victory, -1 if it's player's loose or 0 if it's a draw.
        '''
        winner_color = self.board.get_leader()
        if winner_color is None:
            return 0
        if winner_color == player_color:
            return 1
        return -1

    def to_string(self):
        '''
        Returns stringfied state.
        '''
        ret_str = ''
        field = self.board.get_field()
        for i in range(self.board.COLS):
            ret_str = ret_str.join(str(e) for e in field[i])
        return ret_str

class AlphaBetaState(State):
    '''
    Class with information about a game state inside specific node of the game tree used in alpha-beta prunning.
    '''
    def game_result(self, player_color: PlayerColor) -> int:
        '''
        Returns heuristic valuation of player's pawns in current state
        '''
        if self.is_game_over():
            return self.board.points[player_color]

        player_points = 0
        for col in range(self.board.COLS):
            for row in range(self.board.ROWS):
                if self.board[col, row] == player_color.value:
                    player_points += HEURISTIC_WEIGHTS[col][row]
        return player_points

class GroupingGraphState(State):
    '''
    Class with information about a game state inside specific node of the game tree (graph) used in MCTS modification with grouping of identical states.
    '''
    def __init__(self, board: Board, color: PlayerColor) -> None:
        super().__init__(board, color)
        self.number_of_visits = 0
        self.results = defaultdict(int)
        self.results[1] = 0
        self.results[0] = 0
        self.results[-1] = 0

    def rotate_board(self) -> "GroupingGraphState":
        '''
        Rotates the board and returns the state with it.
        '''
        self.board.rotate_board()
        return self

    def check_if_in_dictionary(self, dictionary: dict) -> bool:
        '''
        Checks if the state is already added to specified \"dictionary\".
        '''
        if self.to_string() in dictionary:
            return True
        elif self.rotate_board().to_string() in dictionary:
            return True
        elif self.rotate_board().to_string() in dictionary:
            return True
        elif self.rotate_board().to_string() in dictionary:
            return True
        return False
