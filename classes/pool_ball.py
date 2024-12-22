from config import pool_balls_config, pygame, pymunk, math
from globals import media_manager

from classes.draw_mode_enum import DrawModeEnum
from classes.__helpers__ import aspect_scale
from classes.game_sprite import GameSprite

class PoolBall(GameSprite):
    def __init__(self, identifier, radius, mass, elasticity, friction, position, color, media):
        super(GameSprite, self).__init__()
        
        self.draw_mode = pool_balls_config.pool_ball_draw_mode
        self.mass = mass
        self.shape_elasticity = elasticity
        self.shape_friction = friction
        self.ball_RAW_color = color
        self.ball_RICH_media = media
        self.max_force = pool_balls_config.pool_ball_max_force
        self.radius = radius
        self.position = position
        self.shape_collision_type = pool_balls_config.COLLISION_TYPE_POOL_BALL
        self.WIREFRAME_outline_width = pool_balls_config.pool_ball_DM_WIREFRAME_outline_width

        self.identifier = identifier

        self.angle = 0
        self.body = None
        self.shape = None

        self.is_moving = False
        self.is_in_active_play = False
        self.is_picked_up = False

        self.surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=(self.radius,self.radius))
        self.ball_surface = self.surface.copy()
        self.orig_image = None
        self.z_distance_from_floor = 0.01

    def setup_visuals(self):
        if self.draw_mode in DrawModeEnum.RAW | DrawModeEnum.WIREFRAME:
            outline_width = 0
            if self.draw_mode in DrawModeEnum.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            pygame.draw.circle(self.ball_surface, self.ball_RAW_color, (self.radius, self.radius), self.radius, outline_width)
        elif self.draw_mode in DrawModeEnum.RICH:
            # Ball
            self.orig_image = media_manager.get(self.ball_RICH_media)
            if not self.orig_image:
                print('No pool ball img:', self.ball_RICH_media)
                return
            
            self.image = pygame.transform.scale(self.orig_image, (self.radius*2, self.radius*2))
            # self.image.set_alpha(50)
            # self.image.set_colorkey((0,0,0))
            # self.ball_surface.blit(self.image, (0, 0))

        #TODO: FiX for working with wireframe/RAW
        self.mask = pygame.mask.from_surface(self.image)

    def setup_physical_body(self, body_iter):
        inertia = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body = pymunk.Body(self.mass, inertia)
        self.body.position = self.position
        self.shape = pymunk.Circle(self.body, self.radius)

        # IGNORE THIS FOR NOW......
        # self.shape.collision_type = self.shape_collision_type + body_iter
        self.shape.collision_type = self.shape_collision_type
        # self.shape.filter = pymunk.ShapeFilter()

        self.shape.elasticity = self.shape_elasticity
        self.shape.friction = self.shape_friction

    def stop_moving(self):
        self.body.velocity = (0,0)

    def on_init(self, body_iter):
        self.setup_visuals()
        self.setup_physical_body(body_iter)

    def pick_up_ball(self):
        self.stop_moving()
        self.is_picked_up = True
        self.shape.sensor = True
        scale = 2.1
        self.image = aspect_scale(self.orig_image, (self.radius*scale, self.radius*scale))
        self.ball_surface = self.image
        self.z_distance_from_floor = 1.0

    def update(self, *args, **kwargs):
        if not self.is_picked_up:
            self.angle = self.body.angle
            self.position = self.body.position
        elif self.is_picked_up:
            self.body.position = self.position  #Wont collide if its a sensor
        
        self.rect = self.surface.get_rect(center=self.position)
        
        #TODO: Consider the 'is_moving' again - am I checking already for this?
        # stop_force_margin = 3
        # x_v = self.body.velocity[0]
        # y_v = self.body.velocity[1]
        # if not self.body.is_sleeping and (x_v > -stop_force_margin and x_v < stop_force_margin) and (y_v > -stop_force_margin and y_v < stop_force_margin):
        #     # force stop the ball
        #     self.body._set_velocity((0, 0))
        #     self.is_moving = False
        # else:
        #     self.is_moving = True
        
        return super().update(*args, **kwargs)



    # def highlight_position(self, show=True):
    #     self.is_highlighted = show
    #     self._draw()

    def set_force_at_point(self, force):
        #TODO: IF using max force, then apply at SCALE, fixing the ratio!!
        force_x = force[0]
        force_y = force[1]
        # if force_x > 0 and force_x > self.max_force:
        #     force_x = self.max_force
        # elif force_x < 0 and force_x < -self.max_force:
        #     force_x = -self.max_force
        # if force_y > 0 and force_y > self.max_force:
        #     force_y = self.max_force
        # elif force_y < 0 and force_y < -self.max_force:
        #     force_y = -self.max_force
        # print('force applied', force_x, force_y)
        self.body.apply_force_at_local_point((force_x, force_y))
