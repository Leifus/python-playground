from config import pygame

class ButtonNew(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface, position, on_hover, on_press, on_release):
        pygame.sprite.Sprite.__init__(self)

        self.surface = surface
        self.image = None
        self.rect = self.surface.get_rect()
        self.position = position
        self.on_hover = on_hover
        self.on_press = on_press
        self.on_release = on_release
        self.is_hovered = False
        self.is_pressed = False

    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        self.is_hovered = False

        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return
        
        self.relative_mouse_position = (parent_mouse_position[0] - self.rect.left, parent_mouse_position[1] - self.rect.top)
        
        if self.relative_mouse_position[0] >= 0 and self.relative_mouse_position[0] <= self.rect.width and self.relative_mouse_position[1] >= 0 and self.relative_mouse_position[1] <= self.rect.height:
            self.is_hovered = True
            if self.on_hover is not None:
                self.on_hover(self)

        if self.is_pressed and event.type == pygame.MOUSEBUTTONUP and self.on_release is not None:
            self.on_release(self)

        self.is_pressed = pygame.mouse.get_pressed()[0] and self.is_hovered
        if self.is_pressed and self.on_press is not None:
            self.on_press(self)