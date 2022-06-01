from board import Board
from othello_utils import PlayerColor
import copy

class State:
    def __init__(self, board: Board, color: PlayerColor):
        self.color = color
        self.board = board

    '''
    Returns True if game is over
    '''
    def is_game_over(self):
        return not self.board.can_move(self.color)

    '''
    Returns all legal actions for player
    '''
    def get_legal_actions(self):
        moves = []
        for i in range(self.board.COLS):
            for j in range(self.board.ROWS):
                if self.board.evaluate_move(i, j, self.color) > 0:
                    moves.append((i,j, self.color))
        return moves

    '''
    Performs a specified move
    '''
    def move(self, col, row, color):
        self.board.move(col, row, color)
        state = State(copy.deepcopy(self.board), color)
        return state

    '''
    Returns 1 if game's result is players victory, -1 if it's player's loose or 0 if it's a draw
    '''
    def game_result(self):
        white_player_point = self.board.points[PlayerColor.WHITE]
        black_player_point = self.board.points[PlayerColor.BLACK]
        if white_player_point > black_player_point and self.color.value == 1:
            return 1 
        if white_player_point > black_player_point and self.color.value != 1:
            return -1
        if white_player_point < black_player_point and self.color.value == 1:
            return -1 
        if white_player_point < black_player_point and self.color.value != 1:
            return 1
        return 0
