from config import pygame

class GameSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = None
        self.orig_image = None
        self.mask = None
        self.rect = None