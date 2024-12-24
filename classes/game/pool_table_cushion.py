from classes.common.game_sprite import GameSprite
from config import pool_balls_config, pool_table_config, pygame, pymunk
from classes.enums.draw_mode_enum import DrawModeEnum
from classes.common.helper_methods import draw_poly_points
from globals import media_manager

class PoolTableCushion(GameSprite):
    def __init__(self, size, position, poly_points):
        super(PoolTableCushion, self).__init__()
        
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

        self.size = size
        self.position = position

        if poly_points is not None:
            self.poly_points = poly_points
        else:   # rectangle
            self.poly_points = [(0,0), (self.size[0], 0), (self.size[0], self.size[1]), (0, self.size[1])]
        
        self.image: pygame.Surface | None = None
        self.orig_image: pygame.Surface | None = None
        self.mask: pygame.mask.Mask | None = None
        self.rect: pygame.Rect | None = None
        
        self.body = None
        self.shape = None

        self.setup_visuals()
        self.setup_physical_space()
        self.redraw()

    def redraw(self):
        self.image = pygame.transform.scale(self.orig_image, self.size)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def setup_visuals(self):
        if self.draw_mode in DrawModeEnum.Raw | DrawModeEnum.Wireframe:
            self.orig_image = pygame.Surface(self.size, pygame.SRCALPHA)
            outline_width = 0
            if self.draw_mode in DrawModeEnum.Wireframe:
                outline_width = self.WIREFRAME_outline_width

            pygame.draw.polygon(self.orig_image, self.cushion_RAW_color, self.poly_points, outline_width)

            if self.draw_mode in DrawModeEnum.Wireframe:
                color = (0,0,0)
                draw_poly_points(self.orig_image, self.poly_points, color, self.WIREFRAME_poly_point_radius)
        if self.draw_mode in DrawModeEnum.Rich:
            self.orig_image = media_manager.get(self.cushion_RICH_media, convert_alpha=True)
            if not self.orig_image:
                print('No cushion img', self.cushion_RICH_media)
    
    def setup_physical_space(self):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (self.position[0] - (self.size[0]/2), self.position[1] - (self.size[1]/2))
        self.shape = pymunk.Poly(self.body, self.poly_points)
        self.shape.collision_type = self.shape_collision_type# + body_iter
        self.shape.elasticity = self.shape_elasticity
        self.shape.friction = self.shape_friction
        