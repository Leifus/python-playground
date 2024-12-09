from config import COLLISION_TYPE_POOL_TABLE_CUSHION, pygame, pymunk

class PoolTableCushion():
    def __init__(self, size, color, elasticity, friction, position):
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=position)
        self.position = position
        self.elasticity = elasticity
        self.friction = friction
        self.color = color
        self.poly_points = [(0,0), (self.rect.width, 0), (self.rect.width, self.rect.height), (0, self.rect.height)]

        self.body = None
        self.shape = None

    def on_init(self, space, body_iter):
        pygame.draw.polygon(self.surface, self.color, self.poly_points)

        mass = 10
        moment = 10
        self.body = pymunk.Body(mass, moment)
        self.body.position = (self.position[0] - (self.rect.width/2), self.position[1] - (self.rect.height/2))
        self.shape = pymunk.Poly(self.body, self.poly_points)
        self.shape.collision_type = COLLISION_TYPE_POOL_TABLE_CUSHION + body_iter
        space.add(self.body, self.shape)

    def update(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)
