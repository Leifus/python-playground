from classes.game_sprite import GameSprite
from classes.ui_light_control_options import UILightControlOptions
from config import pygame

class LightSource(GameSprite):
    def __init__(self, lumens, radius, position, z_position, show_light):
        super(LightSource, self).__init__()
        
        self.z_position = z_position
        self.base_radius = radius
        self.radius = radius
        self.position = position
        self.show_light = show_light
        self.lumens = lumens
        self.base_lumens = lumens
        self.alpha = lumens/2
        self.light_size_scale = 1.0
        self.light_strength_scale = 1.0

        self.image: pygame.Surface | None = None
        self.orig_image: pygame.Surface | None = None

        self.surface: pygame.Surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rect: pygame.Rect = self.surface.get_rect(center=self.position)


        self.setup_visuals()
        self.redraw()

    def redraw(self):
        self.image = pygame.transform.scale(self.orig_image, (self.radius*2, self.radius*2))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.position)
        self.image.set_alpha(self.alpha)

    def setup_visuals(self):
        self.orig_image = self.surface.copy()
        color = pygame.Color('lightyellow1')
        pygame.draw.circle(self.orig_image, color, (self.radius,self.radius), self.radius)
        
    def update(self, light_options: UILightControlOptions, mouse_position, *args, **kwargs):
        redraw = False
        if light_options.light_size_scale != self.light_size_scale:
            self.light_size_scale = light_options.light_size_scale
            self.radius = self.base_radius * self.light_size_scale
            redraw = True

        if light_options.light_strength_scale != self.light_strength_scale:
            self.light_strength_scale = light_options.light_strength_scale
            self.lumens = self.base_lumens * self.light_strength_scale
            redraw = True

        if light_options.move_light:
            self.position = mouse_position
            self.rect = self.image.get_rect(center=self.position)
            redraw = True

        if redraw:
            self.redraw()

        return super().update(*args, **kwargs)

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))
        if self.show_light:
            self.surface.blit(self.image, (0,0))
            
        surface.blit(self.surface, self.rect)
    