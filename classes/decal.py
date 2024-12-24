from classes.__helpers__ import aspect_scale
from config import pygame
from classes.game_sprite import GameSprite

class Decal(GameSprite):
    def __init__(self, orig_image, size, position, use_aspect_scale=False):
        super(Decal, self).__init__()

        self.size = size
        self.position = position
        self.use_aspect_scale = use_aspect_scale

        self.orig_image: pygame.Surface | None = orig_image
        self.image: pygame.Surface | None = None
        self.mask: pygame.mask.Mask | None = None
        self.rect: pygame.Rect | None = None

        self.redraw()
    
    def redraw(self):
        if not self.use_aspect_scale:
            self.image = pygame.transform.scale(self.orig_image, self.size)
        else:
            self.image = aspect_scale(self.orig_image, self.size)

        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)