from config import pygame, math
import config.floor_config as floor_config
from classes.media_manager import MediaManager

class Floor():
    def __init__(self, size, position, media_manager: MediaManager):
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect(center=position)
        self.media_manager = media_manager
        self.floor_tile_media_path = floor_config.floor_tile_media_path
        self.tile_scale = floor_config.floor_tile_scale
        self.tile_surface = None
        self.tile_rect = None
        
    def on_init(self):
        img = self.media_manager.get(self.floor_tile_media_path)
        size = (img.get_width() * self.tile_scale, img.get_height() * self.tile_scale)
        self.tile_surface = pygame.transform.scale(img, size)
        self.tile_rect = self.tile_surface.get_rect()

        rows = math.ceil(self.rect.height / self.tile_rect.height)
        cols = math.ceil(self.rect.width / self.tile_rect.width)
        draw_x = self.rect.width - self.tile_rect.width

        for row in range(rows):
            for col in range(cols):
                position = (self.tile_rect.width * col, self.tile_rect.height * row)
                self.surface.blit(self.tile_surface, position)
                

        # while draw_y > 0:
        #     draw_y -= self.tile_rect.height
        #     while draw_x > 0:
        #         draw_x -= self.tile_rect.width
        #         position = (position[0] + self.tile_rect.width, position[1])
        #         self.surface.blit(self.tile_surface, position)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)