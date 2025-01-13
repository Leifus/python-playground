
from classes.common.game_sprite import GameSprite
from config import pymunk, pygame

class MainContainmentBox(GameSprite):
    def __init__(self, size, position):
        super(MainContainmentBox, self).__init__()

        self.size = size
        self.position = position
        self.body: pymunk.Body = None
        self.shapes: list[pymunk.Shape] = []
        self.elasticity = 0.99
        self.friction = 0.9
        self.wall_thickness = 15
        self.wall_vertices = [
            [ # Top
                (0,0),
                (self.size[0], 0),
                (self.size[0], self.wall_thickness),
                (0, self.wall_thickness)
            ],
            [ # Bottom
                (0, self.size[1]-self.wall_thickness),
                (self.size[0], self.size[1]-self.wall_thickness),
                (self.size[0], self.size[1]),
                (0, self.size[1])
            ],
            [ # Right
                (self.size[0]-self.wall_thickness, 0),
                (self.size[0], 0),
                (self.size[0], self.size[1]),
                (self.size[0]-self.wall_thickness, self.size[1])
            ],
            [ # Left
                (0, 0),
                (self.wall_thickness, 0),
                (self.wall_thickness, self.size[1]),
                (0, self.size[1])
            ]
        ]

        self.construct_physical_body()
        self.redraw()

    def redraw(self):
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.image.fill('white')
        self.rect = self.image.get_rect(center=self.position)

        color = pygame.Color('gray60')
        for vertices in self.wall_vertices:
            # rect = pygame.Rect(vertices[0], vertices[1], vertices[2], vertices[3])
            pygame.draw.polygon(self.image, color, vertices)


    def construct_physical_body(self):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = self.position
        position_transform = pymunk.Transform(tx=-self.size[0]/2, ty=-self.size[1]/2)

        for vertices in self.wall_vertices:
            shape = pymunk.Poly(self.body, vertices, position_transform)
            shape.elasticity = self.elasticity
            shape.friction = self.friction
            self.shapes.append(shape)