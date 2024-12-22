from classes.camera import Camera
from config import pygame
from classes.game_sprite import GameSprite


class CameraScreen(GameSprite):
    def __init__(self, size, position, camera: Camera):
        super(GameSprite, self).__init__()

        self.size = size
        self.position = position
        self.camera = camera

        self.setup_visuals()

    def setup_visuals(self):
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)
        self.redraw()

    def redraw(self):
        self.image.fill((255,255,255,255))
        
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)
    
    def draw(self, surface: pygame.Surface):
        self.camera.draw(surface)
        surface.blit(self.image, self.rect)