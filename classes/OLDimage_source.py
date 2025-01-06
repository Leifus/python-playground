from classes.common.game_sprite import GameSprite
from classes.common.helper_methods import aspect_scale
from classes.enums.image_source_display_mode_enum import ImageSourceDisplayModeEnum
from globals import media_manager
from config import pygame



class ImageSource(GameSprite):
    def __init__(self, position, image_path):
        super(ImageSource, self).__init__()

        self.position = position
        self.image_path = image_path
        self.size = (300, 300)
        self.orig_image = media_manager.get(self.image_path, convert_alpha=True)
        self.display_mode = ImageSourceDisplayModeEnum.Rich
        self.do_redraw = False

        self.redraw()

    def scale_by(self, scale):
        scale_by = 1.0 + scale
        self.size = (self.size[0] * scale_by, self.size[1] * scale_by)
        self.do_redraw = True

    def show_image(self):
        self.display_mode = ImageSourceDisplayModeEnum.Rich
        self.do_redraw = True

    def show_mask(self):
        self.display_mode = ImageSourceDisplayModeEnum.Mask
        self.do_redraw = True

    def show_outline(self):
        self.display_mode = ImageSourceDisplayModeEnum.Outline
        self.do_redraw = True

    def update(self):
        if self.do_redraw:
            self.redraw()
            self.do_redraw = False

        return super().update()
    
    def redraw(self):
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)

        orig_image_rect = self.orig_image.get_rect()

        if orig_image_rect.width > self.size[0] or orig_image_rect.height > self.size[1]:
            self.surface = aspect_scale(self.orig_image, self.size).convert_alpha()
        else:
            self.surface = self.orig_image.copy()

        self.rect = self.surface.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.surface)

        if self.display_mode is ImageSourceDisplayModeEnum.Mask:
            self.surface = self.mask.to_surface(setcolor=(0,0,0), unsetcolor=None)
        elif self.display_mode is ImageSourceDisplayModeEnum.Outline:
            self.surface.fill((0,0,0,0))
            mask_outline = self.mask.outline(5)
            line_color = pygame.Color('red')
            point_color = pygame.Color('blue')
            point_radius = 3
            line_width = 2
            pygame.draw.polygon(self.surface, line_color, mask_outline, line_width)
            for point in mask_outline:
                pygame.draw.circle(self.surface, point_color, point, point_radius)

        # #draw box
        # rect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        # pygame.draw.rect(self.surface, (0,0,0), rect, 2)

        self.image = self.surface
