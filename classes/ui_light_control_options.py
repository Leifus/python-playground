from classes.button import Button
from config import pygame
from classes.draw_mode_enum import DrawModeEnum
from globals import media_manager

class UILightControlOptions():
    def __init__(self, draw_mode, size, position):
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

        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)
        self.housing_surface = self.surface.copy()
        self.housing_RICH_surface = None
        self.relative_mouse_position = None
        self.hovered_component = None
        self.title_rect = None

        self.move_light = False
        self.light_size = 1.0

    def setup_visuals(self):
        title = self.font.render(self.title, True, self.font_color)
        self.title_rect = title.get_rect(topleft=(self.outer_margin, 0))

        if self.draw_mode in DrawModeEnum.RAW | DrawModeEnum.WIREFRAME:
            outline_width = 0
            if self.draw_mode in DrawModeEnum.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            # Housing
            rect = self.housing_surface.get_rect(topleft=(0, self.title_rect.height))
            pygame.draw.rect(self.housing_surface, self.housing_RAW_color, rect, outline_width)
        elif self.draw_mode in DrawModeEnum.RICH:
            # Housing
            img = media_manager.get(self.housing_RICH_media)
            size = (self.size[0], self.size[1] - self.title_rect.height)
            self.housing_RICH_surface = pygame.transform.scale(img, size)
            rect = self.housing_RICH_surface.get_rect(topleft=(0, self.title_rect.height))
            self.housing_surface.blit(self.housing_RICH_surface, rect)

        self.housing_surface.blit(title, self.title_rect)
        
    def on_button_hover(self, button: Button):
        self.hovered_component = button
         
    def on_change_light_size_button_press(self, button: Button):
        self.light_size = self.light_size / 2
        if self.light_size < 0.25:
            self.light_size = 2.0

    def on_move_light_button_press(self, button: Button):
        self.move_light = button.value
        button.value = not button.value

    def setup_options(self):
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
        
        button_size = (100, 40)
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
        label = 'Move Light'
        
        surface = button_surface.copy()
        surface.fill(button_color)

        text = font.render(label, True, font_color)
        text_rect = text.get_rect(center=surface.get_rect().center)
        surface.blit(text, text_rect)
        rect = surface.get_rect()

        position = (x, y)
        button = Button(surface, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(button)

        # Change Light Size
        label = 'Resize Light'
        surface = button_surface.copy()
        surface.fill(button_color)
        text = font.render(label, True, font_color)
        text_rect = text.get_rect(center=surface.get_rect().center)
        surface.blit(text, text_rect)

        x = x + rect.right + self.button_spacing*2
        position = (x, y)
        on_press = self.on_change_light_size_button_press
        button = Button(surface, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(button)

    def on_init(self):
        self.setup_options()
        self.setup_visuals()

    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        self.hovered_component = None

        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return
        
        self.relative_mouse_position = (parent_mouse_position[0] - self.rect.left, parent_mouse_position[1] - self.rect.top)
        
        for button in self.buttons_group:
            button.on_event(self.relative_mouse_position, event)

    def update(self):
        pass
        
    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        self.surface.blit(self.housing_surface, (0,0))

        self.buttons_group.draw(self.surface)

        surface.blit(self.surface, self.rect)
