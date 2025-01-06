from classes.common.game_sprite import GameSprite
from classes.image_panel import ImagePanel
from config import pygame
from globals import media_manager

class MainDrawSpace(GameSprite):
    def __init__(self, size, position):
        super(MainDrawSpace, self).__init__()

        self.size = size
        self.position = position
        self.poly_point_radius = 2
        self.scale = 1.0
        self.max_sprite_loading_size = (800,600)
        self.sprite_size = self.max_sprite_loading_size
        self.mouse_position = None
        self.sprite_position = None
        self.poly_points = []
        self.image_panels = pygame.sprite.Group()
        
        self.create_default_surface()
        self.setup_visuals()
        self.redraw()

    def setup_visuals(self):
        color = pygame.Color('cornsilk')
        self.orig_image.fill(color)

    def redraw(self):
        self.image = pygame.transform.scale(self.orig_image, self.size)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def add_image_panel(self, image_panel: ImagePanel):
        image_panel.parent_rect = self.rect
        self.image_panels.add(image_panel)

    def update(self, *args, **kwargs):
        self.image_panels.update()
            
        return super().update(*args, **kwargs)

    def on_event(self, event: pygame.event.Event):
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            mouse_x, mouse_y = event.pos
            self.mouse_position = pygame.Vector2(mouse_x - self.rect.left, mouse_y - self.rect.top)

        for panel in self.image_panels:
            panel: ImagePanel
            panel.on_event(self.mouse_position, event)

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        self.surface.blit(self.image, (0,0))

        for panel in self.image_panels:
            panel: ImagePanel
            panel.draw(self.surface)

        # # Right Side Info Panel
        # info_panel_size = (150, box_rect.height)
        # position = (box_rect.right, box_rect.top)
        # info_surface = pygame.Surface(info_panel_size, pygame.SRCALPHA)
        # info_rect = info_surface.get_rect(topleft=position)
        # fill_color = pygame.Color('white')
        # info_surface.fill(fill_color)
        # edge_color = pygame.Color('gray80')
        # width = 2
        # pygame.draw.rect(info_surface, edge_color, (0,0,info_rect.width, info_rect.height), width)

        # font_size = 11
        # info_font = pygame.font.Font('freesansbold.ttf', font_size)
        # font_color = pygame.Color('black')

        # # Info Panel Image Info
        # image_info_label = f'SIZE: {self.sprite_rect.width} x {self.sprite_rect.height}'
        # image_info_surface = info_font.render(image_info_label, True, font_color)
        # y_pos = 5
        # info_surface.blit(image_info_surface, (5, y_pos))

        # orig_rect = self.sprite_orig_image.get_rect()
        # image_info_label = f'ORIG SIZE: {orig_rect.width} x {orig_rect.height}'
        # image_info_surface = info_font.render(image_info_label, True, font_color)
        # y_pos += 15
        # info_surface.blit(image_info_surface, (5, y_pos))

        # # Info Panel Poly Points
        # # y_pos += 20
        # # for i, point in enumerate(self.poly_points):
        # #     point_label = str(point)
        # #     point_surface = info_font.render(point_label, True, font_color)
        # #     x = 5
        # #     y = y_pos + (i*(font_size+2))
        # #     info_surface.blit(point_surface, (x, y))

        # self.surface.blit(info_surface, info_rect)

        surface.blit(self.surface, self.rect)
