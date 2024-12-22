from config import pygame, ui_layer_config, floor_config
from classes.draw_mode_enum import DrawModeEnum
from classes.button import Button
from globals import media_manager

class UIChangeFloorOptions():
    def __init__(self, draw_mode, size, position, on_change_floor):
        self.draw_mode = draw_mode
        self.position = position
        self.size = size
        self.on_change_floor = on_change_floor
        self.WIREFRAME_outline_width = 2
        self.housing_RAW_color = pygame.Color('gray45')
        self.housing_RICH_media = 'UI/spr_UI_Popup.png'
        self.button_size = (30, 30)
        self.outer_margin = 10
        self.button_spacing = 5
        self.floor_button_RAW_color = pygame.Color('black')
        self.floor_DM_RICH_medias = floor_config.floor_DM_RICH_medias
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.font_color = pygame.Color('white')
        self.title = 'Change Floor'
        self.title_height = 18

        self.floor_RAW_color_options = [
            pygame.Color('black'),
            pygame.Color('blue'),
            pygame.Color('pink'),
            pygame.Color('brown'),
            pygame.Color('turquoise'),
            pygame.Color('violetred'),
        ]

        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)
        self.housing_surface = self.surface.copy()
        self.housing_RICH_surface = None
        self.floor_button_surface = self.surface.copy()
        self.buttons_group = pygame.sprite.Group()
        self.relative_mouse_position = None
        self.hovered_component = None
        self.title_rect = None
        self.button_surfaces = []

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

            # Buttons
            button_surface = pygame.Surface(self.button_size, pygame.SRCALPHA)
            for color in self.floor_RAW_color_options:
                surface = button_surface.copy()
                surface.fill(color)
                self.button_surfaces.append(surface)

        elif self.draw_mode in DrawModeEnum.RICH:
            # Housing
            img = media_manager.get(self.housing_RICH_media)
            size = (self.size[0], self.size[1] - self.title_rect.height)
            self.housing_RICH_surface = pygame.transform.scale(img, size)
            rect = self.housing_RICH_surface.get_rect(topleft=(0, self.title_rect.height))

            self.housing_surface.blit(self.housing_RICH_surface, rect)

            # Buttons
            for media, scale in self.floor_DM_RICH_medias:
                img = media_manager.get(media, convert=True)
                img = pygame.transform.scale(img, self.button_size)
                self.button_surfaces.append(img)

        self.housing_surface.blit(title, self.title_rect)

    def setup_buttons(self):
        row = 0
        col = 0
        on_hover = self.on_change_floor_button_hover
        on_press = self.on_change_floor_button_press
        on_release = None
        for i, surface in enumerate(self.button_surfaces):
            x = self.outer_margin + self.button_size[0]*col + self.button_spacing + self.button_spacing*col
            y = self.title_height + self.outer_margin + self.button_size[1]*row + self.button_spacing + self.button_spacing*row
            if x > self.size[0]:
                col = 0
                row += 1
            else:
                col += 1
            
            position = (x, y)
            # label = f'{i}'
            value = i
            button = Button(surface, position, value, on_hover, on_press, on_release)
            self.buttons_group.add(button)
                 
    def on_change_floor_button_hover(self, button: Button):
        self.hovered_component = button
         
    def on_change_floor_button_press(self, button: Button):
        self.on_change_floor(button.value)

    def on_init(self):
        self.setup_visuals()
        self.setup_buttons()

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

        #TODO: Use .blits()
        for button in self.buttons_group:
            self.surface.blit(button.image, button.position)

        surface.blit(self.surface, self.rect)
