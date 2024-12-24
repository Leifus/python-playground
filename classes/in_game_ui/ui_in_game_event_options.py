from classes.common.button import Button
from classes.common.game_sprite import GameSprite
from classes.enums.in_game_event_enum import InGameEventEnum
from config import pygame
from classes.enums.draw_mode_enum import DrawModeEnum
from globals import media_manager

class UIInGameEventOptions(GameSprite):
    def __init__(self, draw_mode, size, position):
        super(UIInGameEventOptions, self).__init__()

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
        self.title = 'Game Events'
        self.title_height = 18
        self.ball_RAW_color_options = []
        self.buttons_group = pygame.sprite.Group()

        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)

        self.title_orig_image: pygame.Surface | None = None
        self.housing_orig_image: pygame.Surface | None = None

        self.relative_mouse_position = None
        self.hovered_component = None

        self.selected_game_event: InGameEventEnum = InGameEventEnum.NONE

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

        on_hover = self.on_button_hover
        on_press = self.on_button_press
        on_release = None
        button_color = pygame.Color('white')
        
        button_size = (80, 30)
        button_surface = pygame.Surface(button_size, pygame.SRCALPHA)

        row = 0
        col = 0
        for i, in_game_event in enumerate(InGameEventEnum):
            if in_game_event is InGameEventEnum.NONE:
                continue
            
            x = self.outer_margin + button_size[0]*col + self.button_spacing + self.button_spacing*col
            y = self.title_height + self.outer_margin + button_size[1]*row + self.button_spacing + self.button_spacing*row
            if x > self.size[0]:
                col = 0
                row += 1
            else:
                col += 1

            value = in_game_event
            position = (x, y)
            
            button_image = button_surface.copy()
            button_image.fill(button_color)

            label = in_game_event.name
            text = font.render(label, True, font_color)
            text_rect = text.get_rect(center=button_image.get_rect().center)
            button_image.blit(text, text_rect)

            position = (x, y)
            button = Button(button_image, position, value, on_hover, on_press, on_release)
            self.buttons_group.add(button)


    def on_button_hover(self, button: Button):
        self.hovered_component = button
        
    def on_button_press(self, button: Button):
        self.selected_game_event = button.value
         
    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        self.hovered_component = None

        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return
        
        self.relative_mouse_position = (parent_mouse_position[0] - self.rect.left, parent_mouse_position[1] - self.rect.top)
        
        relative_button_mouse_pos = (self.relative_mouse_position[0], self.relative_mouse_position[1] - self.title_height)
        for button in self.buttons_group:
            button.on_event(relative_button_mouse_pos, event)
