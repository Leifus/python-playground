from classes.game_time_config import GameTimeConfig
from classes.player import Player
from config import pygame, game_mode_time_config
from classes.game_mode_enum import GameModeEnum

class GameSession():
    def __init__(self, game_id, game_mode: GameModeEnum):
        self.game_id: str = game_id
        self.game_mode: GameModeEnum = game_mode
        self.players = []
        self.active_player: Player = None
        self.clock = pygame.time.Clock()
        self.time_lapsed = 0
        self.time_config: GameTimeConfig = game_mode_time_config.game_mode_times[self.game_mode]
        self.is_running = False

        self.setup()

    def setup(self):
        player_count = 1
        if self.game_mode in GameModeEnum.BILLIARDS | GameModeEnum.SNOOKER:
            player_count = 2

        for i in range(player_count):
            name = f'Player {i+1}'
            player = Player(name)
            self.players.append(player)

        self.active_player = self.players[0]
        
        pygame.display.set_caption(self.game_id)
        # pygame.display.set_caption(f"Pool Table: {round(self.clock.get_fps(),3)} fps | {round(time_lapsed / 1000)} secs")

    def update(self):
        self.time_lapsed = pygame.time.get_ticks()
        self.clock.tick(self.time_config.fps)
