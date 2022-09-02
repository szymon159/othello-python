from timeit import default_timer as timer
from config import ConfigModel
from othello_game import OthelloGame

def main():
    '''
    Project's entry point.
    Reads config from file, parses it and run all games one by one, using configured UI and printing results to console.
    '''
    config = ConfigModel.get_from_file('source/config/config.json')

    if config.output_file:
        with open(config.output_file, 'w', encoding='utf8') as output_file:
            output_file.write('player1,color1,result1,player2,color2,result2\n')

    matches = config.get_matches()
    for i, match in enumerate(matches):
        player_names = match.player_names
        print(f'\nMatch {i + 1}: {player_names[0]} vs {player_names[1]}')
        for j, players in enumerate(match.get_games()):
            game = OthelloGame(players, config.show_visualization)
            time_start = timer()
            if not game.run_game():
                result = game.get_result()
                times = game.get_times()
                match.add_game_result(j, result)
                print(f'Game result ({players[0].color.name} - {players[1].color.name}): {match.results[-1][0]} - {match.results[-1][1]}')
                print(f'Game time: {1000 * (timer() - time_start)} ({times[players[0].color]} s vs {times[players[1].color]})')
                if config.output_file:
                    with open(config.output_file, 'a', encoding='utf8') as output_file:
                        output_file.write(f'{player_names[0]},{players[0].color.name.lower()},{match.results[-1][0]},{player_names[1]},{players[1].color.name.lower()},{match.results[-1][1]}\n')
        print(f'Match result: {match.total[0]} - {match.total[1]}')

if __name__ == "__main__":
    main()
