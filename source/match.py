from typing import Generator
from othello_utils import PlayerColor
from player import Player

class Match():
    '''
    Class with information about a single match, each match contains 3 games.
    Contains information about player names, results of each game and total match result.
    '''
    def __init__(self, games: list[tuple[Player, Player]]) -> None:
        self.total = [0, 0]
        self.results = []
        self.player_names = [str(p).split(" ", maxsplit=1)[0] for p in games[0]]
        self.__games = games

    def get_games(self) -> Generator[tuple[Player, Player], None, None]:
        '''
        Yields pairs of players for each game.
        If any player already won 2 games, no more games are returned.
        Can be used with updating the result between fetching new fields to handle logic of playing 3rd game only if needed.
        '''
        for game in self.__games:
            if self.total[0] < 2 and self.total[1] < 2:
                yield [game[0], game[1]]

    def add_game_result(self, game_number: int, result: dict[PlayerColor, int]) -> None:
        '''
        Updates match with \"result\" of game with specified \"game_number\".
        '''
        res = (result[self.__games[game_number][0].color], result[self.__games[game_number][1].color])
        self.results.append(res)
        if res[0] > res[1]:
            self.total[0] += 1
        elif res[0] < res[1]:
            self.total[1] += 1
        else:
            self.total[0] += 0.5
            self.total[1] += 0.5
