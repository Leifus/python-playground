from classes.game_time_config import GameTimeConfig
from classes.player import Player
from config import pygame, game_mode_time_config
from classes.game_mode_enum import GameModeEnum

class GameSession():
    def __init__(self, game_id, game_mode: GameModeEnum):
        self.game_id: str = game_id
        self.game_mode: GameModeEnum = game_mode
        self.players = []
        self.active_player_idx = -1
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

        self.active_player_idx = 0
        self.players[self.active_player_idx].is_playing = True
        
    def move_to_next_player(self):
        active_player_idx = self.active_player_idx + 1
        if active_player_idx >= len(self.players):
            active_player_idx = 0

        if active_player_idx != self.active_player_idx:
            self.players[self.active_player_idx].is_playing = False

        self.active_player_idx = active_player_idx
        self.players[self.active_player_idx].is_playing = True



    def update(self):
        self.time_lapsed = pygame.time.get_ticks()
        self.clock.tick(self.time_config.fps)

        pygame.display.set_caption(f'{self.game_id} ({round(self.clock.get_fps(),3)} fps) | {round(self.time_lapsed / 1000)} secs')
