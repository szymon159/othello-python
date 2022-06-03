from board import Board
from othello_utils import PlayerColor
import copy

class State:
    def __init__(self, board: Board, color: PlayerColor):
        self.current_color = color
        self.board = board

    '''
    Returns True if game is over
    '''
    def is_game_over(self):
        if self.board.points[PlayerColor.BLACK] + self.board.points[PlayerColor.WHITE] == 64:
            return True
        return not (self.board.can_move(self.current_color) or self.board.can_move(PlayerColor(-self.current_color.value)))

    '''
    Returns True if game is over
    '''
    def can_move(self):
        if self.board.points[PlayerColor.BLACK] + self.board.points[PlayerColor.WHITE] == 64:
            return False
        return self.board.can_move(self.current_color)

    '''
    Change color if have to wait turn
    '''
    def change_color(self):
        self.current_color = PlayerColor(-self.current_color.value)

    '''
    Returns all legal actions for player
    '''
    def get_legal_actions(self):
        moves = []
        for i in range(self.board.COLS):
            for j in range(self.board.ROWS):
                if self.board.evaluate_move(i, j, self.current_color) > 0:
                    moves.append((i,j,self.current_color))
        return moves

    # '''
    # Performs a specified move
    # '''
    # def move(self, col, row):
    #     self.board.move(col, row, self.current_color)
    #     return State(copy.deepcopy(self.board), PlayerColor(-self.current_color.value)

    '''
    Performs a specified move on a copy of board and returns the copy and color of next moving player
    '''
    def move(self, col, row):
        board_copy = copy.deepcopy(self.board)
        board_copy.move(col, row, self.current_color)
        board_copy.refresh_result()
        return board_copy, PlayerColor(-self.current_color.value)


    '''
    Returns 1 if game's result is players victory, -1 if it's player's loose or 0 if it's a draw
    '''
    def game_result(self, player_color: PlayerColor):
        player_points = self.board.points[player_color]
        opponent_points = self.board.points[PlayerColor(-player_color.value)]
        if player_points > opponent_points:
            return 1 
        if player_points < opponent_points:
            return -1 
        return 0
