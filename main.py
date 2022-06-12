from config import ConfigModel
from othello_game import OthelloGame
from timeit import default_timer as timer

def main():
    config = ConfigModel.get_from_file('config.json')

    if config.output_file:
        output_file = open(config.output_file, 'w', encoding='utf8')
        output_file.write('player1,color1,result1,player2,color2,result2\n')

    matches = config.get_matches()
    for i, match in enumerate(matches):
        player_names = [str(p).split(" ", maxsplit=1)[0] for p in match.players]
        print(f'\nMatch {i + 1}: {player_names[0]} vs {player_names[1]}')
        for players in match.get_games():
            game = OthelloGame(players, config.show_visualization)
            time_start = timer()
            if not game.run_game():
                result = game.get_result()
                times = game.get_times()
                match.add_game_result(result)
                output_file.write(f'{player_names[0]},{players[0].color.name.lower()},{match.results[-1][0]},{player_names[1]},{players[1].color.name.lower()},{match.results[-1][1]}\n')
                print(f'Game result ({players[0].color.name} - {players[1].color.name}): {match.results[-1][0]} - {match.results[-1][1]}')
                print(f'Game time: {1000 * (timer() - time_start)} ({times[players[0].color]} s vs {times[players[1].color]})')
        print(f'Match result: {match.total[0]} - {match.total[1]}')

    if config.output_file and not output_file.closed:
        output_file.close()

if __name__ == "__main__":
    main()
