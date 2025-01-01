from pygame import Vector2
from classes.common.helper_methods import aspect_scale
from classes.common.sprite_sheet import SpriteSheet
from classes.enums.collision_type_enum import CollisionTypeEnum
from config import pool_balls_config, pygame, pymunk, random, math
from globals import media_manager, sound_manager

from classes.enums.draw_mode_enum import DrawModeEnum
from classes.common.game_sprite import GameSprite

class PoolBall(GameSprite):
    def __init__(self, identifier, radius, mass, elasticity, friction, position, color, media, make_a_ball=False, sprite_sheet_to_use: SpriteSheet = None):
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
        self.shape_collision_type = CollisionTypeEnum.COLLISION_TYPE_POOL_BALL.value
        self.WIREFRAME_outline_width = pool_balls_config.pool_ball_DM_WIREFRAME_outline_width
        self.alpha = 255
        self.make_a_ball = make_a_ball
        self.sprite_sheet_to_use = sprite_sheet_to_use
        
        self.base_scale_factor = 1.0
        self.scale_factor = self.base_scale_factor
        
        self.identifier = identifier

        self.angle = 0
        self.body = None
        self.shape = None

        self.is_moving = False
        self.is_in_active_play = False
        self.is_picked_up = False

        self.base_z_distance_from_floor = 0.001
        self.z_distance_from_floor = self.base_z_distance_from_floor

        self.sounds_cue_hit = 'cue_hit_billiard_ball.wav'

        self.shape_before_updated: pymunk.Shape = None

        self.setup_visuals()
        self.setup_physical_space()
        self.redraw()

    def redraw(self):
        if self.sprite_sheet_to_use is not None:
            self.orig_image = self.sprite_sheet_to_use.image

        orig_rect = self.orig_image.get_rect()
        image_radius = self.radius*2 * self.scale_factor

        image = pygame.transform.smoothscale(self.orig_image, (image_radius, image_radius))
        
        angle = -math.degrees(self.angle)
        rotated = pygame.transform.rotate(image, angle)

        self.image = rotated
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

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
            self.orig_image = media_manager.get(self.ball_RICH_media, convert=True)
            if not self.orig_image:
                print('No pool ball img:', self.ball_RICH_media)
                return

            if self.make_a_ball:
                # Make a circle mask
                orig_image_rect = self.orig_image.get_rect()

                surface = pygame.Surface(orig_image_rect.size, pygame.SRCALPHA)
                pygame.draw.circle(surface, self.ball_RAW_color, orig_image_rect.center, orig_image_rect.width/2)
                mask = pygame.mask.from_surface(surface)

                # clip the image based on mask/or surface - however its done.
                self.orig_image = mask.to_surface(setsurface=self.orig_image, unsetcolor=None)
                
                


    def setup_physical_space(self, existing_body: pymunk.Body = None):
        inertia = pymunk.moment_for_circle(self.mass, 0, self.radius)

        if not existing_body:
            self.body = pymunk.Body(self.mass, inertia)
            self.body.position = self.position
        else:
            self.body = existing_body

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
            body_before_updated = self.body
            self.shape_before_updated = self.shape
            space.remove(self.body, self.shape)
            self.setup_physical_space(body_before_updated)
            space.add(self.body, self.shape)
        else:
            self.setup_physical_space()

    def set_mass(self, mass):
        print('new mass', self.mass, mass)
        self.mass = mass
        self.body.mass = mass
        
        self.reconstruct_physical_body()
        self.redraw()

    def set_radius(self, radius):
        self.radius = radius
        
        self.reconstruct_physical_body()
        self.redraw()

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

    def update(self, time_lapsed, *args, **kwargs):
        if not self.is_picked_up:
            self.angle = self.body.angle
            self.position = self.body.position
        elif self.is_picked_up:
            self.body.position = self.position  #Wont collide if its a sensor
        
        if self.sprite_sheet_to_use is not None:
            # This allows for idle animation triggers but we'll want to set the speed I think and then within check for 0 or max
            min_ke = 0.1
            ke = self.body.kinetic_energy
            
            self.sprite_sheet_to_use.animate = ke > min_ke
            # print('vel', self.body.velocity)
            if ke > min_ke:
                arbitrary_base_ke = 100000
                ke_ratio = ke / arbitrary_base_ke
                base_anim_speed = 1000
                anim_speed = base_anim_speed / ke_ratio
                lowest_speed = 2000

            # if anim_speed < lowest_speed:
                # reverse_anim = self.body.velocity[0] < 0 or self.body.velocity[1] < 0
                reverse_anim = False
                print('speed', anim_speed, reverse_anim, self.body.velocity, base_anim_speed, ke_ratio, self.body.kinetic_energy)
                self.sprite_sheet_to_use.set_animation_speed(anim_speed, reverse_anim)
            
            self.sprite_sheet_to_use.update(time_lapsed)   #u sure?

        self.redraw()
        
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