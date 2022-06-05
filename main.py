from heuristic_player import AlphaBetaHeuristicPlayer, SimpleHeuristicPlayer
from othello_game import OthelloGame
from othello_utils import PlayerColor
from player import RandomPlayer
from uct_player import UCTPlayer
from othello_utils import MCTSVersion

def main():
    players = [SimpleHeuristicPlayer(PlayerColor.BLACK), UCTPlayer(PlayerColor.WHITE, version=MCTSVersion.UCT_GROUPING, simulation_count=200)]
    game = OthelloGame(players)
    if not game.run_game():
        pass

if __name__ == "__main__":
    main()
