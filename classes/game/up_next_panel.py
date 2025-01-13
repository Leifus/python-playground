from classes.common.game_sprite import GameSprite
from classes.common.helper_methods import aspect_scale
from classes.game.merge_object import MergeObject
from config import pygame

class UpNextPanel(GameSprite):
    def __init__(self, size, position):
        super(UpNextPanel, self).__init__()

        self.size = size
        self.position = position
        self.follow_mouse = False
        self.up_next: list[MergeObject] = []
        self.next_object: MergeObject = None
        self.border_width = 3

        self.redraw()

    def redraw(self):
        # Housing
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)

        # Next Object
        if self.next_object:
            # Next Object Image
            scale = 0.9
            surface_size = ((self.size[0]-self.border_width*2)*scale, (self.size[1]-self.border_width*2)*scale)
            surface = pygame.Surface(surface_size, pygame.SRCALPHA)
            surface.fill('gray80')
            surface_rect = surface.get_rect(center=(self.size[0]/2, self.size[1]/2))

            image_scale = 0.8
            image_size = (surface_size[0]*image_scale, surface_size[1]*image_scale)
            image = aspect_scale(self.next_object.image, image_size)
            image_rect = image.get_rect(center=(surface_size[0]/2, surface_size[1]/2))

            # Next Object Label
            font_size = 9
            font = pygame.font.Font('freesansbold.ttf', font_size)
            label = self.next_object.label
            font_color = pygame.Color('black')
            background_color = pygame.Color('yellow')
            label_surface = font.render(label, True, font_color, background_color)
            label_rect = label_surface.get_rect()
            label_rect.bottomleft = (self.border_width, self.rect.height - self.border_width)

            surface.blit(image, image_rect)
            self.image.blit(surface, surface_rect)
            self.image.blit(label_surface, label_rect)

        # Border
        border_color = pygame.Color('gray70')
        pygame.draw.rect(self.image, border_color, pygame.Rect(0, 0, self.size[0], self.size[1]), self.border_width)

    def set_position(self, position):
        self.position = position
        self.rect = self.image.get_rect(center=self.position)
    
    def update(self, *args, **kwargs):
        if len(self.up_next) > 0:
            if self.next_object is None:
                self.next_object = self.up_next[0]
                self.redraw()
        else:
            self.next_object = None

        return super().update(*args, **kwargs)