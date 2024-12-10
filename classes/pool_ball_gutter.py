from classes.pool_ball import PoolBall
from config import pygame, pymunk, math
import config

class PoolBallGutter():
    def __init__(self, size, color, border_width, border_color, position):
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect(center=position)

        self.space = pymunk.Space()
        self.space.iterations = config.pool_ball_gutter_space_iterations
        self.space.gravity = config.pool_ball_gutter_space_gravity
        self.space.damping = config.pool_ball_gutter_space_damping
        self.space.sleep_time_threshold = config.pool_ball_gutter_space_sleep_time_threshold
        self.debug_draw = config.pool_ball_gutter_space_debug_draw
        self.space_draw_options = None

        if self.debug_draw:
            self.space_draw_options = pymunk.pygame_util.DrawOptions(self.surface)

        self.balls = []
        self.border_elasticity = config.pool_ball_gutter_border_elasticity
        self.border_friction = config.pool_ball_gutter_border_friction
        self.border_segments = []


    def on_init(self):
        self.surface.fill(self.color)
        static_body = self.space.static_body

        # left gutter
        start_pos = (self.border_width/2 - 1, 0)
        end_pos = (self.border_width/2 - 1, self.rect.height)
        segment = pymunk.Segment(static_body, start_pos, end_pos, self.border_width/2)
        segment.elasticity = self.border_elasticity
        segment.friction = self.border_friction
        self.border_segments.append(segment)

        # right gutter
        start_pos = (self.rect.width - self.border_width/2, 0)
        end_pos = (self.rect.width - self.border_width/2, self.rect.height)
        segment = pymunk.Segment(static_body, start_pos, end_pos, self.border_width/2)
        segment.elasticity = self.border_elasticity
        segment.friction = self.border_friction
        self.border_segments.append(segment)

        # bottom gutter
        start_pos = (0, self.rect.height - self.border_width/2)
        end_pos = (self.rect.width - self.border_width/2, self.rect.height - self.border_width/2)
        segment = pymunk.Segment(static_body, start_pos, end_pos, self.border_width/2)
        segment.elasticity = self.border_elasticity
        segment.friction = self.border_friction
        self.border_segments.append(segment)

        self.space.add(*self.border_segments)

    def add_ball(self, ball: PoolBall):
        ball.shape.body.position = ((self.rect.width/2), ball.radius)
        ball.body.velocity = (0, 0)
        ball.body.angular_velocity = 0
        self.space.add(ball.shape.body, ball.shape)
        self.balls.append(ball)

    def update(self):
        for _ in range(config.time_dt_steps):
            self.space.step(config.time_dt / config.time_dt_steps)

        for _ in self.balls:
            _.update()
            

    def draw(self, surface: pygame.Surface):
        # draw gutter
        self.surface.fill(self.color)
        
        # draw borders
        for segment in self.border_segments:
            pygame.draw.line(self.surface, self.border_color, segment.a, segment.b, self.border_width)


        for _ in self.balls:
            _.draw(self.surface)

        if self.debug_draw:
            self.space.debug_draw(self.space_draw_options)

        surface.blit(self.surface, self.rect)