import copy
from board import Board
from othello_utils import HEURISTIC_WEIGHTS, PlayerColor

class State:
    def __init__(self, board: Board, color: PlayerColor):
        self.current_color = color
        self.board = board

    def is_game_over(self):
        '''
        Returns True if game is over
        '''
        return not (self.board.can_move(self.current_color) or self.board.can_move(PlayerColor(-self.current_color.value)))

    def can_move(self):
        '''
        Returns True if game is over
        '''
        return self.board.can_move(self.current_color)

    def change_color(self):
        '''
        Change color if have to wait turn
        '''
        self.current_color = PlayerColor(-self.current_color.value)

    def get_legal_actions(self) -> list[tuple[int, int, PlayerColor]]:
        '''
        Returns all legal actions for player
        '''
        return [(col, row, self.current_color) for (col, row) in self.board.get_legal_actions(self.current_color)]

    def move(self, col, row):
        '''
        Performs a specified move on a copy of board and returns the copy and color of next moving player
        '''
        board_copy = copy.deepcopy(self.board)
        board_copy.move(col, row, self.current_color)
        board_copy.refresh_result()
        return board_copy, PlayerColor(-self.current_color.value)

    def game_result(self, player_color: PlayerColor) -> int:
        '''
        Returns 1 if game's result is players victory, -1 if it's player's loose or 0 if it's a draw
        '''
        player_points = self.board.points[player_color]
        opponent_points = self.board.points[PlayerColor(-player_color.value)]
        if player_points > opponent_points:
            return 1
        if player_points < opponent_points:
            return -1
        return 0

class AlphaBetaState(State):
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
