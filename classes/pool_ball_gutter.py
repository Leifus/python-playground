from config import pygame, pymunk, pool_ball_gutter_config
import config
from classes.pool_ball import PoolBall
from classes.draw_mode import DrawMode
from classes.media_manager import MediaManager
from classes.__helpers__ import draw_poly_points_around_rect

class PoolBallGutter():
    def __init__(self, position, media_manager: MediaManager):
        self.draw_mode = pool_ball_gutter_config.pool_ball_gutter_draw_mode
        self.size = pool_ball_gutter_config.pool_ball_gutter_size
        self.gutter_RAW_color = pool_ball_gutter_config.pool_ball_gutter_DM_RAW_color
        self.edge_barrier_RAW_color = pool_ball_gutter_config.pool_ball_gutter_edge_barrier_DM_RAW_color
        self.edge_barrier_width = pool_ball_gutter_config.pool_ball_gutter_edge_barrier_width
        self.space_iterations = pool_ball_gutter_config.pool_ball_gutter_space_iterations
        self.space_gravity = pool_ball_gutter_config.pool_ball_gutter_space_gravity
        self.space_damping = pool_ball_gutter_config.pool_ball_gutter_space_damping
        self.space_sleep_time_threshold = pool_ball_gutter_config.pool_ball_gutter_space_sleep_time_threshold
        self.edge_barrier_elasticity = pool_ball_gutter_config.pool_ball_gutter_edge_barrier_elasticity
        self.edge_barrier_friction = pool_ball_gutter_config.pool_ball_gutter_edge_barrier_friction
        self.WIREFRAME_outline_width = pool_ball_gutter_config.pool_ball_gutter_DM_WIREFRAME_outline_width
        self.WIREFRAME_poly_point_radius = pool_ball_gutter_config.pool_ball_gutter_DM_WIREFRAME_poly_point_radius
        self.gutter_RICH_media = pool_ball_gutter_config.pool_ball_gutter_DM_RICH_media

        self.media_manager = media_manager
        self.position = position

        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)
        self.gutter_surface = None
        self.gutter_RICH_surface = None
        
        self.space_draw_options = None
        self.space = None

        self.balls = []
        self.border_shapes = []
        self.edge_barrier_vectors = []

    def setup_edge_barrier_vectors(self):
        # left barrier
        points = [
            (0, 0),
            (self.edge_barrier_width, 0),
            (self.edge_barrier_width, self.size[1]),
            (0, self.size[1])
        ]
        self.edge_barrier_vectors.append(points)

        # right barrier
        points = [
            (self.size[0]-self.edge_barrier_width, 0),
            (self.size[0], 0),
            (self.size[0], self.size[1]),
            (self.size[0]-self.edge_barrier_width, self.size[1])
        ]
        self.edge_barrier_vectors.append(points)

        # bottom barrier
        points = [
            (0, self.size[1]-self.edge_barrier_width),
            (self.size[0], self.size[1]-self.edge_barrier_width),
            (self.size[0], self.size[1]),
            (0, self.size[1])
        ]
        self.edge_barrier_vectors.append(points)

    def setup_visuals(self):
        self.gutter_surface = self.surface.copy()

        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME | DrawMode.PHYSICS:
            if self.draw_mode in DrawMode.PHYSICS:
                self.space_draw_options = pymunk.pygame_util.DrawOptions(self.surface)

            outline_width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width
            
            # Main gutter
            rect = pygame.Rect(0, 0, self.size[0], self.size[1])
            pygame.draw.rect(self.gutter_surface, self.gutter_RAW_color, rect, outline_width)

            wireframe_point_color = pygame.Color('black')
            if self.draw_mode in DrawMode.WIREFRAME:
                draw_poly_points_around_rect(self.gutter_surface, rect, wireframe_point_color, self.WIREFRAME_poly_point_radius)
                
            # Edge barriers
            for points in self.edge_barrier_vectors:
                rect = pygame.draw.polygon(self.gutter_surface, self.edge_barrier_RAW_color, points, outline_width)

            if self.draw_mode in DrawMode.WIREFRAME:
                for points in self.edge_barrier_vectors:
                    draw_poly_points_around_rect(self.gutter_surface, rect, wireframe_point_color, self.WIREFRAME_poly_point_radius)
        elif self.draw_mode in DrawMode.RICH:
            img = self.media_manager.get(self.gutter_RICH_media, convert_alpha=True)
            if not img:
                print('No gutter img')
                return
            
            self.gutter_RICH_surface = pygame.transform.scale(img, self.size)
            self.gutter_surface.blit(self.gutter_RICH_surface, (0, 0))

    def setup_physical_space(self):
        self.space = pymunk.Space()
        self.space.iterations = self.space_iterations
        self.space.gravity = self.space_gravity
        self.space.damping = self.space_damping
        self.space.sleep_time_threshold = self.space_sleep_time_threshold

        static_body = self.space.static_body
        
        for points in self.edge_barrier_vectors:
            shape = pymunk.Poly(static_body, points)
            shape.elasticity = self.edge_barrier_elasticity
            shape.friction = self.edge_barrier_friction
            self.space.add(shape)

    def on_init(self):
        self.setup_edge_barrier_vectors()
        self.setup_visuals()
        self.setup_physical_space()

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
        self.surface.fill((0,0,0,0))

        self.surface.blit(self.gutter_surface, (0, 0))

        for _ in self.balls:
            _.draw(self.surface)
        
        if self.draw_mode in DrawMode.PHYSICS:
            self.space.debug_draw(self.space_draw_options)

        surface.blit(self.surface, self.rect)
        
    