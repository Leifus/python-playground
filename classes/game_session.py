from classes.game_mode_config import GameModeConfig
from classes.game_time_config import GameTimeConfig
from classes.player import Player
from config import pygame, game_mode_time_config, Dict
from classes.game_mode_enum import GameModeEnum
import config.game_mode_configs as game_mode_configs

class GameSession():
    def __init__(self, game_id, game_mode: GameModeEnum):
        self.game_id: str = game_id
        self.game_mode: GameModeEnum = game_mode
        self.game_mode_config: GameModeConfig = game_mode_configs.game_modes[game_mode.name]
        self.players: Dict[str, Player] = dict()
        self.active_player: Player = None
        self.clock = pygame.time.Clock()
        self.time_lapsed = 0
        self.time_config: GameTimeConfig = game_mode_time_config.game_mode_times[self.game_mode]
        self.is_running = False

        self.setup_players()

    def setup_players(self):
        player_count = 1
        if self.game_mode in GameModeEnum.BILLIARDS | GameModeEnum.SNOOKER:
            player_count = 2

        for i in range(player_count):
            name = f'Player {i+1}'
            identifier = f'{i}'
            player = Player(identifier, name)
            self.players[identifier] = player

    def get_first_player(self) -> Player:
        first_player_id = list(self.players.keys())[0]
        return self.players[first_player_id]


    def set_active_player(self, player: Player):
        self.active_player = player
        self.active_player.is_playing = True
        
    def on_event(self, event: pygame.event.Event):
        if not self.is_running:
            return
        
        if event.type not in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            return
        
        mouse_pos = event.pos
        
    def move_to_next_player(self) -> Player:
        player_ids = list(self.players.keys())
        current_player_idx = -1
        if self.active_player is not None:
            current_player_idx = player_ids.index(self.active_player.identifier)

        next_player_idx = current_player_idx + 1
        if next_player_idx >= len(player_ids):
            next_player_idx = 0

        if next_player_idx == current_player_idx:
            return self.active_player
        
        self.active_player.is_playing = False
        self.active_player.can_take_shot = False

        next_player_id = player_ids[next_player_idx]
        next_player = self.players[next_player_id]

        self.set_active_player(next_player)
        
        return self.active_player

    def update(self):
        self.time_lapsed = pygame.time.get_ticks()
        self.clock.tick(self.time_config.fps)

        #TODO: Move this out of here
        pygame.display.set_caption(f'{self.game_id} ({round(self.clock.get_fps(),3)} fps) | {round(self.time_lapsed / 1000)} secs')
