from config import pygame, pymunk
import config

class PathTracer():
    def __init__(self, surface):
        self.surface = surface#pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.position_a = None
        self.position_b = None
        self.position_a_color = pygame.Color('red')
        self.position_b_color = pygame.Color('red')
        self.line_color = pygame.Color('black')
        self.line_width = 2
        self.position_radius = 3

    def update(self, position_a, position_b):
        self.position_a = position_a
        self.position_b = position_b

        if self.position_a is not None:
            pygame.draw.circle(self.surface, self.position_a_color, self.position_a, self.position_radius)

        if self.position_b is not None:
            pygame.draw.circle(self.surface, self.position_b_color, self.position_b, self.position_radius)
            pygame.draw.line(self.surface, self.line_color, self.position_a, self.position_b, self.line_width)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)