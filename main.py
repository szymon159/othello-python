from othello_game import OthelloGame
from othello_utils import PlayerColor
from player import RandomPlayer, UserPlayer

def main():
    players = [RandomPlayer(PlayerColor.BLACK), UserPlayer(PlayerColor.WHITE)]
    game = OthelloGame(players)
    if not game.run_game():
        pass

if __name__ == "__main__":
    main()
