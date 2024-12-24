from classes.game_sprite import GameSprite
from config import pygame, math
import config.floor_config as floor_config
from classes.draw_mode_enum import DrawModeEnum
from classes.__helpers__ import draw_poly_points_around_rect
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
    
    def update(self, selected_floor_idx, *args, **kwargs):
        if selected_floor_idx is self.active_floor_idx:
            return

        self.active_floor_idx = selected_floor_idx
        self.setup_visuals()
        return super().update(*args, **kwargs)

    def setup_visuals(self):
        if self.draw_mode in DrawModeEnum.Raw | DrawModeEnum.Wireframe:
            self.floor_options = self.floor_RAW_colors

            outline_width = 0
            if self.draw_mode in DrawModeEnum.Wireframe:
                outline_width = self.WIREFRAME_outline_width

            # Draw floor
            color = self.floor_RAW_colors[self.active_floor_idx]
            rect = pygame.Rect(0, 0, self.size[0], self.size[1])
            rect = pygame.draw.rect(self.image, color, rect, outline_width)

            if self.draw_mode in DrawModeEnum.Wireframe:
                color = pygame.Color('black')
                draw_poly_points_around_rect(self.image, rect, color, self.WIREFRAME_poly_point_radius)
        elif self.draw_mode in DrawModeEnum.Rich:
            self.floor_options = self.floor_DM_RICH_medias

            # Draw floor
            media, scale = self.floor_DM_RICH_medias[self.active_floor_idx]
            img = media_manager.get(media)
            size = (img.get_width() * scale, img.get_height() * scale)
            self.orig_image = pygame.transform.scale(img, size)
            rect = self.orig_image.get_rect()

            rows = math.ceil(self.rect.height / rect.height)
            cols = math.ceil(self.rect.width / rect.width)

            for row in range(rows):
                for col in range(cols):
                    position = (rect.width * col, rect.height * row)
                    self.image.blit(self.orig_image, position)
        
    def on_init(self):
        self.setup_visuals()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)