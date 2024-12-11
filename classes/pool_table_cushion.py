from config import pool_balls_config, pool_table_config, pygame, pymunk
from classes.draw_mode import DrawMode
from classes.media_manager import MediaManager

class PoolTableCushion():
    def __init__(self, size, position, poly_points, media_manager: MediaManager):
        self.draw_mode = pool_table_config.pool_table_cushion_draw_mode
        self.elasticity = pool_table_config.pool_table_cushion_elasticity
        self.friction = pool_table_config.pool_table_cushion_friction
        self.raw_color = pool_table_config.pool_table_cushion_DM_RAW_color

        self.media_manager = media_manager
        self.size = size
        self.position = position

        if poly_points is not None:
            self.poly_points = poly_points
        else:   # rectangle
            self.poly_points = [(0,0), (self.size[0], 0), (self.size[0], self.size[1]), (0, self.size[1])]
        
        self.body = None
        self.shape = None
        self.raw_surface = None
        self.raw_rect = None
        self.rich_surface = None
        self.rich_rect = None

    def on_init(self, space: pymunk.Space, body_iter):
        self.raw_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.raw_rect = self.raw_surface.get_rect(center=self.position)

        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            outline_width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                outline_width = pool_table_config.pool_table_cushion_draw_mode_wireframe_thickness

                for _ in self.poly_points:
                    pygame.draw.circle(self.raw_surface, (0,0,0), _, 2)

            pygame.draw.polygon(self.raw_surface, self.raw_color, self.poly_points, outline_width)

            if self.draw_mode in DrawMode.WIREFRAME:
                for _ in self.poly_points:
                    pygame.draw.circle(self.raw_surface, (0,0,0), _, 3)
        elif self.draw_mode in DrawMode.RICH:
            media_path = pool_table_config.pool_table_cushion_DM_RICH_media
            rich_surface = self.media_manager.get(media_path, convert_alpha=True)
            if not rich_surface:
                print('No cushion img')
                return
            
            self.rich_surface = pygame.transform.scale(rich_surface, self.size)
            self.rich_rect = self.rich_surface.get_rect(center=self.position)





        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (self.position[0] - (self.raw_rect.width/2), self.position[1] - (self.raw_rect.height/2))
        self.shape = pymunk.Poly(self.body, self.poly_points)
        self.shape.collision_type = pool_balls_config.COLLISION_TYPE_POOL_TABLE_CUSHION + body_iter
        self.shape.elasticity = pool_table_config.pool_table_cushion_elasticity
        self.shape.friction = pool_table_config.pool_table_cushion_friction
        space.add(self.body, self.shape)


        

    def update(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.raw_surface, self.raw_rect)

        if self.draw_mode in DrawMode.RICH:
            surface.blit(self.rich_surface, self.rich_rect)
