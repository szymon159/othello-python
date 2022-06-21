from othello_utils import PlayerColor
from player import Player


class Match():
    def __init__(self, games: list[tuple[Player, Player]]) -> None:
        self.total = [0, 0]
        self.results = []
        self.player_names = [str(p).split(" ", maxsplit=1)[0] for p in games[0]]
        self.__games = games

    def get_games(self):
        for game in self.__games:
            if self.total[0] < 2 and self.total[1] < 2:
                yield [game[0], game[1]]

    def add_game_result(self, game_number: int, result: dict[PlayerColor, int]):
        res = (result[self.__games[game_number][0].color], result[self.__games[game_number][1].color])
        self.results.append(res)
        if res[0] > res[1]:
            self.total[0] += 1
        elif res[0] < res[1]:
            self.total[1] += 1
        else:
            self.total[0] += 0.5
            self.total[1] += 0.5
