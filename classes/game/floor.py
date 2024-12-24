from classes.common.game_sprite import GameSprite
from config import pygame, math
import config.floor_config as floor_config
from classes.enums.draw_mode_enum import DrawModeEnum
from classes.common.helper_methods import draw_poly_points_around_rect
from globals import media_manager

class Floor(GameSprite):
    def __init__(self, size, position):
        super(Floor, self).__init__()

        self.draw_mode = floor_config.floor_draw_mode
        self.floor_RAW_colors = floor_config.floor_DM_RAW_colors
        self.floor_DM_RICH_medias = floor_config.floor_DM_RICH_medias
        self.active_floor_idx = floor_config.floor_DM_active_idx
        self.WIREFRAME_outline_width = floor_config.floor_DM_WIREFRAME_thickness
        self.WIREFRAME_poly_point_radius = floor_config.floor_DM_WIREFRAME_poly_point_radius

        self.size = size
        self.position = position

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=position)
        
        self.floor_options = None
        self.image_scale = 1.0

        self.setup_visuals()
        self.redraw()

    def redraw(self):
        self.image.fill((0,0,0,0))

        orig_image_rect = self.orig_img.get_rect()
        size = (orig_image_rect.width * self.image_scale, orig_image_rect.height * self.image_scale)
        tile_image = pygame.transform.scale(self.orig_img, size)
        tile_rect = tile_image.get_rect()

        rows = math.ceil(self.rect.height / tile_rect.height)
        cols = math.ceil(self.rect.width / tile_rect.width)

        for row in range(rows):
            for col in range(cols):
                position = (tile_rect.width * col, tile_rect.height * row)
                self.image.blit(tile_image, position)

    def update(self, selected_floor_idx, *args, **kwargs):
        if selected_floor_idx != self.active_floor_idx:
            self.active_floor_idx = selected_floor_idx
            self.setup_visuals()
            self.redraw()

        return super().update(*args, **kwargs)

    def setup_visuals(self):
        # if self.draw_mode in DrawModeEnum.Raw | DrawModeEnum.Wireframe:
        #     self.floor_options = self.floor_RAW_colors

        #     outline_width = 0
        #     if self.draw_mode in DrawModeEnum.Wireframe:
        #         outline_width = self.WIREFRAME_outline_width

        #     # Draw floor
        #     color = self.floor_RAW_colors[self.active_floor_idx]
        #     rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        #     rect = pygame.draw.rect(self.image, color, rect, outline_width)

        #     if self.draw_mode in DrawModeEnum.Wireframe:
        #         color = pygame.Color('black')
        #         draw_poly_points_around_rect(self.image, rect, color, self.WIREFRAME_poly_point_radius)
        if self.draw_mode in DrawModeEnum.Rich:
            self.floor_options = self.floor_DM_RICH_medias
            media, scale = self.floor_DM_RICH_medias[self.active_floor_idx]
            self.orig_img = media_manager.get(media)
            self.image_scale = scale
            