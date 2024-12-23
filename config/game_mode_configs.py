from classes.game_mode_config import GameModeConfig
from classes.game_mode_enum import GameModeEnum
from classes.game_space_config import GameSpaceConfig
from classes.game_time_config import GameTimeConfig

game_modes = dict()

# Billiards
time_config = GameTimeConfig(60)
space_config = GameSpaceConfig(1.0 / 60, 3, 10, (0, 0), 0.23, 0.1)
config = GameModeConfig(GameModeEnum.Billiards, time_config, space_config)
game_modes[config.identifier] = config

# Snooker
time_config = GameTimeConfig(60)
space_config = GameSpaceConfig(1.0 / 60, 3, 10, (0, 0), 0.23, 0.1)
config = GameModeConfig(GameModeEnum.Snooker, time_config, space_config)
game_modes[config.identifier] = config