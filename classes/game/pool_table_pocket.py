from classes.common.game_sprite import GameSprite
from classes.enums.collision_type_enum import CollisionTypeEnum
from config import pool_balls_config, pool_table_config, pygame, pymunk
from classes.enums.draw_mode_enum import DrawModeEnum
from globals import media_manager

class PoolTablePocket(GameSprite):
    def __init__(self, position, radius):
        super(PoolTablePocket, self).__init__()

        self.draw_mode = pool_table_config.pool_table_pocket_draw_mode
        self.radius = radius
        self.pocket_RAW_color = pool_table_config.pool_table_pocket_DM_RAW_color
        self.WIREFRAME_outline_width = pool_table_config.pool_table_pocket_DM_WIREFRAME_outline_width
        self.pocket_RICH_media = pool_table_config.pool_table_pocket_DM_RICH_media

        self.position = position

        self.image: pygame.Surface | None = None
        self.orig_image: pygame.Surface | None = None
        self.mask: pygame.mask.Mask | None = None
        self.rect: pygame.Rect | None = None

        self.body = None
        self.shape = None

        self.setup_visuals()
        self.construct_physical_body()
        self.redraw()

    def redraw(self):
        orig_rect = self.orig_image.get_rect()
        image_radius = self.radius*2
        if self.image is None or orig_rect.width != image_radius:
            self.image = pygame.transform.scale(self.orig_image, (image_radius, image_radius))
            self.rect = self.image.get_rect(center=self.position)
            self.mask = pygame.mask.from_surface(self.image)

        if self.mask is None:
            self.mask = pygame.mask.from_surface(self.image)

    def setup_visuals(self):
        if self.draw_mode in DrawModeEnum.Wireframe | DrawModeEnum.Raw:
            outline_width = 0
            if self.draw_mode in DrawModeEnum.Wireframe:
                outline_width = self.WIREFRAME_outline_width

            self.orig_image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(self.orig_image, self.pocket_RAW_color, (self.radius, self.radius), self.radius, outline_width)
        elif self.draw_mode in DrawModeEnum.Rich:
            rich_surface = media_manager.get(self.pocket_RICH_media, convert_alpha=True)
            if not rich_surface:
                print('No pocket img', self.pocket_RICH_media)
                return
            
            self.orig_image = pygame.transform.scale(rich_surface, (self.radius*2, self.radius*2))

    def construct_physical_body(self):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = self.position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.sensor = True
        self.shape.collision_type = CollisionTypeEnum.COLLISION_TYPE_POOL_TABLE_POCKET.value # + body_iter
