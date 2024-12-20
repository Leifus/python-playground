from turtle import position
from classes.button_new import ButtonNew
from classes.draw_mode import DrawMode
from config import cue_power_bar_config, pygame
from classes.media_manager import MediaManager
from classes.__helpers__ import aspect_scale, draw_poly_points_around_rect


class CuePowerBar():
    def __init__(self, draw_mode, size, position, media_manager: MediaManager):
        self.draw_mode = draw_mode
        self.size = size
        self.media_manager = media_manager
        self.max_power = cue_power_bar_config.cue_power_bar_max_power
        self.power = cue_power_bar_config.cue_power_bar_default_power

        self.position = position
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)
        self.housing_surface = self.surface.copy()
        self.housing_overlay_surface = self.surface.copy()
        self.cue_surface = self.surface.copy()
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

    def on_cue_button_hover(self, button: ButtonNew):
        # print('on_cue_button_hover', button.is_pressed)
        pass

    def on_cue_button_press(self, button: ButtonNew):
        mouse_y = self.relative_mouse_position[1]
        percent = mouse_y / self.rect.height
        self.power = self.max_power * percent
        button.position = (button.position[0], mouse_y - self.cue_tip_size_buffer)

    def setup_cue_button(self):
        on_hover = self.on_cue_button_hover
        on_press = self.on_cue_button_press
        on_release = None
        percent = self.power / self.max_power
        y_pos = self.rect.height * percent
        position = (0, y_pos)
        self.cue_button = ButtonNew(self.cue_surface, position, on_hover, on_press, on_release)

    def setup_visuals(self):
        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            outline_width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            # Draw housing
            rect = pygame.Rect(0, 0, self.size[0], self.size[1])
            rect = pygame.draw.rect(self.housing_surface, self.housing_RAW_color, rect, outline_width)

            if self.draw_mode in DrawMode.WIREFRAME:
                color = pygame.Color('black')
                draw_poly_points_around_rect(self.housing_surface, rect, color, self.WIREFRAME_outline_width)


            # Draw Cue
            width = 10
            left_pos = self.rect.width/2 - width/2
            rect = pygame.Rect(left_pos, 0, width, self.size[1] - 10)
            rect = pygame.draw.rect(self.cue_surface, self.cue_button_RAW_color, rect, outline_width)
            
            if self.draw_mode in DrawMode.WIREFRAME:
                color = pygame.Color('black')
                draw_poly_points_around_rect(self.cue_surface, rect, color, self.WIREFRAME_outline_width, offset=(left_pos,0))
            
            # position = (self.rect.width/2 - rect.width/2, 6)
            # self.cue_surface.blit(self.cue_RICH_surface, position)
            
        elif self.draw_mode in DrawMode.RICH:
            # Housing
            img = self.media_manager.get(self.housing_RICH_media)
            img = pygame.transform.scale(img, self.size)
            self.housing_RICH_surface = img
            self.housing_surface.blit(self.housing_RICH_surface, (0,0))

            # Overlay
            img = self.media_manager.get(self.housing_overlay_RICH_media)
            img = pygame.transform.scale(img, self.size)
            self.housing_overlay_RICH_surface = img
            self.housing_overlay_surface.blit(self.housing_overlay_RICH_surface, (0,0))

            # TODO: TURN THIS INTO A BUTTON YES!?
            # THIS WOULD REQURE US TO FEED A BUTTON A BAKED SURFACE...

            # Cue
            img = self.media_manager.get(self.cue_RICH_media)
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


    def update(self):
        self.is_hovered = self.cue_button.is_hovered

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        self.surface.blit(self.housing_surface, (0, 0))
        self.surface.blit(self.cue_button.surface, self.cue_button.position)
        self.surface.blit(self.housing_overlay_surface, (0, 0))

        surface.blit(self.surface, self.rect)
        
    