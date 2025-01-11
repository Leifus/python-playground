
from classes.common.game_sprite import GameSprite
from config import pymunk

class MainContainmentBox(GameSprite):
    def __init__(self, size, position):
        super(MainContainmentBox, self).__init__()

        self.size = size
        self.position = position
        self.body: pymunk.Body = None
        self.shapes: list[pymunk.Shape] = []

        self.construct_physical_body()

    def construct_physical_body(self):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = self.position
        thickness = 15

        # Top
        vertices = [
            (0,0),
            (self.size[0], 0),
            (self.size[0], thickness),
            (0, thickness)
        ]
        shape = pymunk.Poly(self.body, vertices)
        self.shapes.append(shape)

        # Bottom
        vertices = [
            (0, self.size[1]-thickness),
            (self.size[0], self.size[1]-thickness),
            (self.size[0], self.size[1]),
            (0, self.size[1])
        ]
        shape = pymunk.Poly(self.body, vertices)
        self.shapes.append(shape)

        # Right
        vertices = [
            (self.size[0]-thickness, 0),
            (self.size[0], 0),
            (self.size[0], self.size[1]),
            (self.size[0]-thickness, self.size[1])
        ]
        shape = pymunk.Poly(self.body, vertices)
        self.shapes.append(shape)

        # Left
        vertices = [
            (0, 0),
            (thickness, 0),
            (thickness, self.size[1]),
            (0, self.size[1])
        ]
        shape = pymunk.Poly(self.body, vertices)
        self.shapes.append(shape)