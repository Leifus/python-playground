from config import pool_balls_config, pygame, pymunk

from classes.draw_mode import DrawMode
from classes.media_manager import MediaManager
from classes.__helpers__ import aspect_scale

class PoolBall(pygame.sprite.Sprite):
    def __init__(self, identifier, radius, mass, elasticity, friction, position, color, media, media_manager: MediaManager):
        pygame.sprite.Sprite.__init__(self)
        
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

        self.media_manager = media_manager
        self.identifier = identifier

        self.angle = 0
        self.body = None
        self.shape = None

        self.is_moving = False
        self.is_in_active_play = False

        self.image = None
        self.mask = None
        self.surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=(self.radius,self.radius))
        self.ball_surface = self.surface.copy()
        self.orig_image = None

    def setup_visuals(self):
        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            outline_width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            pygame.draw.circle(self.ball_surface, self.ball_RAW_color, (self.radius, self.radius), self.radius, outline_width)
        elif self.draw_mode in DrawMode.RICH:
            image = self.media_manager.get(self.ball_RICH_media)
            if not image:
                print('No pool ball img:', self.ball_RICH_media)
                return
            
            self.orig_image = aspect_scale(image, (self.radius*2, self.radius*2))
            self.image = self.orig_image
            self.ball_surface.blit(self.orig_image, (0, 0))

        self.mask = pygame.mask.from_surface(self.ball_surface)

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


    def on_init(self, body_iter):
        self.setup_visuals()
        self.setup_physical_body(body_iter)

    def update(self):
        self.angle = self.body.angle
        self.position = self.body.position
        self.rect = self.surface.get_rect(center=self.position)
        
        # # if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
        # #     self.rect = self.surface.get_rect(center=self.body.position)
        # # elif self.draw_mode in DrawMode.RICH:
        # #     self.rich_rect = self.rich_surface.get_rect(center=self.body.position)

        # stop_force_margin = 3
        # x_v = self.body.velocity[0]
        # y_v = self.body.velocity[1]
        # if not self.body.is_sleeping and (x_v > -stop_force_margin and x_v < stop_force_margin) and (y_v > -stop_force_margin and y_v < stop_force_margin):
        #     # force stop the ball
        #     self.body._set_velocity((0, 0))
        #     self.is_moving = False
        # else:
        #     self.is_moving = True

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))
        
        self.surface.blit(self.ball_surface, (0,0))

        surface.blit(self.surface, self.rect)


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
