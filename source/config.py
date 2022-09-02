from enum import Enum
import json
from random import Random
from heuristic_player import AlphaBetaHeuristicPlayer, SimpleHeuristicPlayer
from othello_utils import MCTSVersion, PlayerColor
from match import Match
from player import Player, RandomPlayer, UserPlayer
from mcts_player import MCTSPlayer

class GameType(Enum):
    '''
    Type of the game - match for single game or tournament for set of games.
    '''
    MATCH = "match"
    TOURNAMENT = "tournament"

class PlayerConfig():
    '''
    Player's configuration - information about color and used algorithm.
    '''
    class PlayerType(Enum):
        '''
        Type of the player - algorithm to use for bot or \"user\" for real player.
        '''
        USER = "user"
        SIMPLE_HEURISTIC = "simple_heuristic"
        HEURISTIC = "heuristic"
        RANDOM = "random"
        MCTS = "mcts_uct"
        MCTS_UCB = "mcts_ucb1"
        MCTS_GROUPING = "mcts_grouping"

    class PlayerColor(Enum):
        '''
        Color of player's pawns.
        '''
        BLACK = "black"
        WHITE = "white"

    def __init__(self, parsed_config: dict) -> None:
        self.type = PlayerConfig.PlayerType(parsed_config["player_type"])
        self.color = PlayerConfig.PlayerColor(parsed_config["player_color"]) if "player_color" in parsed_config else None

    def to_game_player(self, color: "PlayerConfig.PlayerColor" = None, seed: int = None, simulation_depth: int = 5, simulation_count: int = 500) -> Player:
        '''
        Returns instance of class derived from \"Player\", created based on configuraiton.
        '''
        if color is None:
            color = self.color
        player_color = PlayerColor[color.name]
        match self.type:
            case PlayerConfig.PlayerType.USER:
                return UserPlayer(player_color)
            case PlayerConfig.PlayerType.SIMPLE_HEURISTIC:
                return SimpleHeuristicPlayer(player_color)
            case PlayerConfig.PlayerType.HEURISTIC:
                return AlphaBetaHeuristicPlayer(player_color, simulation_depth)
            case PlayerConfig.PlayerType.RANDOM:
                return RandomPlayer(player_color, seed)
            case PlayerConfig.PlayerType.MCTS:
                return MCTSPlayer(player_color, seed, simulation_count, MCTSVersion.UCT)
            case PlayerConfig.PlayerType.MCTS_UCB:
                return MCTSPlayer(player_color, seed, simulation_count, MCTSVersion.UCB1_TUNED)
            case PlayerConfig.PlayerType.MCTS_GROUPING:
                return MCTSPlayer(player_color, seed, simulation_count, MCTSVersion.UCT_GROUPING)

class ConfigModel:
    '''
    Configuration for Othello game. Model for \"config.json\".
    '''
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
                                    or (len(self.__players) == 2 and self.__players[0].color == self.__players[1].color))

    def get_matches(self) -> list[Match]:
        '''
        Returns list of all matches that will should be played according to configuration.
        '''
        if len(self.__players) < 2:
            raise Exception('Invalid configration - requires at least 2 players')
        matches: list[Match] = []
        seeds = Random(self.seed).sample(range(1000000000), self.game_repetitions)
        for seed in seeds:
            rand = Random(seed)
            if self.game_type == GameType.MATCH:
                if len(self.__players) != 2:
                    raise Exception('Invalid configration - match requires exactly 2 players')
                first_color = PlayerConfig.PlayerColor.BLACK if self.__ignore_player_colors else None
                second_color = PlayerConfig.PlayerColor.WHITE if self.__ignore_player_colors else None
                matches.append(Match([[self.__get_game_player(0, seed, first_color), self.__get_game_player(1, seed, second_color)]]))
            else:
                for i, _ in enumerate(self.__players):
                    for j in range(i + 1, len(self.__players)):
                        colors = [PlayerConfig.PlayerColor.BLACK, PlayerConfig.PlayerColor.WHITE]
                        games = []
                        games.append([self.__get_game_player(i, seed, colors[0]), self.__get_game_player(j, seed, colors[1])])
                        games.append([self.__get_game_player(i, seed, colors[1]), self.__get_game_player(j, seed, colors[0])])
                        if rand.randint(0, 1) == 1: # Random for last game
                            colors.reverse()
                        games.append([self.__get_game_player(i, seed, colors[0]), self.__get_game_player(j, seed, colors[1])])
                        matches.append(Match(games))
        return matches

    def __get_game_player(self, index: int, seed: int, color: PlayerConfig.PlayerColor) -> Player:
        return self.__players[index].to_game_player(color, seed, self.heurstic_simulation_depth, self.mcts_simulation_count)

    @staticmethod
    def get_from_file(file_name: str) -> "ConfigModel":
        '''
        Reads the configuration from files, parses it and returns the instance of \"ConfigModel\" class.
        '''
        with open(file_name, 'r', encoding='utf8') as file:
            data = json.load(file)
        return ConfigModel(data)
