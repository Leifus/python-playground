
from classes.common.game_sprite import GameSprite
from config import pymunk, pygame, math
from globals import media_manager


class FoodSource(GameSprite):
    def __init__(self, size, position):
        super(FoodSource, self).__init__()

        self.size = size
        self.position = position

        self.body: pymunk.Body = None
        self.shape: pymunk.Shape = None
        self.mass = 10
        self.elasticity = 0.1
        self.friction = 0.9
        self.is_active = False

        self.create_visuals()
        self.redraw()
        self.construct_physical_body()

    def redraw(self):
        scaled_image = pygame.transform.scale(self.orig_image, self.size)
        rotated_image = pygame.transform.rotate(scaled_image, self.angle).convert_alpha()
        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.position)

    def create_visuals(self):
        media = 'terrain_tiles/SandTile.png'
        self.orig_image = media_manager.get(media, convert=True)
        color = (0,0,0,255)
        width = 2
        pygame.draw.rect(self.orig_image, color, self.orig_image.get_rect(), width)

    def construct_physical_body(self):
        body_type = pymunk.Body.DYNAMIC
        moment = pymunk.moment_for_box(self.mass, self.size)
        self.body = pymunk.Body(self.mass, moment, body_type=body_type)
        self.body.position = self.position
        self.shape = pymunk.Poly.create_box(self.body, self.size)
        self.shape.elasticity = self.elasticity
        self.shape.friction = self.friction
        
    def update(self, time_lapsed, *args, **kwargs):
        redraw = False
        if self.position != self.body.position:
            self.position = self.body.position
            redraw = True

        angle = -round(math.degrees(self.body.angle),3)
        if self.angle != angle:
            self.angle = angle
            redraw = True

        if redraw:
            self.redraw()

        return super().update(*args, **kwargs)