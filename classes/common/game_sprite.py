from config import pygame

class GameSprite(pygame.sprite.Sprite):
    def __init__(self):
        super( GameSprite, self).__init__()
        
        self.size = None
        self.position = (0,0)
        self.angle = 0

        self.surface: pygame.Surface | None = None
        self.image: pygame.Surface | None = None
        self.orig_image: pygame.Surface | None = None
        self.mask: pygame.mask.Mask | None = None
        self.rect: pygame.Rect | None = None

    def create_default_surface(self):
        if self.size is None:
            return
        
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.orig_image = self.surface
        self.image = self.orig_image
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

