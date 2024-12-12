from config import pool_balls_config, pool_table_config, pygame, pymunk
from classes.draw_mode import DrawMode
from classes.media_manager import MediaManager
from classes.__helpers__ import draw_poly_points

class PoolTableCushion():
    def __init__(self, size, position, poly_points, media_manager: MediaManager):
        self.draw_mode = pool_table_config.pool_table_cushion_draw_mode
        self.elasticity = pool_table_config.pool_table_cushion_elasticity
        self.friction = pool_table_config.pool_table_cushion_friction
        self.cushion_RAW_color = pool_table_config.pool_table_cushion_DM_RAW_color
        self.WIREFRAME_outline_width = pool_table_config.pool_table_cushion_DM_WIREFRAME_outline_width
        self.WIREFRAME_poly_point_radius = pool_table_config.pool_table_cushion_DM_WIREFRAME_poly_point_radius
        self.cushion_RICH_media = pool_table_config.pool_table_cushion_DM_RICH_media
        self.shape_collision_type = pool_balls_config.COLLISION_TYPE_POOL_TABLE_CUSHION
        self.shape_elasticity = pool_table_config.pool_table_cushion_elasticity
        self.shape_friction = pool_table_config.pool_table_cushion_friction

        self.media_manager = media_manager
        self.size = size
        self.position = position

        if poly_points is not None:
            self.poly_points = poly_points
        else:   # rectangle
            self.poly_points = [(0,0), (self.size[0], 0), (self.size[0], self.size[1]), (0, self.size[1])]
        
        self.body = None
        self.shape = None

        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)
        self.cushion_surface = self.surface.copy()
        self.cushion_RICH_surface = None

    def setup_visuals(self):
        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            outline_width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            pygame.draw.polygon(self.cushion_surface, self.cushion_RAW_color, self.poly_points, outline_width)

            if self.draw_mode in DrawMode.WIREFRAME:
                color = (0,0,0)
                draw_poly_points(self.cushion_surface, self.poly_points, color, self.WIREFRAME_poly_point_radius)
        elif self.draw_mode in DrawMode.RICH:
            media_path = self.cushion_RICH_media
            rich_surface = self.media_manager.get(media_path, convert_alpha=True)
            if not rich_surface:
                print('No cushion img')
                return
            
            self.cushion_RICH_surface = pygame.transform.scale(rich_surface, self.size)
            self.cushion_surface.blit(self.cushion_RICH_surface, (0, 0))
    
    def setup_physical_space(self, space: pymunk.Space, body_iter):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (self.position[0] - (self.rect.width/2), self.position[1] - (self.rect.height/2))
        self.shape = pymunk.Poly(self.body, self.poly_points)
        self.shape.collision_type = self.shape_collision_type + body_iter
        self.shape.elasticity = self.shape_elasticity
        self.shape.friction = self.shape_friction
        space.add(self.body, self.shape)
        
    def on_init(self, space: pymunk.Space, body_iter):
        self.setup_visuals()
        self.setup_physical_space(space, body_iter)

    def update(self):
        pass

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        self.surface.blit(self.cushion_surface, (0,0))

        surface.blit(self.surface, self.rect)