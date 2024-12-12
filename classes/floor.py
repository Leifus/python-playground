from config import pygame, math
import config.floor_config as floor_config
from classes.media_manager import MediaManager
from classes.draw_mode import DrawMode
from classes.__helpers__ import draw_poly_points_around_rect

class Floor():
    def __init__(self, size, position, media_manager: MediaManager):
        self.draw_mode = floor_config.floor_draw_mode
        self.floor_RAW_color = floor_config.floor_DM_RAW_color
        self.floor_tile_RICH_media = floor_config.floor_tile_DM_RICH_media
        self.floor_tile_RICH_scale = floor_config.floor_tile_DM_RICH_scale
        self.WIREFRAME_outline_width = floor_config.floor_DM_WIREFRAME_thickness
        self.WIREFRAME_poly_point_radius = floor_config.floor_DM_WIREFRAME_poly_point_radius

        self.size = size
        self.position = position
        self.media_manager = media_manager

        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=position)
        self.raw_surface = None
        self.floor_RICH_surface = None
        self.floor_tile_RICH_surface = None
    
    def setup_visuals(self):
        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            self.raw_surface = self.surface.copy()
            outline_width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            # Draw floor
            rect = pygame.Rect(0, 0, self.size[0], self.size[1])
            rect = pygame.draw.rect(self.raw_surface, self.floor_RAW_color, rect, outline_width)

            if self.draw_mode in DrawMode.WIREFRAME:
                color = pygame.Color('black')
                draw_poly_points_around_rect(self.raw_surface, rect, color, self.WIREFRAME_poly_point_radius)
        elif self.draw_mode in DrawMode.RICH:
            self.floor_RICH_surface = self.surface.copy()

            # Draw floor
            img = self.media_manager.get(self.floor_tile_RICH_media)
            size = (img.get_width() * self.floor_tile_RICH_scale, img.get_height() * self.floor_tile_RICH_scale)
            self.floor_tile_RICH_surface = pygame.transform.scale(img, size)
            rect = self.floor_tile_RICH_surface.get_rect()

            rows = math.ceil(self.rect.height / rect.height)
            cols = math.ceil(self.rect.width / rect.width)

            for row in range(rows):
                for col in range(cols):
                    position = (rect.width * col, rect.height * row)
                    self.floor_RICH_surface.blit(self.floor_tile_RICH_surface, position)
        
    def on_init(self):
        self.setup_visuals()

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            self.surface.blit(self.raw_surface, (0, 0))
        elif self.draw_mode in DrawMode.RICH:
            self.surface.blit(self.floor_RICH_surface, (0, 0))

        surface.blit(self.surface, self.rect)