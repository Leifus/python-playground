from classes.common.game_sprite import GameSprite
from classes.configs.game_mode_config import GameModeConfig
from classes.configs.game_time_config import GameTimeConfig
from classes.configs.sprite_animation_config import SpriteAnimationConfig
from classes.enums.game_mode_enum import GameModeEnum
from classes.enums.gems_merge_object_color_enum import GemsMergeObjectColorEnum
from classes.enums.merge_object_size_enum import MergeObjectSizeEnum
from classes.game.gems_merge_object import GemsMergeObject
from classes.game.main_containment_box import MainContainmentBox
from classes.game.merge_object import MergeObject
import config.game_mode_configs as game_mode_configs
from config import pygame, pymunk, Dict, random

class GameSession(GameSprite):
    def __init__(self, display_size, game_id, game_mode: GameModeEnum):
        super(GameSession, self).__init__()

        self.game_id: str = game_id
        self.game_mode: GameModeEnum = game_mode
        self.game_config: GameModeConfig = game_mode_configs.game_modes[game_mode.name]
        
        self.surface = pygame.Surface(display_size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

        self.clock = pygame.time.Clock()
        self.space = pymunk.Space()
        self.space.gravity = self.game_config.space_config.gravity
        self.space.damping = self.game_config.space_config.damping
        self.space.iterations = self.game_config.space_config.iterations
        self.space.sleep_time_threshold = self.game_config.space_config.sleep_time_threshold
        self.space_debug_draw = True

        self.total_time_lapsed = 0
        self.is_running = False
        self.time_per_spawn = 3000
        self.time_till_next_spawn = 0

        self.containment_box: MainContainmentBox = None

        self.sprites_group = pygame.sprite.Group()
        self.merge_objects_group = pygame.sprite.Group()

        self.setup_players()
        self.setup_containment_box()

    def setup_containment_box(self):
        size = (400, 600)
        position = (self.rect.width/2 - size[0]/2, self.rect.height/2 - size[1]/2)
        self.containment_box = MainContainmentBox(size, position)
        self.sprites_group.add(self.containment_box)
        self.space.add(self.containment_box.body, *self.containment_box.shapes)

    def setup_players(self):
        pass
        
    def on_event(self, event: pygame.event.Event):
        if not self.is_running:
            return
        
    def spawn_merge_object(self):
        # Spawn new merge object
        gem_colors = []
        for gem_color in GemsMergeObjectColorEnum:
            gem_colors.append(gem_color)
        rand_gem_color = random.randint(0, len(gem_colors)-1)
        
        size = MergeObjectSizeEnum.Large
        merge_object = GemsMergeObject(rand_gem_color, size)
        self.merge_objects_group.add(merge_object)
        
        # Set spawn timer
        self.time_till_next_spawn = self.time_per_spawn
        
    def update(self, *args, **kwargs):
        if not self.is_running:
            return
        
        for _ in range(self.game_config.space_config.dt_steps):
            self.space.step(self.game_config.space_config.dt / self.game_config.space_config.dt_steps)
        
        self.total_time_lapsed = pygame.time.get_ticks()
        self.clock.tick(self.game_config.time_config.fps)
        time_lapsed = self.clock.get_time()

        self.time_till_next_spawn -= time_lapsed
        if self.time_till_next_spawn <= 0:
            self.spawn_merge_object()

        self.sprites_group.update(time_lapsed)
        self.merge_objects_group.update(time_lapsed)

        #TODO: Move this out of here
        pygame.display.set_caption(f'{self.game_id} ({round(self.clock.get_fps(),3)} fps) | {round(self.total_time_lapsed / 1000)} secs')
        
        return super().update(*args, **kwargs)

    def kill(self):
        self.is_running = False    #Force this for now
        
        self.sprites_group.empty() # Not reqd meethinks
        self.merge_objects_group.empty() # Not reqd meethinks
        print('ending session')

    def draw(self, surface):
        if self.space_debug_draw:
            self.space.debug_draw(pymunk.pygame_util.DrawOptions(self.surface))

        # self.sprites_group.draw(self.surface)
        self.merge_objects_group.draw(self.surface)


        self.image = self.surface
        return super().draw(surface)