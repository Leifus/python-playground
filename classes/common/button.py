from classes.common.game_sprite import GameSprite
from config import pygame

class Button(GameSprite):
    def __init__(self, surface: pygame.Surface, position, value, on_hover, on_press, on_release, hover_surface: pygame.Surface = None, active_surface: pygame.Surface = None, tooltip: str=None):
        super(Button, self).__init__()

        self.orig_image: pygame.Surface = surface
        self.hover_surface: pygame.Surface = hover_surface
        self.active_surface: pygame.Surface = active_surface
        self.position = position
        self.tooltip = tooltip
        self.value = value
        self.on_hover = on_hover
        self.on_press = on_press
        self.on_release = on_release
        self.is_hovered = False
        self.is_pressed = False
        self.is_active = False

        self.redraw()

    def redraw(self):
        if self.is_active and self.active_surface:
            self.image = self.active_surface
        elif self.is_hovered and self.hover_surface:
            self.image = self.hover_surface
        else:
            self.image = self.orig_image

        self.rect = self.image.get_rect(topleft=self.position)

    def update(self, *args, **kwargs):
        if self.is_hovered and self.hover_surface and self.image is not self.hover_surface:
            self.redraw()
        elif self.is_active and self.active_surface and self.image is not self.active_surface:
            self.redraw()
                
        return super().update(*args, **kwargs)

    def on_event(self, mouse_position: pygame.Vector2, event: pygame.event.Event):
        is_in_x = False
        is_in_y = False
        if mouse_position:
            is_in_x = mouse_position[0] >= self.rect.left and mouse_position[0] <= self.rect.right
            is_in_y = mouse_position[1] >= self.rect.top and mouse_position[1] <= self.rect.bottom

        self.is_hovered = is_in_x and is_in_y

        if self.is_hovered:
            if self.hover_surface:
                self.image = self.hover_surface
                
            if self.on_hover:
                self.on_hover(self)
            
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                buttons_pressed = pygame.mouse.get_pressed()
                if event.type == pygame.MOUSEBUTTONDOWN and buttons_pressed[0]:
                    self.is_pressed = True
                    if self.on_press:
                        self.on_press(self)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.is_pressed = False
                    if self.on_release:
                        self.on_release(self)

        else:
            self.is_pressed = False
            if self.hover_surface and self.image is not self.orig_image:
                self.image = self.orig_image
    
    def set_position(self, position):
        self.position = position
        self.rect.center = self.position