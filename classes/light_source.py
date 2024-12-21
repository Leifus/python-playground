from config import pygame

class LightSource(pygame.sprite.Sprite):
    def __init__(self, lumens, radius, position, z_position):
        pygame.sprite.Sprite.__init__(self)
        
        self.z_position = z_position
        self.radius = radius
        self.position = position
        self.surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)
        self.image = None
        self.lumens = lumens
        self.setup_visuals()

    def setup_visuals(self):
        self.image = self.surface.copy()
        color = pygame.Color('lightyellow1')
        pygame.draw.circle(self.image, color, (self.radius,self.radius), self.radius)

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))
        self.image.set_alpha(10)
        self.surface.blit(self.image, (0,0))
        surface.blit(self.surface, self.rect)