from classes.button import Button
from classes.draw_mode_enum import DrawModeEnum
from classes.game_sprite import GameSprite
from config import cue_power_bar_config, pygame
from classes.__helpers__ import aspect_scale, draw_poly_points_around_rect
from globals import media_manager


class CuePowerBar(GameSprite):
    def __init__(self, draw_mode, size, position):
        super(CuePowerBar, self).__init__()

        self.draw_mode = draw_mode
        self.size = size
        self.max_power = cue_power_bar_config.cue_power_bar_max_power
        self.power = cue_power_bar_config.cue_power_bar_default_power
        self.power_percent = self.power / self.max_power

        self.position = position
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)
        self.housing_surface = self.image.copy()
        self.housing_overlay_surface = self.image.copy()
        self.cue_surface = self.image.copy()
        self.housing_RAW_color = cue_power_bar_config.cue_power_bar_DM_RAW_color
        self.cue_button_RAW_color = cue_power_bar_config.cue_power_bar_cue_button_DM_RAW_color
        self.housing_RICH_media = cue_power_bar_config.cue_power_bar_DM_RICH_media
        self.housing_overlay_RICH_media = cue_power_bar_config.cue_power_bar_overlay_DM_RICH_media
        self.housing_overlay_RICH_surface = None
        self.housing_RICH_surface = None
        self.WIREFRAME_outline_width = cue_power_bar_config.cue_power_bar_DM_WIREFRAME_thickness
        self.cue_RICH_media = cue_power_bar_config.cue_power_bar_cue_DM_RICH_media
        self.cue_RICH_surface = None
        self.cue_button = None
        self.is_hovered = False
        self.relative_mouse_position = None
        self.cue_tip_size_buffer = 8
        self.is_active = False

    def on_init(self):
        self.setup_visuals()
        self.setup_cue_button()
        self.is_active = True

    def on_cue_button_hover(self, button: Button):
        # print('on_cue_button_hover', button.is_pressed)
        pass

    def on_cue_button_press(self, button: Button):
        mouse_y = self.relative_mouse_position[1]
        self.power_percent = mouse_y / self.rect.height
        self.power = self.max_power * self.power_percent
        button.position = (button.position[0], mouse_y - self.cue_tip_size_buffer)

    def setup_cue_button(self):
        on_hover = self.on_cue_button_hover
        on_press = self.on_cue_button_press
        on_release = None
        position = (0, 0)
        value = None
        self.cue_button = Button(self.cue_surface, position, value, on_hover, on_press, on_release)
        percent = self.power / self.max_power
        y_pos = self.rect.height * percent
        self.cue_button.position = (0, y_pos)

    def setup_visuals(self):
        if self.draw_mode in DrawModeEnum.Raw | DrawModeEnum.Wireframe:
            outline_width = 0
            if self.draw_mode in DrawModeEnum.Wireframe:
                outline_width = self.WIREFRAME_outline_width

            # Draw housing
            rect = pygame.Rect(0, 0, self.size[0], self.size[1])
            rect = pygame.draw.rect(self.housing_surface, self.housing_RAW_color, rect, outline_width)

            if self.draw_mode in DrawModeEnum.Wireframe:
                color = pygame.Color('black')
                draw_poly_points_around_rect(self.housing_surface, rect, color, self.WIREFRAME_outline_width)


            # Draw Cue
            width = 10
            left_pos = self.rect.width/2 - width/2
            rect = pygame.Rect(left_pos, 0, width, self.size[1] - 10)
            rect = pygame.draw.rect(self.cue_surface, self.cue_button_RAW_color, rect, outline_width)
            
            if self.draw_mode in DrawModeEnum.Wireframe:
                color = pygame.Color('black')
                draw_poly_points_around_rect(self.cue_surface, rect, color, self.WIREFRAME_outline_width, offset=(left_pos,0))
            
            # position = (self.rect.width/2 - rect.width/2, 6)
            # self.cue_surface.blit(self.cue_RICH_surface, position)
            
        elif self.draw_mode in DrawModeEnum.Rich:
            # Housing
            img = media_manager.get(self.housing_RICH_media)
            img = pygame.transform.scale(img, self.size)
            self.housing_RICH_surface = img
            self.housing_surface.blit(self.housing_RICH_surface, (0,0))

            # Overlay
            img = media_manager.get(self.housing_overlay_RICH_media)
            img = pygame.transform.scale(img, self.size)
            self.housing_overlay_RICH_surface = img
            self.housing_overlay_surface.blit(self.housing_overlay_RICH_surface, (0,0))

            # Cue
            img = media_manager.get(self.cue_RICH_media)
            img = aspect_scale(img, (img.get_width(), self.size[1] - 10))
            self.cue_RICH_surface = img
            rect = self.cue_RICH_surface.get_rect()
            position = (self.rect.width/2 - rect.width/2, 6)
            self.cue_surface.blit(self.cue_RICH_surface, position)

    def on_event(self, event: pygame.event.Event):
        if not self.is_active:
            return
        
        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return
        
        self.relative_mouse_position = (event.pos[0] - self.rect.left, event.pos[1] - self.rect.top)
        mouse_x = self.relative_mouse_position[0]
        mouse_y = self.relative_mouse_position[1]
        if mouse_x >= 0 and mouse_x <= self.rect.width and mouse_y >= 0 and mouse_y <= self.rect.height:
            self.is_hovered = True
    
        self.cue_button.on_event(self.relative_mouse_position, event)


    def update(self, *args, **kwargs):
        self.is_hovered = self.cue_button.is_hovered
        return super().update(*args, **kwargs)

    # TODO: Tear down and use redraw
    def draw(self, surface: pygame.Surface):
        self.image.fill((0,0,0,0))

        self.image.blit(self.housing_surface, (0, 0))
        self.image.blit(self.cue_button.image, self.cue_button.position)
        self.image.blit(self.housing_overlay_surface, (0, 0))

        surface.blit(self.image, self.rect)