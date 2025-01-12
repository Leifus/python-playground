from classes.configs.game_mode_config import GameModeConfig
from classes.enums.game_mode_enum import GameModeEnum
from classes.configs.game_space_config import GameSpaceConfig
from classes.configs.game_time_config import GameTimeConfig

game_modes = dict()

# Default
time_config = GameTimeConfig(60)
space_config = GameSpaceConfig(1.0 / 60, 3, 10, (0, 980), 0.98, 0.1)
config = GameModeConfig(GameModeEnum.Default, time_config, space_config)
game_modes[config.identifier] = config
