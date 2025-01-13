from classes.common.button import Button
from classes.common.game_sprite import GameSprite
from classes.image_panel import ImagePanel
from config import pygame
from globals import media_manager

class Toolbar(GameSprite):
    def __init__(self, position, size):
        super(Toolbar, self).__init__()

        self.position = position
        self.size = size
        self.is_hovered = False
        self.is_active = False
        self.button_size = 28
        self.button_gap = 10
        self.move_button_default_image: pygame.Surface = None
        self.move_button_hover_image: pygame.Surface = None
        self.move_button_active_image: pygame.Surface = None
        self.buttons_group = pygame.sprite.Group()
        self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW
        self.linked_image_panel: ImagePanel = None
        self.hovered_button: Button = None

        self.setup_visuals()
        self.setup_toolbar()
        self.redraw()

    def setup_visuals(self):
        # Housing 
        self.housing_image = pygame.Surface(self.size, pygame.SRCALPHA)
        color = pygame.Color('gray90')
        self.housing_image.fill(color)

        # Housing Edge
        color = pygame.Color('gray70')
        thickness = 2
        start_pos = (self.size[0]-thickness, 0)
        end_pos = (self.size[0]-thickness, self.size[1])
        pygame.draw.line(self.housing_image, color, start_pos, end_pos, thickness)

        # Buttons
        button_default_bg_color = pygame.Color('gray95')
        button_hover_bg_color = pygame.Color('gray80')
        button_active_bg_color = pygame.Color('gold')
        button_border_color = pygame.Color('gray80')
        button_border_width = 1
        button_surface = pygame.Surface((self.button_size, self.button_size), pygame.SRCALPHA)
        button_border_surface = button_surface.copy()
        button_surface.fill(button_default_bg_color)
        pygame.draw.rect(button_border_surface, button_border_color, pygame.Rect(0,0,self.button_size,self.button_size), button_border_width)

        # Move Button
        image = media_manager.get('icons/move_icon.png', convert_alpha=True)
        icon_scale = 0.8
        button_icon = pygame.transform.scale(image, (self.button_size*icon_scale, self.button_size*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size/2, self.button_size/2))

        # default
        button_image = button_surface.copy()
        button_image.blit(button_border_surface, (0,0))
        button_image.blit(button_icon, icon_rect)
        self.move_button_default_image = button_image

        # hover
        button_image = button_surface.copy()
        button_image.fill(button_hover_bg_color)
        button_image.blit(button_border_surface, (0,0))
        button_image.blit(button_icon, icon_rect)
        self.move_button_hover_image = button_image

        # active
        button_image = button_surface.copy()
        button_image.fill(button_active_bg_color)
        button_image.blit(button_border_surface, (0,0))
        button_image.blit(button_icon, icon_rect)
        self.move_button_active_image = button_image

    def on_event(self, mouse_position: pygame.Vector2, event: pygame.event.Event):
        self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW
        relative_mouse_position = None

        if mouse_position:
            relative_mouse_position = (mouse_position.x - self.rect.left, mouse_position.y - self.rect.top)

        self.hovered_button = None
        for button in self.buttons_group:
            button: Button
            button.on_event(relative_mouse_position, event)
            if button.is_hovered:
                self.hovered_button = button

        self.is_hovered = self.hovered_button is not None
        if self.is_hovered:
            self.mouse_cursor = pygame.SYSTEM_CURSOR_HAND

    def redraw(self):
        self.image = pygame.transform.scale(self.housing_image, self.size)
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, surface: pygame.Surface):
        if not self.is_active:
            return
        
        self.buttons_group.draw(self.image)

        surface.blit(self.image, self.rect)

    
    def setup_toolbar(self):
        x = self.button_gap
        y = self.button_gap

        # Move Button
        position = (x,y)
        value = 'move'
        tooltip = 'Move panels'
        on_hover = None
        on_press = self.on_move_button_press
        on_release = None
        self.move_button = Button(self.move_button_default_image, position, value, on_hover, on_press, on_release, hover_surface=self.move_button_hover_image, active_surface=self.move_button_active_image, tooltip=tooltip)
        self.buttons_group.add(self.move_button)

    def on_move_button_press(self, button):
        pass