from config import pygame
from classes.game_sprite import GameSprite


class Camera(GameSprite):
    def __init__(self, target_surface: pygame.Surface, size, position):
        super(GameSprite, self).__init__()
        
        self.target_surface = target_surface
        self.size = size
        self.position = position
        self.has_changed = False

        self.target: GameSprite | None = None
        self.target_offset_rect: pygame.Rect | None = None

        self.setup_visuals()

    def setup_visuals(self):
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)
        self.redraw()

    def track_target(self, target: GameSprite, offset_rect: pygame.Rect = None):
        self.target_offset_rect = offset_rect
        self.target = target

    def redraw(self):
        self.image.fill((0,0,0,50))

    def update(self, *args, **kwargs):
        if self.target:
            x, y = self.target.position
            offset_x, offset_y = (0,0)
            if self.target_offset_rect:
                offset_x, offset_y = (self.target_offset_rect.left, self.target_offset_rect.top)

            target_position = (x + offset_x, y + offset_y)
            if self.position != target_position:
                self.position = target_position
                self.rect = self.image.get_rect(center=self.position)
                self.has_changed = True
                self.redraw()

        return super().update(*args, **kwargs)