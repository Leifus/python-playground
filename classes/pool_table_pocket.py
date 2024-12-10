from config import pool_balls_config, pygame, pymunk

class PoolTablePocket():
    def __init__(self, radius, color, position):
        self.radius = radius
        self.surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=position)
        self.position = position
        self.color = color

        self.body = None
        self.shape = None

    def on_init(self, space: pymunk.Space, body_iter):
        pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)

        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = self.position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.sensor = True
        self.shape.collision_type = pool_balls_config.COLLISION_TYPE_POOL_TABLE_POCKET + body_iter
        space.add(self.body, self.shape)

    def update(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)