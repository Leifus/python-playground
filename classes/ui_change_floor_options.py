from config import pygame, ui_layer_config, floor_config
from classes.draw_mode import DrawMode
from classes.media_manager import MediaManager
from classes.button import Button

class UIChangeFloorOptions():
    def __init__(self, draw_mode, size, position, on_change_floor, media_manager: MediaManager):
        self.draw_mode = draw_mode
        self.media_manager = media_manager
        self.position = position
        self.size = size
        self.on_change_floor = on_change_floor
        self.WIREFRAME_outline_width = 2
        self.housing_RAW_color = pygame.Color('white')
        self.floor_button_size = (30, 30)
        self.floor_button_spacing = 5
        self.floor_button_RAW_color = pygame.Color('black')
        self.floor_DM_RICH_medias = floor_config.floor_DM_RICH_medias

        self.floor_RAW_color_options = [
            pygame.Color('black'),
            pygame.Color('blue'),
            pygame.Color('pink'),
            pygame.Color('brown'),
            pygame.Color('turquoise'),
            pygame.Color('violetred'),
            pygame.Color('wheat'),
            pygame.Color('yellow2'),
            pygame.Color('salmon'),
            pygame.Color('seagreen1'),
            pygame.Color('mediumpurple2'),
            pygame.Color('indigo'),
        ]

        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)
        self.housing_surface = self.surface.copy()
        self.floor_button_surface = self.surface.copy()
        self.change_floor_buttons = []
        self.relative_mouse_position = None
        self.hovered_component = None

    def setup_visuals(self):
        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            outline_width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            # Housing
            rect = pygame.Rect(0, 0, self.size[0], self.size[1])
            pygame.draw.rect(self.housing_surface, self.housing_RAW_color, rect, outline_width)
        elif self.draw_mode in DrawMode.RICH:
            pass

    def setup_change_floor_buttons(self):
        row = 0
        col = 0
        font_family = ui_layer_config.ui_layer_options_button_DM_RAW_font_family
        font_size = ui_layer_config.ui_layer_options_button_DM_RAW_font_size
        font_color = ui_layer_config.ui_layer_options_button_DM_RAW_font_color

        button_protos = []
        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            for color in self.floor_RAW_color_options:
                media = None
                button_protos.append([
                    color, media
                ])
        elif self.draw_mode in DrawMode.RICH:
            color = pygame.Color('black')
            for media, scale in self.floor_DM_RICH_medias:
                button_protos.append([
                    color, media
                ])

        for i, data in enumerate(button_protos):
            color, media = data
            x = 0 + self.floor_button_size[0]*col + self.floor_button_spacing + self.floor_button_spacing*col
            y = 0 + self.floor_button_size[1]*row + self.floor_button_spacing + self.floor_button_spacing*row
            if x > self.size[1]:
                col = 0
                row += 1
            else:
                col += 1
            
            position = (x + self.floor_button_size[0]/2, y + self.floor_button_size[1]/2)
            label = f'{i}'
            on_hover = self.on_change_floor_button_hover
            on_press = self.on_change_floor_button_press
            button = Button(self.floor_button_size, color, label, i, self.draw_mode, position, font_family, font_size, font_color, media, on_hover, on_press, self.media_manager)
            self.change_floor_buttons.append(button)
                 
    def on_change_floor_button_hover(self, button: Button):
        self.hovered_component = button
         
    def on_change_floor_button_press(self, button: Button):
        self.on_change_floor(button.value)

    def on_init(self):
        self.setup_change_floor_buttons()
        self.setup_visuals()

    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        self.hovered_component = None

        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return
        
        self.relative_mouse_position = (parent_mouse_position[0] - self.rect.left, parent_mouse_position[1] - self.rect.top)
        
        for button in self.change_floor_buttons:
            button.on_event(self.relative_mouse_position, event)

    def update(self):
        pass
        
    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        self.surface.blit(self.housing_surface, (0,0))

        for button in self.change_floor_buttons:
            button.draw(self.surface)

        surface.blit(self.surface, self.rect)
