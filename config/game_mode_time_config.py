from classes.game_mode_enum import GameModeEnum
from classes.game_time_config import GameTimeConfig

game_mode_times = dict()
game_mode_times[GameModeEnum.Billiards] = GameTimeConfig(60)
game_mode_times[GameModeEnum.Snooker] = GameTimeConfig(60)
game_mode_times[GameModeEnum.CirclePool] = GameTimeConfig(60)

#SPACE , 1.0 / 60, 3

# game_modes = 