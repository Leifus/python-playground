from classes.ui_user_control_options import UIUserControlOptions
from config import pygame, ui_layer_config
from classes.draw_mode import DrawMode
from classes.button import Button
from classes.ui_change_floor_options import UIChangeFloorOptions
from classes.ui_change_pool_table_balls_options import UIChangePoolTableBallsOptions
from globals import media_manager

class UILayer():
    def __init__(self, size, position, on_change_floor, on_change_ball_set):
        self.draw_mode = ui_layer_config.ui_layer_draw_mode
        self.WIREFRAME_outline_width = ui_layer_config.ui_layer_DM_WIREFRAME_outline_width
        self.housing_RAW_color = ui_layer_config.ui_layer_housing_DM_RAW_color
        self.housing_RICH_media = ui_layer_config.ui_layer_housing_DM_RICH_media
        self.options_button_RICH_media = ui_layer_config.ui_layer_options_button_DM_RICH_media

        self.position = position
        self.on_change_floor = on_change_floor
        self.on_change_ball_set = on_change_ball_set

        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)

        self.housing_surface = self.surface.copy()
        self.housing_RICH_surface = None

        self.options_button_position = ui_layer_config.ui_layer_options_button_position
        self.button_size = ui_layer_config.ui_layer_options_button_size
        self.button_surface = pygame.Surface(self.button_size, pygame.SRCALPHA)

        self.options_button = None
        self.change_floor_options = None
        self.change_balls_options = None
        self.user_control_options = None

        self.is_active = False
        self.is_hovered = False
        self.relative_mouse_position = None
        self.hovered_component = None

    def setup_visuals(self):
        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            outline_width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            # Housing
            pygame.draw.rect(self.housing_surface, self.housing_RAW_color, self.rect, outline_width)

            # Main Options Button
            button_color = ui_layer_config.ui_layer_options_button_DM_RAW_color
            label = ui_layer_config.ui_layer_options_button_label
            font_family = ui_layer_config.ui_layer_options_button_DM_RAW_font_family
            font_size = ui_layer_config.ui_layer_options_button_DM_RAW_font_size
            font_color = ui_layer_config.ui_layer_options_button_DM_RAW_font_color
            self.button_surface.fill(button_color)
            font = pygame.font.Font(font_family, font_size)
            text = font.render(label, True, font_color)
            button_rect = self.button_surface.get_rect()
            text_rect = text.get_rect(center=(button_rect.width/2, button_rect.height/2))
            self.button_surface.blit(text, text_rect)


        elif self.draw_mode in DrawMode.RICH:
            # Housing
            housing = media_manager.get(self.housing_RICH_media, convert_alpha=True)
            if not housing:
                print('No ui_housing img:', self.housing_RICH_media)
            else:
                self.housing_RICH_surface = pygame.transform.scale(housing, self.housing_surface.get_size())
                self.housing_surface.blit(self.housing_RICH_surface, (0, 0))

            # Main Options Button
            img = media_manager.get(self.options_button_RICH_media)
            img = pygame.transform.scale(img, self.button_size)
            self.button_surface = img

        # size = ui_layer_config.ui_layer_options_button_size
        # button_RAW_color = ui_layer_config.ui_layer_options_button_DM_RAW_color
        # label = ui_layer_config.ui_layer_options_button_label
        # font_family = ui_layer_config.ui_layer_options_button_DM_RAW_font_family
        # font_size = ui_layer_config.ui_layer_options_button_DM_RAW_font_size
        # font_color = ui_layer_config.ui_layer_options_button_DM_RAW_font_color
        # rich_media = ui_layer_config.ui_layer_options_button_DM_RICH_media

    def on_options_button_hover(self, button):
        self.hovered_component = button

    def on_options_button_press(self, button: Button):
        self.toggle_ui_layer()
        button.is_pressed = False

    def setup_change_floor_options(self):
        size = (self.rect.width, 80)
        position = (size[0]/2, 100 + size[1]/2)
        draw_mode = self.draw_mode
        self.change_floor_options = UIChangeFloorOptions(draw_mode, size, position, self.on_change_floor, media_manager)
        self.change_floor_options.on_init()

    def setup_change_pool_table_ball_options(self):
        size = (self.rect.width, 100)
        position = (size[0]/2, self.change_floor_options.rect.bottom + 16 + size[1]/2)
        draw_mode = self.draw_mode
        self.change_balls_options = UIChangePoolTableBallsOptions(draw_mode, size, position, self.on_change_ball_set, media_manager)
        self.change_balls_options.on_init()

    def setup_options_button(self):
        position = self.options_button_position
        on_hover = self.on_options_button_hover
        on_press = self.on_options_button_press
        on_release = None
        draw_mode = self.draw_mode
        value = 0
        self.options_button = Button(self.button_surface, position, value, on_hover, on_press, on_release)
        # self.options_button = Button(size, button_RAW_color, label, 0, draw_mode, position, font_family, font_size, font_color, rich_media, on_hover, on_press, media_manager)
        
    def setup_user_control_options(self):
        size = (self.rect.width, 140)
        position = (size[0]/2, self.change_balls_options.rect.bottom + 16 + size[1]/2)
        draw_mode = self.draw_mode
        self.user_control_options = UIUserControlOptions(draw_mode, size, position, media_manager)
        self.user_control_options.on_init()

    def on_init(self):
        self.setup_visuals()
        self.setup_options_button()
        self.setup_change_floor_options()
        self.setup_change_pool_table_ball_options()
        self.setup_user_control_options()

    def on_event(self, event: pygame.event.Event):
        self.hovered_component = None
        self.is_hovered = False
        
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            self.relative_mouse_position = (event.pos[0] - self.rect.left, event.pos[1] - self.rect.top)
            mouse_x = self.relative_mouse_position[0]
            mouse_y = self.relative_mouse_position[1]
            if self.is_active and mouse_x >= 0 and mouse_x <= self.rect.width and mouse_y >= 0 and mouse_y <= self.rect.height:
                self.is_hovered = True
        
        self.options_button.on_event(self.relative_mouse_position, event)

        if not self.is_active:
            return
        
        self.change_floor_options.on_event(self.relative_mouse_position, event)
        self.change_balls_options.on_event(self.relative_mouse_position, event)
        self.user_control_options.on_event(self.relative_mouse_position, event)
        if self.change_floor_options.hovered_component is not None:
            self.hovered_component = self.change_floor_options.hovered_component
        elif self.change_balls_options.hovered_component is not None:
            self.hovered_component = self.change_balls_options.hovered_component

        if self.hovered_component is not None:
            self.is_hovered = True

    def toggle_ui_layer(self):
        self.is_active = not self.is_active

    def update(self):
        self.options_button.update()
        if not self.is_active:
            return
        
        self.change_floor_options.update()
        self.change_balls_options.update()
        self.user_control_options.update()

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        if self.is_active:
            self.surface.blit(self.housing_surface, (0, 0))
            self.change_floor_options.draw(self.surface)
            self.change_balls_options.draw(self.surface)
            self.user_control_options.draw(self.surface)

        self.surface.blit(self.options_button.image, self.options_button.position)

        surface.blit(self.surface, self.rect)