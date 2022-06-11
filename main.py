from config import ConfigModel
from othello_game import OthelloGame

def main():
    config = ConfigModel.get_from_file('config.json')
    matches = config.get_matches()
    for i, match in enumerate(matches):
        print(f'\nMatch {i + 1}: {type(match.players[0]).__name__} vs {type(match.players[1]).__name__}')
        for players in match.get_games():
            game = OthelloGame(players, config.show_visualization)
            if not game.run_game():
                result = game.get_result()
                match.add_game_result(result)
                print(f'Game result ({players[0].color.name} - {players[1].color.name}): {match.results[-1][0]} - {match.results[-1][1]}')
        print(f'Match result: {match.total[0]} - {match.total[1]}')

if __name__ == "__main__":
    main()
