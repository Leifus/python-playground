from classes.draw_mode_enum import DrawModeEnum
from classes.game_space_config import GameSpaceConfig
from classes.game_tables.game_table import GameTable
from classes.pool_ball import PoolBall
from classes.pool_table_pocket import PoolTablePocket
from config import pygame, pymunk, Dict

class CircleGameTable(GameTable):
    def __init__(self, radius, position, space_config: GameSpaceConfig, draw_mode: DrawModeEnum):
        size = (radius*2, radius*2)
        super(CircleGameTable, self).__init__(size=size, position=position, space_config=space_config, draw_mode=draw_mode)
        
        self.radius = radius
        
        self.setup_visuals()
        self.redraw()

    def redraw(self):
        size = (self.radius*2, self.radius*2)
        self.image = pygame.transform.scale(self.orig_image, size)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def setup_visuals(self):
        size = (self.radius*2, self.radius*2)
        self.orig_image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.orig_image.get_rect(center=self.position)

        color = pygame.Color('darkorange1')
        position = (self.radius, self.radius)
        pygame.draw.circle(self.orig_image, color, position, self.radius)

    # def draw(self, surface: pygame.Surface):
    #     surface.blit(self.image, self.rect)
    