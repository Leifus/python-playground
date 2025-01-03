
from classes.common.game_sprite import GameSprite
from config import pymunk, pygame, math
from globals import media_manager


class WaterSource(GameSprite):
    def __init__(self, size, position, edge_vectors):
        super(WaterSource, self).__init__()

        self.size = size
        self.position = position
        self.edge_vectors = edge_vectors
        self.is_active = False
        self.body: pymunk.Body = None
        self.shape: pymunk.Shape = None

        # self.create_default_surface()
        self.create_visuals()
        self.redraw()
        self.construct_physical_body()

    def redraw(self):
        scaled_image = pygame.transform.scale(self.orig_image, self.size)
        poly_image = pygame.Surface(self.size, pygame.SRCALPHA)
        
        color = pygame.Color('blue')
        vects = []
        for _ in self.edge_vectors:
            vects.append((_[0] + self.size[0]/2, _[1] + self.size[1]/2))
        poly_rect = pygame.draw.polygon(poly_image, color, vects)
        poly_mask = pygame.mask.from_surface(poly_image)
        masked_image = poly_mask.to_surface(setsurface=scaled_image, unsetcolor=None)

        self.image = masked_image
        self.rect = self.image.get_rect(center=self.position)

    def create_visuals(self):
        media = 'terrain_tiles/WaterTile.png'
        self.orig_image = media_manager.get(media, convert=True)

    def construct_physical_body(self):
        body_type = pymunk.Body.STATIC
        self.body = pymunk.Body(body_type=body_type)
        self.body.position = self.position
        self.shape = pymunk.Poly(self.body, self.edge_vectors)
        