from classes.button import Button
from classes.game_sprite import GameSprite
from config import pygame
from classes.draw_mode_enum import DrawModeEnum
from globals import media_manager

class UILightControlOptions(GameSprite):
    def __init__(self, draw_mode, size, position):
        super(UILightControlOptions, self).__init__()

        self.draw_mode = draw_mode
        self.position = position
        self.size = size
        self.WIREFRAME_outline_width = 2
        self.housing_RAW_color = pygame.Color('gray45')
        self.housing_RICH_media = 'UI/spr_UI_Popup.png'
        self.outer_margin = 10
        self.button_spacing = 5
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.font_color = pygame.Color('white')
        self.title = 'Light Settings'
        self.title_height = 18
        self.ball_RAW_color_options = []
        self.buttons_group = pygame.sprite.Group()

        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)

        self.title_orig_image: pygame.Surface | None = None
        self.housing_orig_image: pygame.Surface | None = None

        self.relative_mouse_position = None
        self.hovered_component = None

        self.move_light = False
        self.light_size_scale = 1.0
        self.light_strength_scale = 1.0

        self.setup_visuals()
        self.setup_buttons()
        self.redraw()

    def redraw(self):
        self.image.fill((0,0,0,0))

        # Title
        title_image = self.title_orig_image
        title_rect = title_image.get_rect(topleft=(self.outer_margin, 0))
        
        # Housing
        size = (self.size[0], self.size[1] - title_rect.height)
        housing_image = pygame.transform.scale(self.housing_orig_image, size)
        housing_rect = housing_image.get_rect(topleft=(0, title_rect.height))

        # Buttons
        for button in self.buttons_group:
            housing_image.blit(button.image, button.rect)

        self.image.blit(housing_image, housing_rect)
        self.image.blit(title_image, title_rect)
     
    def setup_visuals(self):
        self.title_orig_image = self.font.render(self.title, True, self.font_color)

        if self.draw_mode in DrawModeEnum.Rich:
            # Housing
            self.housing_orig_image = media_manager.get(self.housing_RICH_media)

    def setup_buttons(self):
        # Control light with mouse
        font_family = 'freesansbold.ttf'
        font_size = 12
        font_color = pygame.Color('black')
        font = pygame.font.Font(font_family, font_size)

        row = 0
        col = 0
        on_hover = self.on_button_hover
        on_press = self.on_move_light_button_press
        on_release = None
        button_color = pygame.Color('white')
        
        button_size = (60, 30)
        button_surface = pygame.Surface(button_size, pygame.SRCALPHA)
        x = self.outer_margin + button_size[0]*col + self.button_spacing + self.button_spacing*col
        y = self.title_height + self.outer_margin + button_size[1]*row + self.button_spacing + self.button_spacing*row
        if x > self.size[0]:
            col = 0
            row += 1
        else:
            col += 1

        value = True
        position = (x, y)
        label = 'Move'
        
        button_image = button_surface.copy()
        button_image.fill(button_color)

        text = font.render(label, True, font_color)
        text_rect = text.get_rect(center=button_image.get_rect().center)
        button_image.blit(text, text_rect)
        button_rect = button_image.get_rect()

        position = (x, y)
        button = Button(button_image, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(button)

        # Change Light Size
        label = 'Resize'
        button_image = button_surface.copy()
        button_image.fill(button_color)
        text = font.render(label, True, font_color)
        text_rect = text.get_rect(center=button_image.get_rect().center)
        button_image.blit(text, text_rect)
        x = x + button_rect.right + self.button_spacing*2
        position = (x, y)
        on_press = self.on_change_light_size_button_press
        button = Button(button_image, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(button)

        # Change Light Strength
        label = 'Strength'
        button_image = button_surface.copy()
        button_image.fill(button_color)
        text = font.render(label, True, font_color)
        text_rect = text.get_rect(center=button_image.get_rect().center)
        button_image.blit(text, text_rect)
        x = x + button_rect.right + self.button_spacing*2
        position = (x, y)
        on_press = self.on_change_light_strength_button_press
        button = Button(button_image, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(button)

    def on_button_hover(self, button: Button):
        self.hovered_component = button
         
    def on_change_light_size_button_press(self, button: Button):
        self.light_size_scale = self.light_size_scale / 2
        if self.light_size_scale < 0.25:
            self.light_size_scale = 3.0

    def on_change_light_strength_button_press(self, button: Button):
        self.light_strength_scale = self.light_strength_scale / 2
        if self.light_strength_scale < 0.25:
            self.light_strength_scale = 3.0

    def on_move_light_button_press(self, button: Button):
        self.move_light = button.value
        button.value = not button.value

    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        self.hovered_component = None

        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return
        
        self.relative_mouse_position = (parent_mouse_position[0] - self.rect.left, parent_mouse_position[1] - self.rect.top)
        
        relative_button_mouse_pos = (self.relative_mouse_position[0], self.relative_mouse_position[1] - self.title_height)
        for button in self.buttons_group:
            button.on_event(relative_button_mouse_pos, event)
