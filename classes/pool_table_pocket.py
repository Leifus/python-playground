from classes.draw_mode import DrawMode
from config import pool_balls_config, pool_table_config, pygame, pymunk
from classes.media_manager import MediaManager

class PoolTablePocket():
    def __init__(self, radius, color, position, media_manager: MediaManager):
        self.draw_mode = pool_table_config.pool_table_pocket_draw_mode
        self.radius = radius

        self.surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=position)

        self.media_manager = media_manager
        self.position = position
        self.color = color

        self.body = None
        self.shape = None
        self.rich_pocket_surface = None
        self.rich_pocket_rect = None

    def setup_visual(self):
        if self.draw_mode in DrawMode.WIREFRAME | DrawMode.RAW:
            outline_width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                outline_width = pool_table_config.pool_table_pocket_draw_mode_wireframe_thickness

            pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius, outline_width)
        elif self.draw_mode in DrawMode.RICH:
            media_path = pool_table_config.pool_table_pocket_DM_RICH_media
            rich_surface = self.media_manager.get(media_path, convert_alpha=True)
            if not rich_surface:
                print('No pocket img', media_path)
                return
            
            self.rich_pocket_surface = pygame.transform.scale(rich_surface, (self.radius*2, self.radius*2))
            self.rich_pocket_rect = self.rich_pocket_surface.get_rect(center=self.position)



    def setup_physical(self, space: pymunk.Space, body_iter):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = self.position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.sensor = True
        self.shape.collision_type = pool_balls_config.COLLISION_TYPE_POOL_TABLE_POCKET + body_iter
        space.add(self.body, self.shape)

    def on_init(self, space: pymunk.Space, body_iter):
        self.setup_visual()
        self.setup_physical(space, body_iter)

    def update(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)

        if self.draw_mode in DrawMode.RICH:
            surface.blit(self.rich_pocket_surface, self.rich_pocket_rect)