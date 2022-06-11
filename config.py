from enum import Enum
import json
from random import Random
from heuristic_player import AlphaBetaHeuristicPlayer, SimpleHeuristicPlayer
from othello_utils import MCTSVersion

from player import Player, RandomPlayer, UserPlayer
from uct_player import UCTPlayer

class GameType(Enum):
    MATCH = "match"
    TOURNAMENT = "tournament"

class PlayerConfig():
    class PlayerType(Enum):
        USER = "user"
        SIMPLE_HEURISTIC = "simple_heuristic"
        HEURISTIC = "heuristic"
        RANDOM = "random"
        MCTS = "MCTS"
        MCTS_UCB = "MCTS_UCB"
        MCTS_GROUPING = "MCTS_grouping"

    class PlayerColor(Enum):
        BLACK = "black"
        WHITE = "white"

    def __init__(self, parsed_config: dict) -> None:
        self.type = PlayerConfig.PlayerType(parsed_config["player_type"]),
        self.color = PlayerConfig.PlayerColor(parsed_config.get("player_color", None))

    def to_game_player(self, color: "PlayerConfig.PlayerColor" = None, seed: int = None, simulation_depth: int = 5, simulation_count: int = 500) -> Player:
        if color is not None:
            color = self.color
        match self.type:
            case PlayerConfig.PlayerType.USER:
                return UserPlayer(color)
            case PlayerConfig.PlayerType.SIMPLE_HEURISTIC:
                return SimpleHeuristicPlayer(color)
            case PlayerConfig.PlayerType.HEURISTIC:
                return AlphaBetaHeuristicPlayer(color, simulation_depth)
            case PlayerConfig.PlayerType.RANDOM:
                return RandomPlayer(color, seed)
            case PlayerConfig.PlayerType.MCTS:
                return UCTPlayer(color, seed, simulation_count, MCTSVersion.UCT)
            case PlayerConfig.PlayerType.MCTS_UCB:
                return UCTPlayer(color, seed, simulation_count, MCTSVersion.UCB1_TUNED)
            case PlayerConfig.PlayerType.MCTS_GROUPING:
                return UCTPlayer(color, seed, simulation_count, MCTSVersion.UCT_GROUPING)

class ConfigModel:
    def __init__(self, parsed_config: dict) -> None:
        self.game_type = GameType(parsed_config.get("game_type", "match"))
        self.show_visualization = parsed_config.get("show_visualization", True)
        self.output_file = parsed_config.get("output_file", None)
        self.game_repetitions = parsed_config.get("game_repetitions", 1)
        self.seed = parsed_config.get("seed", None)
        self.heurstic_simulation_depth = parsed_config.get("heurstic_simulation_depth", 10)
        self.mcts_simulation_count = parsed_config.get("mcts_simulation_count", 500)

        self.__players = [PlayerConfig(player) for player in parsed_config["players"]]
        self.__ignore_player_colors = (self.game_type == GameType.TOURNAMENT
                                    or any(player.color is None for player in self.__players)
                                    or len(self.__players == 2) and self.__players[0].color == self.__players[1].color)

    def get_matches(self) -> list[tuple[Player, Player]]:
        if len(self.__players) <= 2:
            raise Exception('Invalid configration - requires at least 2 players')
        rand = Random(self.seed)
        games: list[tuple[Player, Player]] = []
        if self.game_type == GameType.MATCH:
            if len(self.__players) != 2:
                raise Exception('Invalid configration - match requires exactly 2 players')
            if self.__ignore_player_colors:
                first_color = PlayerConfig.PlayerColor.BLACK
                second_color = PlayerConfig.PlayerColor.WHITE
            games.append([self.__get_game_player(0, first_color), self.__get_game_player(0, second_color)])
        else:
            for i in enumerate(self.__players):
                for j in enumerate(self.__players[i,:]):
                    colors = [PlayerConfig.PlayerColor.BLACK, PlayerConfig.PlayerColor.WHITE]
                    games.append([self.__get_game_player(i, colors[0]), self.__get_game_player(j, colors[1])])
                    games.append([self.__get_game_player(i, colors[1]), self.__get_game_player(j, colors[0])])
                    if rand.randint(0, 1) == 1: # Random for last game
                        colors.reverse()
                    games.append([self.__get_game_player(i, colors[0]), self.__get_game_player(j, colors[1])])
        return games

    def __get_game_player(self, index: int, color: PlayerConfig.PlayerColor = None) -> Player:
        return self.__players[index].to_game_player(color, self.seed, self.heurstic_simulation_depth, self.mcts_simulation_count)

    @staticmethod
    def get_from_file(file_name: str) -> "ConfigModel":
        with open(file_name, 'r', encoding='utf8') as file:
            data = json.load(file)
        return ConfigModel(data)
