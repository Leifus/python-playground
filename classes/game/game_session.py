from classes.common.game_sprite import GameSprite
from classes.configs.game_mode_config import GameModeConfig
from classes.enums.game_mode_enum import GameModeEnum
from classes.enums.gems_merge_object_color_enum import GemsMergeObjectColorEnum
from classes.enums.merge_object_size_enum import MergeObjectSizeEnum
from classes.game.gems_merge_object import GemsMergeObject
from classes.game.main_containment_box import MainContainmentBox
from classes.game.up_next_panel import UpNextPanel
import config.game_mode_configs as game_mode_configs
from config import pygame, pymunk, random

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
        self.space_debug_draw = False

        self.total_time_lapsed = 0
        self.is_running = False
        self.time_per_spawn = 1000
        self.time_till_next_spawn = 0

        self.containment_box: MainContainmentBox = None
        self.up_next_panel: UpNextPanel = None

        self.sprites_group = pygame.sprite.Group()
        self.merge_objects_group = pygame.sprite.Group()

        self.collision_type_multiplier = 100
        self.shapes_to_remove: list[pymunk.Shape] = []
        self.shapes_to_create = []

        self.mouse_position: pygame.Vector2 = None

        self.setup_players()
        self.setup_containment_box()
        self.setup_up_next_panel()
        self.setup_collision_handlers()

        new_merge_object = self.create_gem_merge_object(position=self.up_next_panel.position)
        self.up_next_panel.up_next.append(new_merge_object)

    def setup_collision_handlers(self):
        for gem_color_enum in GemsMergeObjectColorEnum:
            for size_enum in MergeObjectSizeEnum:
                collision_type = (gem_color_enum.value * self.collision_type_multiplier) + size_enum.value
                handler = self.space.add_collision_handler(collision_type, collision_type)
                handler.pre_solve = self.on_gem_collide_pre_solve

    def on_gem_collide_pre_solve(self, arbiter: pymunk.Arbiter, space, data):
        if arbiter.is_first_contact: # and len(arbiter.shapes) >= 3: # Merge
            col_type = arbiter.shapes[0].collision_type
            gem_color_collision_type = int(col_type / self.collision_type_multiplier)
            gem_color_enum = GemsMergeObjectColorEnum(gem_color_collision_type)
            size_collision_type = col_type - (gem_color_enum.value * self.collision_type_multiplier)
            size_enum = MergeObjectSizeEnum(size_collision_type)

            if size_enum in [MergeObjectSizeEnum.Small, MergeObjectSizeEnum.Medium]:
                new_size_enum = MergeObjectSizeEnum(size_enum.value+1)
                print('Merge Up!', gem_color_enum.name, new_size_enum.name)
                position = arbiter.contact_point_set.points[0].point_a
                self.shapes_to_create.append((gem_color_enum, new_size_enum, position))
            elif size_enum == MergeObjectSizeEnum.Large:
                print('Final Merge', gem_color_enum.name, size_enum.name)
            
            for shape in arbiter.shapes:
                self.shapes_to_remove.append(shape)

        return True

    def setup_containment_box(self):
        size = (400, 600)
        position = (self.rect.width/2, self.rect.height/2)
        self.containment_box = MainContainmentBox(size, position)
        self.sprites_group.add(self.containment_box)
        self.space.add(self.containment_box.body, *self.containment_box.shapes)

    def setup_up_next_panel(self):
        size = (60, 60)
        position = (self.containment_box.rect.left + self.containment_box.rect.width/2, self.containment_box.rect.top + self.containment_box.wall_thickness + size[1]/2)
        self.up_next_panel = UpNextPanel(size, position)
        self.sprites_group.add(self.up_next_panel)

    def setup_players(self):
        pass
        
    def on_event(self, event: pygame.event.Event):
        if not self.is_running:
            return
        
        if event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            mouse_x, mouse_y = event.pos
            self.mouse_position = event.pos
            # self.mouse_position = pygame.Vector2(mouse_x - self.containment_box.rect.left, mouse_y - self.containment_box.rect.top)

        # if event.type == pygame.MOUSEBUTTONUP and event.button[0]:
        #     self.
        
    def create_gem_merge_object(self, position, gem_color: GemsMergeObjectColorEnum = None, size: MergeObjectSizeEnum = None) -> GemsMergeObject:
        if gem_color is None:
            gem_colors = []
            for gem_color in GemsMergeObjectColorEnum:
                gem_colors.append(gem_color)
            gem_color = gem_colors[random.randint(0, len(gem_colors)-1)]
        
        if size is None:
            sizes = [MergeObjectSizeEnum.Large, MergeObjectSizeEnum.Medium, MergeObjectSizeEnum.Small]
            size = sizes[random.randint(0, len(sizes)-1)]
        
        merge_object = GemsMergeObject(gem_color, size)
        merge_object.set_position(position)
        return merge_object
    
    
    # def spawn_gem_merge_object(self, gem_color: GemsMergeObjectColorEnum = None, size: MergeObjectSizeEnum = None, position=None):
    #     # Spawn new merge object
    #     if gem_color is None:
    #         gem_colors = []
    #         for gem_color in GemsMergeObjectColorEnum:
    #             gem_colors.append(gem_color)
    #         gem_color = gem_colors[random.randint(0, len(gem_colors)-1)]
        
    #     if size is None:
    #         sizes = [MergeObjectSizeEnum.Large, MergeObjectSizeEnum.Medium, MergeObjectSizeEnum.Small]
    #         size = sizes[random.randint(0, len(sizes)-1)]
        
    #     merge_object = GemsMergeObject(gem_color, size)

    #     if position is None:
    #         container_min_x = self.containment_box.rect.left + self.containment_box.wall_thickness
    #         container_max_x = self.containment_box.rect.right - self.containment_box.wall_thickness
    #         rand_x_pos = random.uniform(container_min_x + merge_object.rect.width/2, container_max_x - merge_object.rect.width/2)
    #         y_pos = self.containment_box.rect.top + self.containment_box.wall_thickness + merge_object.rect.height/2
    #         position = (rand_x_pos, y_pos)
            
    #     merge_object.set_position(position)
    #     self.space.add(merge_object.body, *merge_object.shapes)
    #     self.merge_objects_group.add(merge_object)
    
    def move_up_next_panel(self):
        if not self.mouse_position or not self.up_next_panel.follow_mouse:
            return
        
        min_x = self.containment_box.wall_thickness + self.up_next_panel.rect.width/2
        max_x = self.containment_box.rect.width - self.containment_box.wall_thickness - self.up_next_panel.rect.width/2
        mouse_x = self.mouse_position.x

        x = mouse_x
        if x < min_x:
            x = min_x
        elif x > max_x:
            x = max_x

        position = (self.containment_box.rect.left + x, self.up_next_panel.position[1])
        self.up_next_panel.set_position(position)
        
    def update(self, *args, **kwargs):
        if not self.is_running:
            return
        
        if len(self.shapes_to_remove) > 0:
            for shape in self.shapes_to_remove:
                self.space.remove(shape.body, shape)
                shape.sprite.kill()

            self.shapes_to_remove.clear()
        
        if len(self.shapes_to_create) > 0:
            for gem_color, size, position in self.shapes_to_create:
                merge_object = GemsMergeObject(gem_color, size)
                merge_object.position = position
                self.merge_objects_group.add(merge_object)
                self.space.add(merge_object.body, *merge_object.shapes)
            
            self.shapes_to_create.clear()
        
        for _ in range(self.game_config.space_config.dt_steps):
            self.space.step(self.game_config.space_config.dt / self.game_config.space_config.dt_steps)
        
        self.total_time_lapsed = pygame.time.get_ticks()
        self.clock.tick(self.game_config.time_config.fps)
        time_lapsed = self.clock.get_time()

        self.move_up_next_panel()

        # self.time_till_next_spawn -= time_lapsed
        # if self.time_till_next_spawn <= 0:
        #     self.spawn_gem_merge_object()
                # # Set spawn timer
                # self.time_till_next_spawn = self.time_per_spawn

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

    def draw_player_aim(self):
        pos_a = self.up_next_panel.position
        pos_b = self.mouse_position
        pygame.draw.line(self.surface, 'black', pos_a, pos_b, 2)

    def draw(self, surface):
        self.surface.fill((0,0,0,0))

        if self.space_debug_draw:
            self.space.debug_draw(pymunk.pygame_util.DrawOptions(self.surface))

        self.sprites_group.draw(self.surface)
        self.merge_objects_group.draw(self.surface)
        self.draw_player_aim()

        self.image = self.surface
        return super().draw(surface)