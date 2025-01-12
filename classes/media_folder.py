
from classes.common.game_sprite import GameSprite
from classes.media_item import MediaItem
from config import pygame

class MediaFolder(GameSprite):
    def __init__(self, folder_name, position, housing_width):
        super(MediaFolder, self).__init__()

        self.folder_name = folder_name
        self.position = position
        self.housing_width = housing_width
        self.media_items = pygame.sprite.Group()
        self.hovered_item: MediaItem = None
        
        self.font_size = 14
        self.font_color = pygame.Color('black')
        self.font = pygame.font.Font('freesansbold.ttf', self.font_size)
        
        self.redraw()

    def redraw(self):
        txt_surface = self.font.render(self.folder_name, True, self.font_color, None)
        txt_rect = txt_surface.get_rect()
        self.image = pygame.Surface((self.housing_width, txt_rect.height), pygame.SRCALPHA)
        
        self.image.blit(txt_surface, txt_rect)
        self.rect = self.image.get_rect(topleft=self.position)

    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        self.hovered_item = None
        for item in self.media_items:
            item: MediaItem
            item.on_event(parent_mouse_position, event)
            if item.is_hovered:
                self.hovered_item = item


    def draw(self, surface: pygame.Surface):
        self.media_items.draw(surface)
        surface.blit(self.image, self.rect)
