from re import S
from config import pygame, pymunk, pool_ball_gutter_config
import config

from classes.pool_ball import PoolBall
from classes.draw_mode import DrawMode
from classes.media_manager import MediaManager

class PoolBallGutter():
    def __init__(self, position, media_manager: MediaManager):
        # Config Values
        size = pool_ball_gutter_config.pool_ball_gutter_size
        DM_RAW_color = pool_ball_gutter_config.pool_ball_gutter_DM_RAW_color
        DM_RAW_border_color = pool_ball_gutter_config.pool_ball_gutter_DM_RAW_border_color
        border_width = pool_ball_gutter_config.pool_ball_gutter_border_width
        draw_mode = pool_ball_gutter_config.pool_ball_gutter_draw_mode
        space_iterations = pool_ball_gutter_config.pool_ball_gutter_space_iterations
        space_gravity = pool_ball_gutter_config.pool_ball_gutter_space_gravity
        space_damping = pool_ball_gutter_config.pool_ball_gutter_space_damping
        space_sleep_time_threshold = pool_ball_gutter_config.pool_ball_gutter_space_sleep_time_threshold
        border_elasticity = pool_ball_gutter_config.pool_ball_gutter_border_elasticity
        border_friction = pool_ball_gutter_config.pool_ball_gutter_border_friction

        self.media_manager = media_manager
        self.draw_mode = draw_mode
        self.size = size
        self.position = position
        self.raw_color = DM_RAW_color
        self.raw_border_color = DM_RAW_border_color
        self.border_width = border_width

        self.raw_surface = None
        self.raw_rect = None
        self.rich_surface = None
        self.rich_rect = None
        
        self.space = pymunk.Space()
        self.space.iterations = space_iterations
        self.space.gravity = space_gravity
        self.space.damping = space_damping
        self.space.sleep_time_threshold = space_sleep_time_threshold
        self.space_draw_options = None

        self.balls = []
        self.border_elasticity = border_elasticity
        self.border_friction = border_friction
        self.border_shapes = []


    def on_init(self):
        self.raw_surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        self.raw_rect = self.raw_surface.get_rect(center=self.position)

        if self.draw_mode in DrawMode.RICH:
            media_path = pool_ball_gutter_config.pool_ball_gutter_DM_RICH_media
            rich_surface = self.media_manager.get(media_path, convert_alpha=True)
            if not rich_surface:
                print('No gutter img')
                return
            
            self.rich_surface = pygame.transform.scale(rich_surface, self.size)
            self.rich_rect = self.rich_surface.get_rect(center=self.position)

        if self.draw_mode in DrawMode.PHYSICS:
            self.space_draw_options = pymunk.pygame_util.DrawOptions(self.raw_surface)

        self.add_physical_borders()

    def add_physical_borders(self):
        static_body = self.space.static_body

        # left gutter
        points = [
            (0, 0),
            (self.border_width, 0),
            (self.border_width, self.size[1]),
            (0, self.size[1])
        ]
        shape = pymunk.Poly(static_body, points)
        shape.elasticity = self.border_elasticity
        shape.friction = self.border_friction
        self.border_shapes.append(shape)

        # right gutter
        points = [
            (self.size[0]-self.border_width, 0),
            (self.size[0], 0),
            (self.size[0], self.size[1]),
            (self.size[0]-self.border_width, self.size[1])
        ]
        shape = pymunk.Poly(static_body, points)
        shape.elasticity = self.border_elasticity
        shape.friction = self.border_friction
        self.border_shapes.append(shape)

        # bottom gutter
        points = [
            (0, self.size[1]-self.border_width),
            (self.size[0], self.size[1]-self.border_width),
            (self.size[0], self.size[1]),
            (0, self.size[1])
        ]
        shape = pymunk.Poly(static_body, points)
        shape.elasticity = self.border_elasticity
        shape.friction = self.border_friction
        self.border_shapes.append(shape)

        self.space.add(*self.border_shapes)

    def add_ball(self, ball: PoolBall):
        ball.shape.body.position = ((self.size[0]/2), ball.radius)
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
        self.raw_surface.fill((0,0,0,0))

        outline_width = 0
        if self.draw_mode in DrawMode.WIREFRAME:
            outline_width = pool_ball_gutter_config.pool_ball_gutter_DM_WIREFRAME_thickness

        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME | DrawMode.PHYSICS:
            # draw gutter
            rect = pygame.Rect(0, 0, self.size[0], self.size[1])
            pygame.draw.rect(self.raw_surface, self.raw_color, rect, outline_width)

            if self.draw_mode in DrawMode.WIREFRAME:
                # draw gutter poly points
                color = pygame.Color('black')
                radius = 2
                pygame.draw.circle(self.raw_surface, color, (0, 0), radius)
                pygame.draw.circle(self.raw_surface, color, (self.raw_rect.width, 0), radius)
                pygame.draw.circle(self.raw_surface, color, (self.raw_rect.width, self.raw_rect.height), radius)
                pygame.draw.circle(self.raw_surface, color, (0, self.raw_rect.height), radius)

            # draw borders
            for shape in self.border_shapes:
                points = shape.get_vertices()
                pygame.draw.polygon(self.raw_surface, self.raw_border_color, points, outline_width)
        
        if self.draw_mode in DrawMode.PHYSICS:
            self.space.debug_draw(self.space_draw_options)
                          
        if self.draw_mode in DrawMode.RICH:
            surface.blit(self.rich_surface, self.rich_rect)

        for _ in self.balls:
            _.draw(self.raw_surface)

        surface.blit(self.raw_surface, self.raw_rect)
        
    