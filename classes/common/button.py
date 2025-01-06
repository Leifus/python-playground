from classes.common.game_sprite import GameSprite
from config import pygame

class Button(GameSprite):
    def __init__(self, surface: pygame.Surface, position, value, on_hover, on_press, on_release):
        super(Button, self).__init__()

        self.image: pygame.Surface = surface
        self.rect = self.image.get_rect(topleft=position)
        self.position = position
        
        self.value = value
        self.on_hover = on_hover
        self.on_press = on_press
        self.on_release = on_release
        self.is_hovered = False
        self.is_pressed = False

    def on_event(self, mouse_position: pygame.Vector2, event: pygame.event.Event):
        is_in_x = False
        is_in_y = False
        if mouse_position:
            is_in_x = mouse_position.x >= self.rect.left and mouse_position.x <= self.rect.right
            is_in_y = mouse_position.y >= self.rect.top and mouse_position.y <= self.rect.bottom

        self.is_hovered = is_in_x and is_in_y

        if self.is_hovered:
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
            