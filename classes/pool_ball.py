from config import COLLISION_TYPE_POOL_BALL, DrawMode, pygame, pymunk
import config
from classes.media_manager import MediaManager

POOL_BALL_TYPE_STRIPE = 1
POOL_BALL_TYPE_SPOT = 0
POOL_BALL_TYPE_8 = 8
POOL_BALL_TYPE_CUE = 7

class PoolBall():
    def __init__(self, type, position, media_manager: MediaManager):
        self.media_manager = media_manager
        self.type = type
        self.position = position
        self.angle = 0
        self.draw_mode = config.pool_ball_draw_mode
        self.type = type
        self.mass = config.pool_ball_mass
        self.max_force = config.pool_ball_max_force
        self.is_highlighted = False
        self.highlight_color = pygame.Color('red')
        self.body = None
        self.shape = None
        self.is_on_table = False
        self.is_moving = False
        self.radius = config.pool_ball_radius

        self.raw_surface = None
        self.raw_rect = None
        self.raw_color = self.get_color_by_type()
        self.wireframe_thickness = config.pool_ball_draw_mode_wireframe_thickness
        
        self.rich_surface = None
        self.rich_rect = None

    def on_init(self, space, body_iter):        
        inertia = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pymunk.Body(self.mass, inertia)
        self.body.position = self.position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.collision_type = COLLISION_TYPE_POOL_BALL + body_iter
        self.shape.elasticity = config.pool_ball_elasticity
        self.shape.friction = config.pool_ball_friction
        space.add(self.body, self.shape)

        if DrawMode.RAW in self.draw_mode or DrawMode.WIREFRAME in self.draw_mode:
            padding = 0
            if DrawMode.WIREFRAME in self.draw_mode:
                padding = config.pool_ball_draw_mode_wireframe_thickness*2

            self.raw_surface = pygame.Surface((self.radius*2+padding, self.radius*2+padding), pygame.SRCALPHA)
        elif DrawMode.RICH in self.draw_mode:
            img = self.get_rich_surface_by_type()
            if not img:
                print('No img:', self.type)
                return
            
            self.rich_surface = pygame.transform.scale(img, (self.radius*2, self.radius*2))
            self.rich_rect = self.rich_surface.get_rect(center=self.position)

        self.is_on_table = True
        
        self._draw()

    def _draw(self):
        if DrawMode.RAW in self.draw_mode or DrawMode.WIREFRAME in self.draw_mode:
            width = 0
            if DrawMode.WIREFRAME in self.draw_mode:
                width = self.wireframe_thickness
            pygame.draw.circle(self.raw_surface, self.raw_color, (self.radius, self.radius), self.radius, width)

            # if self.is_highlighted:
            #     pygame.draw.circle(self.raw_surface, self.highlight_color, (self.radius, self.radius), self.radius, 2)            

    def update(self):
        self.angle = self.body.angle
        self.position = self.body.position
        
        if DrawMode.RAW in self.draw_mode or DrawMode.WIREFRAME in self.draw_mode:
            self.raw_rect = self.raw_surface.get_rect(center=self.body.position)
        elif DrawMode.RICH in self.draw_mode:
            self.rich_rect = self.rich_surface.get_rect(center=self.body.position)

        stop_force_margin = 3
        x_v = self.body.velocity[0]
        y_v = self.body.velocity[1]
        if not self.body.is_sleeping and (x_v > -stop_force_margin and x_v < stop_force_margin) and (y_v > -stop_force_margin and y_v < stop_force_margin):
            # force stop the ball
            self.body._set_velocity((0, 0))
            self.is_moving = False
        else:
            self.is_moving = True

    def draw(self, surface: pygame.Surface):
        if DrawMode.RAW in self.draw_mode or DrawMode.WIREFRAME in self.draw_mode:
            surface.blit(self.raw_surface, self.raw_rect)
        elif DrawMode.RICH in self.draw_mode:
            surface.blit(self.rich_surface, self.rich_rect)
            

    def highlight_position(self, show=True):
        self.is_highlighted = show
        self._draw()

    def set_force_at_point(self, force):
        force_x = force[0]
        force_y = force[1]
        if force_x > 0 and force_x > self.max_force:
            force_x = self.max_force
        elif force_x < 0 and force_x < -self.max_force:
            force_x = -self.max_force
        if force_y > 0 and force_y > self.max_force:
            force_y = self.max_force
        elif force_y < 0 and force_y < -self.max_force:
            force_y = -self.max_force
        self.body.apply_force_at_local_point((force_x, force_y))

    def get_rich_surface_by_type(self):
        media_path = None
        if self.type == POOL_BALL_TYPE_CUE:
            media_path = config.pool_ball_DM_RICH_cue_media_path
        elif self.type == POOL_BALL_TYPE_8:
            media_path = config.pool_ball_DM_RICH_8_media_path
        elif self.type == POOL_BALL_TYPE_SPOT:
            media_path = config.pool_ball_DM_RICH_spot_media_path
        elif self.type == POOL_BALL_TYPE_STRIPE:
            media_path = config.pool_ball_DM_RICH_stripe_media_path
        
        if media_path is None:
            return None
        
        media_path = f'{config.pool_ball_DM_RICH_media_path}/{media_path}'
        rich_surface = self.media_manager.get_image(media_path, convert_alpha=True)
        return rich_surface

    def get_color_by_type(self):
        if self.type == POOL_BALL_TYPE_CUE:
            return config.pool_ball_DM_RAW_cue_color
        elif self.type == POOL_BALL_TYPE_8:
            return config.pool_ball_DM_RAW_8_color
        elif self.type == POOL_BALL_TYPE_SPOT:
            return config.pool_ball_DM_RAW_spot_color
        elif self.type == POOL_BALL_TYPE_STRIPE:
            return config.pool_ball_DM_RAW_stripe_color
        else:
            return (0, 255, 0)