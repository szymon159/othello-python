from heuristic_player import AlphaBetaHeuristicPlayer, SimpleHeuristicPlayer
from othello_game import OthelloGame
from othello_utils import PlayerColor
from player import RandomPlayer
from uct_player import UCTPlayer

def main():
    players = [SimpleHeuristicPlayer(PlayerColor.BLACK), AlphaBetaHeuristicPlayer(PlayerColor.WHITE)]
    game = OthelloGame(players)
    if not game.run_game():
        pass

if __name__ == "__main__":
    main()
