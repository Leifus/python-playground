from config import COLLISION_TYPE_POOL_BALL, pygame, pymunk
import config

POOL_BALL_TYPE_STRIPE = 1
POOL_BALL_TYPE_SPOT = 0
POOL_BALL_TYPE_8 = 8
POOL_BALL_TYPE_CUE = 7

class PoolBall():
    def __init__(self, type, position):
        self.type = type
        self.position = position
        self.radius = self.get_radius_by_type()
        self.color = self.get_color_by_type()
        self.surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=position)
        self.type = type
        self.mass = config.pool_ball_mass

        self.is_highlighted = False
        self.highlight_color = pygame.Color('red')

        self.body = None
        self.shape = None

    def _draw(self):
        pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)

        if self.is_highlighted:
            pygame.draw.circle(self.surface, self.highlight_color, (self.radius, self.radius), self.radius, 2)


    def on_init(self, space, body_iter):
        self._draw()
        
        inertia = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pymunk.Body(self.mass, inertia)
        self.body.position = self.position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.collision_type = COLLISION_TYPE_POOL_BALL + body_iter
        space.add(self.body, self.shape)

    def update(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)

    def highlight_position(self, show=True):
        self.is_highlighted = show
        self._draw()


    def get_radius_by_type(self):
        return config.pool_ball_radius

    def get_color_by_type(self):
        if self.type == POOL_BALL_TYPE_CUE:
            return config.pool_ball_cue_color
        elif self.type == POOL_BALL_TYPE_8:
            return config.pool_ball_8_color
        elif self.type == POOL_BALL_TYPE_SPOT:
            return config.pool_ball_spot_color
        elif self.type == POOL_BALL_TYPE_STRIPE:
            return config.pool_ball_stripe_color
        else:
            return (0, 255, 0)