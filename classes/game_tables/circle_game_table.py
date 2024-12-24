from classes.draw_mode_enum import DrawModeEnum
from classes.game_space_config import GameSpaceConfig
from classes.game_tables.game_table import GameTable
from classes.light_source import LightSource
from config import pool_table_config, pygame
from globals import media_manager

class CircleGameTable(GameTable):
    def __init__(self, radius, position, space_config: GameSpaceConfig, draw_mode: DrawModeEnum):
        size = (radius*2, radius*2)
        super(CircleGameTable, self).__init__(size=size, position=position, space_config=space_config, draw_mode=draw_mode)
        
        self.radius = radius
        self.rich_media_path = pool_table_config.pool_table_DM_RICH_media
        self.circle_image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.circle_image.get_rect(center=self.position)
        pygame.draw.circle(self.circle_image, (0,0,0), (self.radius, self.radius), self.radius)
        self.mask = pygame.mask.from_surface(self.circle_image)

        self.setup_visuals()
        self.redraw()

    def redraw(self):
        super().redraw(mask_surface=self.circle_image)
        
        # if self.draw_mode in DrawModeEnum.Raw | DrawModeEnum.Wireframe:
        #     color = pygame.Color('darkorange1')
        #     pygame.draw.circle(self.circle_image, color, (self.radius, self.radius), self.radius)
        if self.draw_mode in DrawModeEnum.Rich:
            # Table
            self.image = self.mask.to_surface(unsetcolor=None, setsurface=self.image)

    def setup_visuals(self):
        if self.draw_mode in DrawModeEnum.Raw | DrawModeEnum.Wireframe:
            # Table
            self.orig_image = self.circle_image
        elif self.draw_mode in DrawModeEnum.Rich:
            # Table
            self.orig_image = media_manager.get(self.rich_media_path, convert_alpha=True)
            if not self.orig_image:
                print('CircleGameTable: No table img', self.rich_media_path)
                return
