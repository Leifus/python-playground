from classes.configs.game_space_config import GameSpaceConfig
from config import pygame, pymunk, pool_ball_gutter_config
from classes.game.pool_ball import PoolBall
from classes.enums.draw_mode_enum import DrawModeEnum
from classes.common.media_manager import MediaManager
from classes.common.helper_methods import draw_poly_points_around_rect
from globals import media_manager

class PoolBallGutter(pygame.sprite.Sprite):
    def __init__(self, position, space_config: GameSpaceConfig):
        pygame.sprite.Sprite.__init__(self)
        
        self.space_config: GameSpaceConfig = space_config
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

        self.position = position

        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)
        self.gutter_surface = None
        self.gutter_RICH_surface = None
        
        self.space_draw_options = None
        self.space = None

        self.ball_group = pygame.sprite.Group()
        self.border_shapes = []
        self.edge_barrier_vectors = []

    def setup_edge_barrier_vectors(self):
        # # left barrier
        # points = [
        #     (0, 0),
        #     (self.edge_barrier_width, 0),
        #     (self.edge_barrier_width, self.size[1]),
        #     (0, self.size[1])
        # ]
        # self.edge_barrier_vectors.append(points)

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


        # top barrier
        points = [
            (0, 0),
            (self.size[0], 0),
            (self.size[0], self.edge_barrier_width),
            (0, self.edge_barrier_width)
        ]
        self.edge_barrier_vectors.append(points)

    def setup_visuals(self):
        self.gutter_surface = self.surface.copy()

        if self.draw_mode in DrawModeEnum.Raw | DrawModeEnum.Wireframe | DrawModeEnum.Physics:
            if self.draw_mode in DrawModeEnum.Physics:
                self.space_draw_options = pymunk.pygame_util.DrawOptions(self.surface)

            outline_width = 0
            if self.draw_mode in DrawModeEnum.Wireframe:
                outline_width = self.WIREFRAME_outline_width
            
            # Main gutter
            rect = pygame.Rect(0, 0, self.size[0], self.size[1])
            pygame.draw.rect(self.gutter_surface, self.gutter_RAW_color, rect, outline_width)

            wireframe_point_color = pygame.Color('black')
            if self.draw_mode in DrawModeEnum.Wireframe:
                draw_poly_points_around_rect(self.gutter_surface, rect, wireframe_point_color, self.WIREFRAME_poly_point_radius)
                
            # Edge barriers
            for points in self.edge_barrier_vectors:
                rect = pygame.draw.polygon(self.gutter_surface, self.edge_barrier_RAW_color, points, outline_width)

            if self.draw_mode in DrawModeEnum.Wireframe:
                for points in self.edge_barrier_vectors:
                    draw_poly_points_around_rect(self.gutter_surface, rect, wireframe_point_color, self.WIREFRAME_poly_point_radius)
        elif self.draw_mode in DrawModeEnum.Rich:
            img = media_manager.get(self.gutter_RICH_media, convert_alpha=True)
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

    def clear_balls(self):
        for ball in self.ball_group:
            self.space.remove(ball.shape.body, ball.shape)
        self.ball_group.empty()

    def remove_ball(self, ball: PoolBall):
        if not self.ball_group.has(ball):
            return
        self.ball_group.remove(ball)
        self.space.remove(ball.shape.body, ball.shape)

    def add_ball(self, ball: PoolBall):
        ball.is_in_active_play = False
        ball.shape.body.position = (ball.radius + self.edge_barrier_width, ball.radius + self.edge_barrier_width)
        ball.body.velocity = (0, 0)
        ball.body.angular_velocity = 0
        self.space.add(ball.shape.body, ball.shape)
        self.ball_group.add(ball)

    def update(self, *args, **kwargs):
        for _ in range(self.space_config.dt_steps):
            self.space.step(self.space_config.dt / self.space_config.dt_steps)

        self.ball_group.update()
        return super().update(*args, **kwargs)

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        self.surface.blit(self.gutter_surface, (0, 0))

        self.ball_group.draw(self.surface)
        
        if self.draw_mode in DrawModeEnum.Physics:
            self.space.debug_draw(self.space_draw_options)

        surface.blit(self.surface, self.rect)
        
    