from classes.common.game_sprite import GameSprite
from config import pygame, pymunk

class GameTableObject(GameSprite):
    def __init__(self, size, position):
        super(GameTableObject, self).__init__()

        self.size = size
        self.position = position

        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)

        self.body: pymunk.Body = None
        self.shape: pymunk.Shape = None
        self.elasticity: float = 0.0
        self.friction: float = 0.0

        self.on_collide_begin_func = None
        self.on_collide_pre_solve_func = None
        self.on_collide_post_solve_func = None
        self.on_collide_seperate_func = None
        
        self.z_distance_from_floor = 0.01

    def update(self, time_lapsed, *args, **kwargs):
        return super().update(*args, **kwargs)

    def kill(self):
        if self.shape.space:
            self.shape.space.remove(self.shape)

        if self.body.space:
            self.body.space.remove(self.body)

        super().kill()