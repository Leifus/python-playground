from config import pygame
from classes.draw_mode import DrawMode
from classes.media_manager import MediaManager
import config

class UIUserControlOptions():
    def __init__(self, draw_mode, size, position, media_manager: MediaManager):
        self.draw_mode = draw_mode
        self.media_manager = media_manager
        self.position = position
        self.size = size
        self.button_size = (40, 40)
        self.WIREFRAME_outline_width = 2
        self.housing_RAW_color = pygame.Color('gray45')
        self.housing_RICH_media = 'UI/spr_UI_Popup.png'
        self.button_size = (40, 40)
        self.outer_margin = 10
        self.button_spacing = 5
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.font_color = pygame.Color('white')
        self.title = 'User Controls'
        self.title_height = 18
        self.ball_RAW_color_options = []
        self.buttons = []

        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)
        self.housing_surface = self.surface.copy()
        self.housing_RICH_surface = None
        self.relative_mouse_position = None
        self.hovered_component = None
        self.title_rect = None

    def setup_visuals(self):
        title = self.font.render(self.title, True, self.font_color)
        self.title_rect = title.get_rect(topleft=(self.outer_margin, 0))

        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            outline_width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            # Housing
            rect = self.housing_surface.get_rect(topleft=(0, self.title_rect.height))
            pygame.draw.rect(self.housing_surface, self.housing_RAW_color, rect, outline_width)
        elif self.draw_mode in DrawMode.RICH:
            # Housing
            img = self.media_manager.get(self.housing_RICH_media)
            size = (self.size[0], self.size[1] - self.title_rect.height)
            self.housing_RICH_surface = pygame.transform.scale(img, size)
            rect = self.housing_RICH_surface.get_rect(topleft=(0, self.title_rect.height))
            self.housing_surface.blit(self.housing_RICH_surface, rect)

        self.housing_surface.blit(title, self.title_rect)
        
    def setup_options(self):
        # show_travel_path = TOGGLE BUTTON!!!!
        pass

    def on_init(self):
        self.setup_options()
        self.setup_visuals()

    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        self.hovered_component = None

        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return
        
        self.relative_mouse_position = (parent_mouse_position[0] - self.rect.left, parent_mouse_position[1] - self.rect.top)
        
        for button in self.buttons:
            button.on_event(self.relative_mouse_position, event)

    def update(self):
        pass
        
    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        self.surface.blit(self.housing_surface, (0,0))

        for button in self.buttons:
            button.draw(self.surface)

        surface.blit(self.surface, self.rect)
