from config import pygame, path_tracer_config
from classes.media_manager import MediaManager
from classes.__helpers__ import aspect_scale
from classes.draw_mode_enum import DrawModeEnum

class PathTracer():
    def __init__(self, size, media_manager: MediaManager):
        self.draw_mode = path_tracer_config.path_tracer_draw_mode
        self.point_radius = path_tracer_config.path_tracer_point_radius
        self.point_a_RAW_color = path_tracer_config.path_tracer_point_a_DM_RAW_color
        self.point_b_RAW_color = path_tracer_config.path_tracer_point_b_DM_RAW_color
        self.line_RAW_color = path_tracer_config.path_tracer_line_DM_RAW_color
        self.line_RAW_width = path_tracer_config.path_tracer_line_DM_RAW_width
        self.point_a_RICH_media = path_tracer_config.path_tracer_point_a_DM_RICH_media
        self.point_b_RICH_media = path_tracer_config.path_tracer_point_b_DM_RICH_media
        self.WIREFRAME_outline_width = path_tracer_config.path_tracer_DM_WIREFRAME_outline_width

        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=(0,0))
        self.point_a_surface = None
        self.point_b_surface = None
        self.point_a_RICH_surface = None
        self.point_b_RICH_surface = None

        self.media_manager = media_manager
        self.show = True

        self.point_a = None
        self.point_b = None

    def setup_visuals(self):
        self.point_a_surface = pygame.Surface((self.point_radius*2, self.point_radius*2), pygame.SRCALPHA)
        self.point_b_surface = pygame.Surface((self.point_radius*2, self.point_radius*2), pygame.SRCALPHA)

        if self.draw_mode in DrawModeEnum.RAW | DrawModeEnum.WIREFRAME:
            outline_width = 0
            if self.draw_mode in DrawModeEnum.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            # Point A
            pygame.draw.circle(self.point_a_surface, self.point_a_RAW_color, (self.point_radius, self.point_radius), self.point_radius, outline_width)

            # Point B
            pygame.draw.circle(self.point_b_surface, self.point_b_RAW_color, (self.point_radius, self.point_radius), self.point_radius, outline_width)

            # Path Line
            # pygame.draw.line(self.surface, self.line_RAW_color, self.point_a, self.point_b, self.line_RAW_width)
        elif self.draw_mode in DrawModeEnum.RICH:
            # Point A
            img = self.media_manager.get(self.point_a_RICH_media, convert_alpha=True)
            size = (self.point_radius*2, self.point_radius*2)
            img = aspect_scale(img, size)
            self.point_a_RICH_surface = img
            self.point_a_surface.blit(self.point_a_RICH_surface, (0, 0))

            # Point B
            img = self.media_manager.get(self.point_b_RICH_media, convert_alpha=True)
            img = aspect_scale(img, size)
            self.point_b_RICH_surface = img
            self.point_b_surface.blit(self.point_b_RICH_surface, (0, 0))

            # Path Line
            # ...

    def on_init(self):
        self.setup_visuals()

    def update(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        if self.show:
            if self.point_a is not None:
                self.surface.blit(self.point_a_surface, self.point_a_surface.get_rect(center=self.point_a))
            if self.point_b is not None:
                self.surface.blit(self.point_b_surface, self.point_b_surface.get_rect(center=self.point_b))
                
                if self.draw_mode in DrawModeEnum.RAW | DrawModeEnum.WIREFRAME:
                    # Draw Path Line
                    pygame.draw.line(self.surface, self.line_RAW_color, self.point_a, self.point_b, self.line_RAW_width)


        surface.blit(self.surface, (0,0))