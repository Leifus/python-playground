from pygame import Vector2
from classes.game_sprite import GameSprite
from classes.light_source import LightSource
from config import pygame, math

class Shadow(GameSprite):
    def __init__(self, parent_obj):     
        super(GameSprite, self).__init__()

        self.mask = parent_obj.mask
        self.alpha = 50
        unsetcolor=(0,0,0,0)
        setcolor=(0,0,0,255)
        self.orig_image = self.mask.to_surface(unsetcolor=unsetcolor, setcolor=setcolor)
        mask_rect = self.mask.get_rect()
        # height_scale = 0.5
        # width_scale = 0.5
        self.orig_size = (mask_rect.width, mask_rect.height)
        self.image = pygame.transform.smoothscale(self.orig_image, self.orig_size)
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

        height_scale = 1.0
        width_scale = 1.0
        distance_in_light_sources = parent_pos.distance_to(light_pos) / light_source.rect.width
        _distance_in_light_sources = abs(dx / light_source.rect.width)
        if distance_in_light_sources > 0:
            lumens = light_source.lumens / distance_in_light_sources
            strength_factor = lumens / 255
            self.alpha = lumens
            height_scale = 1.0 / distance_in_light_sources
            width_scale = 1.0 / distance_in_light_sources
        
        offset = Vector2(x_off/2, y_off*self.parent_obj.z_distance_from_floor)
        # offset = Vector2(0,0)

        new_width = self.orig_size[0] / width_scale
        new_height = self.orig_size[1] / height_scale
        position = Vector2(self.parent_obj.rect.midbottom) + offset
        self.image = pygame.transform.scale(self.orig_image, (new_width, new_height))
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(midbottom=(position[0], position[1]))

        return super().update(*args, **kwargs)
