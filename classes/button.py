from config import pygame
from classes.draw_mode import DrawMode
from classes.media_manager import MediaManager
from classes.__helpers__ import aspect_scale

class Button():
    def __init__(self, size, color, label, value, draw_mode, position, font_family, font_size, font_color, rich_media, on_hover, on_press, media_manager: MediaManager):
        self.draw_mode = draw_mode
        self.media_manager = media_manager
        self.WIREFRAME_outline_width = 2
        self.size = size
        self.RAW_color = color
        self.button_RICH_media = rich_media
        self.position = position
        self.label = label
        self.value = value
        self.font = pygame.font.Font(font_family, font_size)
        self.font_color = font_color
        self.is_hovered = False
        self.is_pressed = False
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)
        self.button_surface = self.surface.copy()
        self.button_RICH_surface = None
        self.on_hover = on_hover
        self.on_press = on_press
        self.setup_visuals()

        self.relative_mouse_position = None

    def setup_visuals(self):
        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            outline_width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            rect = pygame.Rect(0, 0, self.size[0], self.size[1])
            pygame.draw.rect(self.button_surface, self.RAW_color, rect, outline_width)

            text = self.font.render(self.label, True, self.font_color)
            text_rect = text.get_rect(center=self.button_surface.get_rect().center)
            self.button_surface.blit(text, text_rect)
        elif self.draw_mode in DrawMode.RICH:
            btn = self.media_manager.get(self.button_RICH_media, convert_alpha=True)
            if not btn:
                print('No button img:', self.button_RICH_media)
            else:            
                self.button_RICH_surface = pygame.transform.scale(btn, self.size)
                # self.button_RICH_surface = aspect_scale(btn, self.size)
                self.button_surface.blit(self.button_RICH_surface, self.button_surface.get_rect())


    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        self.is_hovered = False

        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return
        
        self.relative_mouse_position = (parent_mouse_position[0] - self.rect.left, parent_mouse_position[1] - self.rect.top)
        
        if self.relative_mouse_position[0] >= 0 and self.relative_mouse_position[0] <= self.rect.width and self.relative_mouse_position[1] >= 0 and self.relative_mouse_position[1] <= self.rect.height:
            self.is_hovered = True
            if self.on_hover is not None:
                self.on_hover(self)

        if self.is_hovered and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_pressed = True
            if self.on_press is not None:
                self.on_press(self)
    
    def update(self):
        # if self.is_hovered:
        #     print('hovering button', self.label)
        # if self.is_pressed:
        #     print('button pressed', self.label)
        pass

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        self.surface.blit(self.button_surface, (0,0))

        surface.blit(self.surface, self.rect)
