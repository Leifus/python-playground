from config import pool_balls_config, pygame, pymunk

from classes.draw_mode import DrawMode
from classes.media_manager import MediaManager

POOL_BALL_TYPE_STRIPE = 1
POOL_BALL_TYPE_SPOT = 0
POOL_BALL_TYPE_8 = 8
POOL_BALL_TYPE_CUE = 7

class PoolBall():
    def __init__(self, type, identifier, position, media_manager: MediaManager):
        # Config Values
        self.draw_mode = pool_balls_config.pool_ball_draw_mode
        self.mass = pool_balls_config.pool_ball_mass
        self.max_force = pool_balls_config.pool_ball_max_force
        self.radius = pool_balls_config.pool_ball_radius
        self.wireframe_thickness = pool_balls_config.pool_ball_draw_mode_wireframe_thickness

        # Arg Values
        self.media_manager = media_manager
        self.type = type
        self.identifier = identifier
        self.position = position
        self.type = type

        # Default Values
        self.highlight_color = pygame.Color('red')
        self.angle = 0
        self.is_highlighted = False
        self.body = None
        self.shape = None
        self.is_on_table = False
        self.is_moving = False
        self.raw_surface = None
        self.raw_rect = None
        self.raw_color = self.get_color_by_type()
        self.rich_surface = None
        self.rich_rect = None

    def on_init(self, space, body_iter):        
        inertia = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pymunk.Body(self.mass, inertia)
        self.body.position = self.position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.collision_type = pool_balls_config.COLLISION_TYPE_POOL_BALL + body_iter
        self.shape.elasticity = pool_balls_config.pool_ball_elasticity
        self.shape.friction = pool_balls_config.pool_ball_friction
        space.add(self.body, self.shape)

        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME | DrawMode.PHYSICS:
            padding = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                padding = pool_balls_config.pool_ball_draw_mode_wireframe_thickness*2

            self.raw_surface = pygame.Surface((self.radius*2+padding, self.radius*2+padding), pygame.SRCALPHA)
        elif self.draw_mode in DrawMode.RICH:
            img = self.get_rich_surface()
            if not img:
                print('No pool ball img:', self.type)
                return
            
            self.rich_surface = pygame.transform.scale(img, (self.radius*2, self.radius*2))
            self.rich_rect = self.rich_surface.get_rect(center=self.position)

        self.is_on_table = True
        
        self._draw()

    def _draw(self):
        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                width = self.wireframe_thickness
            pygame.draw.circle(self.raw_surface, self.raw_color, (self.radius, self.radius), self.radius, width)

            # if self.is_highlighted:
            #     pygame.draw.circle(self.raw_surface, self.highlight_color, (self.radius, self.radius), self.radius, 2)            

    def update(self):
        self.angle = self.body.angle
        self.position = self.body.position
        
        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            self.raw_rect = self.raw_surface.get_rect(center=self.body.position)
        elif self.draw_mode in DrawMode.RICH:
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
        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            surface.blit(self.raw_surface, self.raw_rect)
        elif self.draw_mode in DrawMode.RICH:
            surface.blit(self.rich_surface, self.rich_rect)
            

    def highlight_position(self, show=True):
        self.is_highlighted = show
        self._draw()

    def set_force_at_point(self, force):
        #TODO: IF using max force, then apply at SCALE, fixing the ratio!!
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

    def get_rich_surface(self):
        media_path = None
        if pool_balls_config.pool_ball_DM_RICH_use_identifer_as_media:
            media_path = f'ball_{self.identifier}.png'
        else:
            if self.type == POOL_BALL_TYPE_CUE:
                media_path = pool_balls_config.pool_ball_DM_RICH_cue_media_path
            elif self.type == POOL_BALL_TYPE_8:
                media_path = pool_balls_config.pool_ball_DM_RICH_8_media_path
            elif self.type == POOL_BALL_TYPE_SPOT:
                media_path = pool_balls_config.pool_ball_DM_RICH_spot_media_path
            elif self.type == POOL_BALL_TYPE_STRIPE:
                media_path = pool_balls_config.pool_ball_DM_RICH_stripe_media_path
        
        if media_path is None:
            return None
        
        media_path = f'{pool_balls_config.pool_ball_DM_RICH_media_path}/{media_path}'
        rich_surface = self.media_manager.get(media_path, convert_alpha=True)
        return rich_surface

    def get_color_by_type(self):
        if self.type == POOL_BALL_TYPE_CUE:
            return pool_balls_config.pool_ball_DM_RAW_cue_color
        elif self.type == POOL_BALL_TYPE_8:
            return pool_balls_config.pool_ball_DM_RAW_8_color
        elif self.type == POOL_BALL_TYPE_SPOT:
            return pool_balls_config.pool_ball_DM_RAW_spot_color
        elif self.type == POOL_BALL_TYPE_STRIPE:
            return pool_balls_config.pool_ball_DM_RAW_stripe_color
        else:
            return (0, 255, 0)