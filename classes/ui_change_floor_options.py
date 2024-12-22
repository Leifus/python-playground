from classes.game_sprite import GameSprite
from config import pygame, floor_config
from classes.draw_mode_enum import DrawModeEnum
from classes.button import Button
from globals import media_manager

class UIChangeFloorOptions(GameSprite):
    def __init__(self, draw_mode, size, position, on_change_floor):
        super(GameSprite, self).__init__()

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

        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)

        self.title_orig_image: pygame.Surface | None = None
        self.housing_orig_image: pygame.Surface | None = None
        self.button_orig_images = []

        self.buttons_group = pygame.sprite.Group()
        self.relative_mouse_position = None
        self.hovered_component = None

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
     
    def setup_buttons(self):
        row = 0
        col = 0
        on_hover = self.on_button_hover
        on_press = self.on_button_press
        on_release = None
        for i, button_orig_image in enumerate(self.button_orig_images):
            x = self.outer_margin + self.button_size[0]*col + self.button_spacing*col
            y = self.outer_margin + self.button_size[1]*row + self.button_spacing + self.button_spacing*row
            if x > self.size[0]:
                col = 0
                row += 1
            else:
                col += 1
            
            button_image = pygame.transform.scale(button_orig_image, self.button_size)
            
            position = (x, y)
            value = i
            button = Button(button_image, position, value, on_hover, on_press, on_release)
            self.buttons_group.add(button)

    def setup_visuals(self):
        self.title_orig_image = self.font.render(self.title, True, self.font_color)

        # if self.draw_mode in DrawModeEnum.RAW | DrawModeEnum.WIREFRAME:
        #     outline_width = 0
        #     if self.draw_mode in DrawModeEnum.WIREFRAME:
        #         outline_width = self.WIREFRAME_outline_width

        #     # Housing
        #     rect = self.housing_surface.get_rect(topleft=(0, title_rect.height))
        #     pygame.draw.rect(self.housing_surface, self.housing_RAW_color, rect, outline_width)

        #     # Buttons
        #     button_surface = pygame.Surface(self.button_size, pygame.SRCALPHA)
        #     for color in self.floor_RAW_color_options:
        #         surface = button_surface.copy()
        #         surface.fill(color)
        #         self.button_surfaces.append(surface)
        if self.draw_mode in DrawModeEnum.RICH:
            # Housing
            self.housing_orig_image = media_manager.get(self.housing_RICH_media)
            
            # Buttons
            for media, scale in self.floor_DM_RICH_medias:
                button_orig_image = media_manager.get(media, convert=True)
                self.button_orig_images.append(button_orig_image)
                 
    def on_button_hover(self, button: Button):
        self.hovered_component = button
         
    def on_button_press(self, button: Button):
        self.on_change_floor(button.value)

    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        self.hovered_component = None

        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return
        
        self.relative_mouse_position = (parent_mouse_position[0] - self.rect.left, parent_mouse_position[1] - self.rect.top)
        
        relative_button_mouse_pos = (self.relative_mouse_position[0], self.relative_mouse_position[1] - self.title_height)
        for button in self.buttons_group:
            button.on_event(relative_button_mouse_pos, event)

