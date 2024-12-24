from config import pool_balls_config, pygame, pymunk, random
from globals import media_manager, sound_manager

from classes.draw_mode_enum import DrawModeEnum
from classes.game_sprite import GameSprite

class PoolBall(GameSprite):
    def __init__(self, identifier, radius, mass, elasticity, friction, position, color, media):
        super(PoolBall, self).__init__()

        #TODO: REPLACE THIS FOR BETTER UID type
        #TODO: Move to super
        self._identifier: float = random.random()

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
        self.alpha = 255

        # self.image: pygame.Surface | None = None
        # self.orig_image: pygame.Surface | None = None
        # self.mask: pygame.mask.Mask | None = None
        # self.rect: pygame.Rect | None = None

        self.base_scale_factor = 1.0
        self.scale_factor = self.base_scale_factor
        
        self.identifier = identifier

        self.angle = 0
        self.body = None
        self.shape = None

        self.is_moving = False
        self.is_in_active_play = False
        self.is_picked_up = False

        self.base_z_distance_from_floor = 0.01
        self.z_distance_from_floor = self.base_z_distance_from_floor

        self.sounds_cue_hit = 'cue_hit_ball_1.wav'

        self.setup_visuals()
        self.setup_physical_space()
        self.redraw()

    def redraw(self):
        orig_rect = self.orig_image.get_rect()
        image_radius = self.radius*2 * self.scale_factor
        if self.image is None or orig_rect.width != image_radius:
            self.image = pygame.transform.scale(self.orig_image, (image_radius, image_radius))
            self.image.set_alpha(self.alpha)
            self.rect = self.image.get_rect(center=self.position)
            self.mask = pygame.mask.from_surface(self.image)

        if self.mask is None:
            self.mask = pygame.mask.from_surface(self.image)

        # self.image.set_alpha(100)

    def setup_visuals(self):
        if self.draw_mode in DrawModeEnum.Raw | DrawModeEnum.Wireframe:
            # Ball
            outline_width = 0
            if self.draw_mode in DrawModeEnum.Wireframe:
                outline_width = self.WIREFRAME_outline_width

            self.orig_image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(self.orig_image, self.ball_RAW_color, (self.radius, self.radius), self.radius, outline_width)
        elif self.draw_mode in DrawModeEnum.Rich:
            # Ball
            self.orig_image = media_manager.get(self.ball_RICH_media)
            if not self.orig_image:
                print('No pool ball img:', self.ball_RICH_media)
                return

    def setup_physical_space(self):
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

    def reconstruct_physical_body(self):
        space = self.body.space
        if space is not None:
            space.remove(self.body, self.shape)
            space.step(1)
            self.setup_physical_space()
            space.add(self.body, self.shape)
            space.step(1)
        else:
            self.setup_physical_space()

    def set_mass(self, mass):
        self.mass = mass

        # TODO: Maybe reuse construct_physical_body
        # What about the inertia moment? Does this need changing?
        self.body.mass = mass
        inertia = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.body.moment = inertia

    def set_radius(self, radius):
        self.radius = radius
        
        self.reconstruct_physical_body()
        self.redraw()

        # TODO: Maybe reuse construct_physical_body
        # TODO: FINSIH tHIS!!!
        # self.body.space.
        # pymunk.

        # TODO: FINSIH tHIS!!!
        # self.redraw()

    def stop_moving(self):
        self.body.velocity = (0,0)

    def drop_ball(self):
        self.stop_moving()
        self.is_picked_up = False
        self.shape.sensor = False
        self.scale_factor = self.base_scale_factor
        self.z_distance_from_floor = self.base_z_distance_from_floor
        self.alpha = 255
        self.redraw()

    def pick_up_ball(self):
        self.stop_moving()
        self.is_picked_up = True
        self.shape.sensor = True
        self.scale_factor = 1.2
        self.z_distance_from_floor = 0.1
        self.alpha = 120
        self.redraw()

    def update(self, *args, **kwargs):
        if not self.is_picked_up:
            self.angle = self.body.angle
            self.position = self.body.position
        elif self.is_picked_up:
            self.body.position = self.position  #Wont collide if its a sensor
        
        self.rect = self.image.get_rect(center=self.position)
        
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

    #TODO: Replace how volume is being resolved
    def on_cue_hit(self, force, volume):
        self.set_force_at_point(force)

        # Make a sound
        sound_manager.play_sound(self.sounds_cue_hit, volume)