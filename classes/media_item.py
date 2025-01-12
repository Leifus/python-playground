
from classes.common.game_sprite import GameSprite
from config import pygame


class MediaItem(GameSprite):
    def __init__(self, folder_name, file_name, position, housing_width):
        super(MediaItem, self).__init__()
        
        self.position = position
        self.housing_width = housing_width
        self.folder_name = folder_name
        self.file_name = file_name

        self.font_size = 14
        self.font_color = pygame.Color('black')
        self.font = pygame.font.Font('freesansbold.ttf', self.font_size)

        self.is_hovered = False

        self.redraw()

    def redraw(self):
        txt_surface = self.font.render(self.file_name, True, self.font_color, None)
        line_height = self.font_size * 1.5
        txt_rect = txt_surface.get_rect(midleft=(4, line_height/2))

        self.image = pygame.Surface((self.housing_width, line_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=self.position)

        if self.is_hovered:
            self.image.fill('gold')

        self.image.blit(txt_surface, txt_rect)

    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        is_hovered = False
        if parent_mouse_position is not None:
            mouse_x, mouse_y = parent_mouse_position

            is_in_x = mouse_x >= self.rect.left and mouse_x <= self.rect.right
            is_in_y = mouse_y >= self.rect.top and mouse_y <= self.rect.bottom
            if is_in_x and is_in_y:
                is_hovered = True

        if self.is_hovered is not is_hovered:
            self.is_hovered = is_hovered
            self.redraw()

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)