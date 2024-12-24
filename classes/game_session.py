from classes.game_mode_config import GameModeConfig
from classes.game_tables.game_table import GameTable
from classes.game_time_config import GameTimeConfig
from classes.in_game_event_enum import InGameEventEnum
from classes.player import Player
from classes.pool_table import PoolTable
from config import pygame, game_mode_time_config, OrderedDict, Dict
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

        self.queued_game_events: OrderedDict[int, InGameEventEnum] = dict()
        self.game_events_to_action: OrderedDict[int, InGameEventEnum] = dict()

        self.game_table: GameTable | None = None
        # self.pool_table: PoolTable = None
        self.pockets_group: pygame.sprite.Group = pygame.sprite.Group()

        self.setup_players()

    def has_picked_up_cue_ball(self) -> bool:
        if not self.is_running or not self.game_table or not self.game_table.cue_ball:
            return False
        
        return self.game_table.cue_ball.is_picked_up

    def setup_players(self):
        player_count = 1
        if self.game_mode in GameModeEnum.Billiards | GameModeEnum.Snooker:
            player_count = 2

        for i in range(player_count):
            name = f'Player {i+1}'
            identifier = f'{i}'
            player = Player(identifier, name)
            self.players[identifier] = player

    def get_first_player(self) -> Player:
        first_player_id = list(self.players.keys())[0]
        return self.players[first_player_id]

    def queue_game_event(self, game_event: InGameEventEnum, activation_time):
        #TODO: Check for dupe activation times
        self.queued_game_events[self.time_lapsed + activation_time] = game_event

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

    def update_queued_game_events(self):
        event_times = list(self.queued_game_events.keys())
        self.game_events_to_action.clear()

        keys_to_remove = []
        for event_time in event_times:
            if self.time_lapsed > event_time:
                keys_to_remove.append(event_time)
                self.game_events_to_action[event_time] = self.queued_game_events[event_time]
        
        if len(keys_to_remove) > 0:
            for key in keys_to_remove:
                del self.queued_game_events[key]

    def update(self):
        self.time_lapsed = pygame.time.get_ticks()
        self.clock.tick(self.time_config.fps)

        self.update_queued_game_events()

        #TODO: Move this out of here
        pygame.display.set_caption(f'{self.game_id} ({round(self.clock.get_fps(),3)} fps) | {round(self.time_lapsed / 1000)} secs')
