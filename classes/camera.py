from config import pygame
from classes.game_sprite import GameSprite


class Camera(GameSprite):
    def __init__(self, size, position):
        super(GameSprite, self).__init__()

        self.size = size
        self.position = position

        self.setup_visuals()

    def setup_visuals(self):
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)
        self.redraw()

    def redraw(self):
        self.image.fill((0,0,0,50))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
