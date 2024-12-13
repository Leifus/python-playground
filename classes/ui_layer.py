from config import pygame, ui_layer_config
from classes.draw_mode import DrawMode
from classes.media_manager import MediaManager
from classes.button import Button
from classes.ui_change_floor_options import UIChangeFloorOptions

class UILayer():
    def __init__(self, size, position, on_change_floor, media_manager: MediaManager):
        self.draw_mode = ui_layer_config.ui_layer_draw_mode
        self.WIREFRAME_outline_width = ui_layer_config.ui_layer_DM_WIREFRAME_outline_width
        self.housing_RAW_color = ui_layer_config.ui_layer_housing_DM_RAW_color
        self.housing_RICH_media = ui_layer_config.ui_layer_housing_DM_RICH_media

        self.position = position
        self.media_manager = media_manager
        self.on_change_floor = on_change_floor

        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)

        self.housing_surface = self.surface.copy()
        self.housing_RICH_surface = None

        self.options_button = None
        self.change_floor_options = None

        self.is_active = False
        self.relative_mouse_position = None
        self.hovered_component = None

    def setup_visuals(self):
        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            outline_width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            # Housing
            pygame.draw.rect(self.housing_surface, self.housing_RAW_color, self.rect, outline_width)
        elif self.draw_mode in DrawMode.RICH:
            # Housing
            housing = self.media_manager.get(self.housing_RICH_media, convert_alpha=True)
            if not housing:
                print('No ui_housing img:', self.housing_RICH_media)
            else:
                self.housing_RICH_surface = pygame.transform.scale(housing, self.housing_surface.get_size())
                self.housing_surface.blit(self.housing_RICH_surface, (0, 0))

    def on_options_button_hover(self, button):
        self.hovered_component = button

    def on_options_button_press(self, button: Button):
        self.toggle_ui_layer()
        button.is_pressed = False

    def setup_change_floor_options(self):
        size = (self.rect.width, 200)
        position = (size[0]/2, 100 + size[1]/2)
        draw_mode = self.draw_mode
        self.change_floor_options = UIChangeFloorOptions(draw_mode, size, position, self.on_change_floor, self.media_manager)
        self.change_floor_options.on_init()

    def setup_options_button(self):
        size = ui_layer_config.ui_layer_options_button_size
        button_RAW_color = ui_layer_config.ui_layer_options_button_DM_RAW_color
        position = ui_layer_config.ui_layer_options_button_position
        label = ui_layer_config.ui_layer_options_button_label
        font_family = ui_layer_config.ui_layer_options_button_DM_RAW_font_family
        font_size = ui_layer_config.ui_layer_options_button_DM_RAW_font_size
        font_color = ui_layer_config.ui_layer_options_button_DM_RAW_font_color
        rich_media = ui_layer_config.ui_layer_options_button_DM_RICH_media
        on_hover = self.on_options_button_hover
        on_press = self.on_options_button_press
        draw_mode = self.draw_mode
        self.options_button = Button(size, button_RAW_color, label, 0, draw_mode, position, font_family, font_size, font_color, rich_media, on_hover, on_press, self.media_manager)
        
    def on_init(self):
        self.setup_options_button()
        self.setup_change_floor_options()
        self.setup_visuals()

    def on_event(self, event: pygame.event.Event):
        self.hovered_component = None

        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            self.relative_mouse_position = (event.pos[0] - self.rect.left, event.pos[1] - self.rect.top)
        
        self.options_button.on_event(self.relative_mouse_position, event)

        if not self.is_active:
            return
        
        self.change_floor_options.on_event(self.relative_mouse_position, event)
        if self.change_floor_options.hovered_component is not None:
            self.hovered_component = self.change_floor_options.hovered_component

    def toggle_ui_layer(self):
        self.is_active = not self.is_active

    def update(self):
        self.options_button.update()
        if self.is_active:
            self.change_floor_options.update()

        if self.hovered_component is not None:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        if self.is_active:
            self.surface.blit(self.housing_surface, (0, 0))
            self.change_floor_options.draw(self.surface)

        self.options_button.draw(self.surface)

        surface.blit(self.surface, self.rect)