from config import pygame
from classes.game_sprite import GameSprite
from globals import media_manager

class PlayersGui(GameSprite):
    def __init__(self, size, position):
        super(GameSprite, self).__init__()

        self.size = size
        self.position = position

        self.setup_visuals()

    def setup_visuals(self):
        media = 'UI/spr_UI_Player_Bar.png'
        img = media_manager.get(media)
        self.orig_image = pygame.transform.scale(img, self.size)
        self.image = self.orig_image
        self.rect = self.image.get_rect(center=self.position)

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)
    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)