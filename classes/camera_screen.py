from classes.camera import Camera
from config import pygame
from classes.game_sprite import GameSprite


class CameraScreen(GameSprite):
    def __init__(self, size, position, camera: Camera):
        super(CameraScreen, self).__init__()

        self.size = size
        self.position = position
        self.camera = camera

        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)

        self.housing_image: pygame.Surface | None = None

        self.setup_visuals()
        self.redraw()

    def setup_visuals(self):
        # Housing
        border_width = 5
        rect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        color = pygame.Color('black')
        self.housing_image = self.image.copy()
        self.housing_image.get_rect(center=(self.size[0]/2, self.size[1]/2))
        pygame.draw.rect(self.housing_image, color, rect, border_width)

    def redraw(self):
        self.image.fill((0,0,0,0))

        # Camera
        camera_image = self.camera.target_surface.subsurface(self.camera.rect)
        camera_image.set_clip(self.rect)

        self.housing_image.set_alpha(120)

        blit_sequence = [
            (camera_image, (0,0)),
            (self.housing_image, (0,0))
        ]
        self.image.blits(blit_sequence)
        
        
    def update(self, *args, **kwargs):
        self.camera.update()
        if self.camera.has_changed:
            self.redraw()

        return super().update(*args, **kwargs)