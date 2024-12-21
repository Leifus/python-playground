from pygame import Vector2
from classes.light_source import LightSource
from config import pygame, math

class Shadow(pygame.sprite.Sprite):
    def __init__(self, parent_obj):
        pygame.sprite.Sprite.__init__(self)
        self.mask = parent_obj.mask
        self.alpha = 50
        unsetcolor=(0,0,0,0)
        setcolor=(0,0,0,255)
        self.orig_image = self.mask.to_surface(unsetcolor=unsetcolor, setcolor=setcolor)
        mask_rect = self.mask.get_rect()
        height_scale = 0.6
        width_scale = 0.6
        self.orig_size = (mask_rect.width*width_scale, mask_rect.height*height_scale)
        self.image = pygame.transform.scale(self.orig_image, self.orig_size)
        self.image.set_alpha(self.alpha)
        self.parent_obj = parent_obj
        self.rect = self.image.get_rect()

    def update(self, relative_parent_position_offset, light_source: LightSource, *args, **kwargs):
        parent_pos = Vector2(self.parent_obj.rect.center) + Vector2(relative_parent_position_offset)
        light_pos = Vector2(light_source.position)

        dx, dy = Vector2(parent_pos-light_pos)
        angle = math.atan2(dy, dx)

        x_off = self.orig_size[0] * math.cos(angle)
        y_off = self.orig_size[1] * math.sin(angle)

        distance_in_light_sources = abs(dx / light_source.rect.width)
        if distance_in_light_sources > 0:
            lumens = light_source.lumens / distance_in_light_sources
            strength_factor = lumens / 255
            self.alpha = lumens
        
        offset = Vector2(x_off/2, y_off/2)
        position = Vector2(self.parent_obj.rect.center) + offset

        new_width = self.orig_size[0] * distance_in_light_sources
        new_height = self.orig_size[1] * distance_in_light_sources
        self.image = pygame.transform.scale(self.orig_image, (new_width, new_height))
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=position)

        return super().update(*args, **kwargs)
