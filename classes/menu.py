from pygame import Vector2
from classes.common.button import Button
from classes.common.game_sprite import GameSprite
from config import pygame

class Menu(GameSprite):
    def __init__(self, size, position):
        super(Menu, self).__init__()

        self.size = size
        self.position = position
        self.orig_housing_image: pygame.Surface = None
        self.orig_tools_default_image: pygame.Surface = None
        self.buttons_group = pygame.sprite.Group()
        self.mouse_position: Vector2 = None
        self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW
        self.is_hovered = False
        self.active_button: Button = None

        self.setup_visuals()
        self.setup_buttons()
        self.redraw()

    def setup_visuals(self):
        # Housing
        housing_bg_color = 'gray90'
        self.orig_housing_image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.orig_housing_image.fill(housing_bg_color)

        # Housing Edge
        color = pygame.Color('gray70')
        thickness = 2
        start_pos = (0, self.size[1]-thickness)
        end_pos = (self.size[0], self.size[1]-thickness)
        pygame.draw.line(self.orig_housing_image, color, start_pos, end_pos, thickness)


        # Tools Button
        button_default_bg_color = pygame.Color('gray70')
        button_hover_bg_color = pygame.Color('gray80')
        button_active_bg_color = pygame.Color('gray90')
        button_size = (self.size[0]/2, self.size[1])
        self.orig_tools_default_image = pygame.Surface(button_size, pygame.SRCALPHA)
        self.orig_tools_default_image.fill(button_default_bg_color)
        self.orig_tools_hover_image = pygame.Surface(button_size, pygame.SRCALPHA)
        self.orig_tools_hover_image.fill(button_hover_bg_color)
        self.orig_tools_active_image = pygame.Surface(button_size, pygame.SRCALPHA)
        self.orig_tools_active_image.fill(button_active_bg_color)
        
        font = pygame.font.Font('freesansbold.ttf', 16)
        color = pygame.Color('black')
        label_surface = font.render('Tools', True, color)
        label_rect = label_surface.get_rect()
        self.orig_tools_default_image.blit(label_surface, (button_size[0]/2-label_rect.width/2, button_size[1]/2-label_rect.height/2))
        self.orig_tools_hover_image.blit(label_surface, (button_size[0]/2-label_rect.width/2, button_size[1]/2-label_rect.height/2))
        self.orig_tools_active_image.blit(label_surface, (button_size[0]/2-label_rect.width/2, button_size[1]/2-label_rect.height/2))
        
        color = pygame.Color('gray70')
        thickness = 2
        start_pos = (button_size[0], 0)
        end_pos = (button_size[0], button_size[1])
        pygame.draw.line(self.orig_tools_default_image, color, start_pos, end_pos, thickness)


        # Media Explorer Button
        button_size = (self.size[0]/2, self.size[1])
        self.orig_media_explorer_default_image = pygame.Surface(button_size, pygame.SRCALPHA)
        self.orig_media_explorer_default_image.fill(button_default_bg_color)
        self.orig_media_explorer_hover_image = pygame.Surface(button_size, pygame.SRCALPHA)
        self.orig_media_explorer_hover_image.fill(button_hover_bg_color)
        self.orig_media_explorer_active_image = pygame.Surface(button_size, pygame.SRCALPHA)
        self.orig_media_explorer_active_image.fill(button_active_bg_color)

        color = pygame.Color('black')
        label_surface = font.render('Media', True, color)
        label_rect = label_surface.get_rect()
        self.orig_media_explorer_default_image.blit(label_surface, (button_size[0]/2-label_rect.width/2, button_size[1]/2-label_rect.height/2))
        self.orig_media_explorer_hover_image.blit(label_surface, (button_size[0]/2-label_rect.width/2, button_size[1]/2-label_rect.height/2))
        self.orig_media_explorer_active_image.blit(label_surface, (button_size[0]/2-label_rect.width/2, button_size[1]/2-label_rect.height/2))
        
        color = pygame.Color('gray70')
        thickness = 2
        start_pos = (0, 0)
        end_pos = (0, button_size[1])
        pygame.draw.line(self.orig_media_explorer_default_image, color, start_pos, end_pos, thickness)

    def on_event(self, mouse_position: Vector2, event: pygame.event.Event):
        self.mouse_position = mouse_position
        self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW

        hovered_button = None
        for button in self.buttons_group:
            button: Button
            button.on_event(self.mouse_position, event)
            if button.is_hovered:
                hovered_button = button

        self.is_hovered = hovered_button is not None
        if self.is_hovered:
            self.mouse_cursor = pygame.SYSTEM_CURSOR_HAND

    def update(self, *args, **kwargs):
        self.buttons_group.update()

        return super().update(*args, **kwargs)

    def redraw(self):
        self.image = self.orig_housing_image
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, surface: pygame.Surface):
        self.buttons_group.draw(self.image)
        surface.blit(self.image, self.rect)

    def setup_buttons(self):
        # Tools Button
        position = (0, 0)
        value = 'Tools'
        on_hover = None
        on_press = self.on_tools_button_press
        on_release = None
        tools_button = Button(self.orig_tools_default_image, position, value, on_hover, on_press, on_release, hover_surface=self.orig_tools_hover_image, active_surface=self.orig_tools_active_image)
        self.buttons_group.add(tools_button)

        # Media Explorer Button
        position = (tools_button.rect.width, 0)
        value = 'Media'
        on_hover = None
        on_press = self.on_media_explorer_button_press
        on_release = None
        media_button = Button(self.orig_media_explorer_default_image, position, value, on_hover, on_press, on_release, hover_surface=self.orig_media_explorer_hover_image, active_surface=self.orig_media_explorer_active_image)
        self.buttons_group.add(media_button)

        self.set_active_button(tools_button)

    def set_active_button(self, button: Button):
        if self.active_button:
            self.active_button.is_active = False
            if not self.active_button.is_active and self.active_button is button:
                self.active_button = None
                return

        self.active_button = button
        self.active_button.is_active = True

    def on_tools_button_press(self, button):
        self.set_active_button(button)

    def on_media_explorer_button_press(self, button):
        self.set_active_button(button)