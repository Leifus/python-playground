from pygame import MOUSEBUTTONDOWN, MOUSEMOTION
from config import pygame, pymunk, math
import config

class PoolCue():
    def __init__(self):
        self.position = (50, 300)
        self.angle = 0
        self.alpha = 255
        self.length = 320
        self.tip_thickness = 5
        self.base_thickness = 15
        self.color = pygame.Color('orange')
        self.focused_color = pygame.Color('red')
        self.picked_up_color = pygame.Color('blue')
        self.surface_buffer = 2
        surface = pygame.Surface((self.base_thickness + self.surface_buffer, self.length + self.surface_buffer), pygame.SRCALPHA)
        self.orig_surface = surface
        self.surface = surface
        # self.surface.fill('white')
        self.rect = self.surface.get_rect(center=self.position)
        self.mouse_position = None
        self.is_focused = False
        self.cue_poly_points = self.construct_cue_poly_points()
        # self.cue_poly = None
        # self.focused_cue_poly = None
        self.is_picked_up = False
        self.pick_up = False

    def construct_cue_poly_points(self):
        half_buffer = self.surface_buffer/2
        points = (
            [half_buffer, self.length + half_buffer], 
            [half_buffer + self.base_thickness, self.length + half_buffer], 
            [half_buffer + (self.base_thickness/2) + (self.tip_thickness/2), 0], 
            [half_buffer + (self.base_thickness/2) - (self.tip_thickness/2), 0]
        )

        return points

    def _draw(self):
        # draw bg
        # self.surface.fill('white')

        # draw cue
        color = self.color
        if self.is_picked_up:
            color = self.picked_up_color
        elif self.is_focused:
            color = self.focused_color

        width = 0
        pygame.draw.polygon(self.surface, color, self.cue_poly_points, width)


    def on_init(self):
        self._draw()

    def on_event(self, event: pygame.event.Event):
        if event.type not in [MOUSEBUTTONDOWN, MOUSEMOTION]:
            return
        
        self.mouse_position = event.pos

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.is_focused and not self.is_picked_up:
                self.pick_up = True

    def check_is_focused(self):
        if self.mouse_position is None:
            return False
        
        mouse_x = self.mouse_position[0]
        mouse_y = self.mouse_position[1]

        is_within_x = mouse_x >= self.rect.left and mouse_x <= self.rect.right
        is_within_y = mouse_y >= self.rect.top and mouse_y <= self.rect.bottom
        
        return is_within_x and is_within_y

    def set_cue_position(self):
        self.surface = pygame.transform.rotate(self.orig_surface, self.angle)

        #check angle to set rect
        print('cue angle', self.angle)
        print('cue position', self.position)
        self.rect = self.surface.get_rect(center=self.rect.center)

    def update(self):
        is_focused = self.check_is_focused()

        draw = False
        if is_focused is not self.is_focused:
            self.is_focused = is_focused
            draw = True

        if self.pick_up:
            self.is_picked_up = True
            draw = True

        if draw:
            self._draw()

        if self.is_picked_up:
            self.set_cue_position()


    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)