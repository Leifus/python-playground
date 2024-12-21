from classes.ui_light_control_options import UILightControlOptions
from config import pygame

class LightSource(pygame.sprite.Sprite):
    def __init__(self, lumens, radius, position, z_position, show_light):
        # TODO: Implement types better!
        # lumens: int     #range from 0 to 255
        # radius: float

        pygame.sprite.Sprite.__init__(self)
        
        self.z_position = z_position
        self.base_radius = radius
        self.radius = radius
        self.position = position
        self.show_light = show_light
        self.orig_image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rect = self.orig_image.get_rect(center=self.position)
        self.image = None
        self.lumens = lumens
        self.alpha = lumens/2

        self.light_size = 1.0

        self.setup_visuals()

    def setup_visuals(self):
        color = pygame.Color('lightyellow1')
        pygame.draw.circle(self.orig_image, color, (self.radius,self.radius), self.radius)
        self.image = self.orig_image
        self.image.set_alpha(self.alpha)

    def update(self, light_options: UILightControlOptions, mouse_position, *args, **kwargs):
        if light_options.light_size != self.light_size:
            self.light_size = light_options.light_size
            self.radius = self.base_radius * self.light_size
            self.image = pygame.transform.scale(self.orig_image, (self.radius*2, self.radius*2))

        if light_options.move_light:
            self.position = mouse_position
        
        self.rect = self.image.get_rect(center=self.position)

        return super().update(*args, **kwargs)

    def draw(self, surface: pygame.Surface):
        if not self.show_light:
            return
        
        # self.surface.fill((0,0,0,0))
        # self.image.set_alpha(self.alpha)
        # self.surface.blit(self.image, (0,0))
        surface.blit(self.image, self.rect)