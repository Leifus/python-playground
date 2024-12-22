from config import pool_balls_config, pool_table_config, pygame, pymunk
from classes.media_manager import MediaManager
from classes.draw_mode_enum import DrawModeEnum

class PoolTablePocket():
    def __init__(self, position, media_manager: MediaManager):
        self.draw_mode = pool_table_config.pool_table_pocket_draw_mode
        self.radius = pool_table_config.pool_table_pocket_radius
        self.pocket_RAW_color = pool_table_config.pool_table_pocket_DM_RAW_color
        self.WIREFRAME_outline_width = pool_table_config.pool_table_pocket_DM_WIREFRAME_outline_width
        self.pocket_RICH_media = pool_table_config.pool_table_pocket_DM_RICH_media

        self.surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=position)
        self.pocket_surface = self.surface.copy()
        self.pocket_RICH_surface = None

        self.media_manager = media_manager
        self.position = position

        self.body = None
        self.shape = None

    def setup_visual_presentation(self):
        if self.draw_mode in DrawModeEnum.WIREFRAME | DrawModeEnum.RAW:
            outline_width = 0
            if self.draw_mode in DrawModeEnum.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            pygame.draw.circle(self.pocket_surface, self.pocket_RAW_color, (self.radius, self.radius), self.radius, outline_width)
        elif self.draw_mode in DrawModeEnum.RICH:
            rich_surface = self.media_manager.get(self.pocket_RICH_media, convert_alpha=True)
            if not rich_surface:
                print('No pocket img', self.pocket_RICH_media)
                return
            
            self.pocket_RICH_surface = pygame.transform.scale(rich_surface, (self.radius*2, self.radius*2))
            self.pocket_surface.blit(self.pocket_RICH_surface, (0, 0))

    def setup_physical_space(self, space: pymunk.Space, body_iter):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = self.position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.sensor = True
        self.shape.collision_type = pool_balls_config.COLLISION_TYPE_POOL_TABLE_POCKET# + body_iter
        space.add(self.body, self.shape)

    def on_init(self, space: pymunk.Space, body_iter):
        self.setup_visual_presentation()
        self.setup_physical_space(space, body_iter)

    def update(self):
        pass

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))
        
        self.surface.blit(self.pocket_surface, (0,0))

        surface.blit(self.surface, self.rect)