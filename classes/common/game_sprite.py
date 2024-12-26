from config import pygame

class GameSprite(pygame.sprite.Sprite):
    def __init__(self):
        super( GameSprite, self).__init__()
        
        self.size = None
        self.position = None
        self.angle = 0

        self.image: pygame.Surface | None = None
        self.orig_image: pygame.Surface | None = None
        self.mask: pygame.mask.Mask | None = None
        self.rect: pygame.Rect | None = None
        
        #TODO: REPLACE THIS TO HANDLE DEAFAULT OBJ ID
        # self._identifier: float = identifier

    #TODO: Tear this down
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)