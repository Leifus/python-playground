from classes.game_mode_enum import GameModeEnum
from classes.game_space_config import GameSpaceConfig
from classes.game_time_config import GameTimeConfig


class GameModeConfig():
    def __init__(self, game_mode: GameModeEnum, time_config, space_config):
        self.game_mode: GameModeEnum = game_mode
        self.identifier: str = game_mode.name
        self.time_config: GameTimeConfig = time_config
        self.space_config: GameSpaceConfig = space_config