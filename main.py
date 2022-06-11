from config import ConfigModel
from othello_game import OthelloGame
from timeit import default_timer as timer

def main():
    config = ConfigModel.get_from_file('config.json')
    matches = config.get_matches()
    for i, match in enumerate(matches):

        print(f'\nMatch {i + 1}: {str(match.players[0]).split(" ", maxsplit=1)[0]} vs {str(match.players[1]).split(" ", maxsplit=1)[0]}')
        for players in match.get_games():
            game = OthelloGame(players, config.show_visualization)
            time_start = timer()
            if not game.run_game():
                result = game.get_result()
                match.add_game_result(result)
                print(f'Game result ({players[0].color.name} - {players[1].color.name}): {match.results[-1][0]} - {match.results[-1][1]}')
                print(f'Game time: {1000 * (timer() - time_start)}')
        print(f'Match result: {match.total[0]} - {match.total[1]}')

if __name__ == "__main__":
    main()
