from pygame import Vector2
from pymunk import Vec2d
from classes.actor.actor import Actor
from classes.common.sprite_sheet import SpriteSheet
from classes.configs.sprite_animation_config import SpriteAnimationConfig
from config import Dict, pymunk, math, pygame

class CowActor(Actor):
    def __init__(self, birth_date):
        sprite_sheet_image_path = 'actors/cow/cow.png'
        color_key = ((255,255,255))

        animation_data = self.construct_animation_data()
        
        current_animation = animation_data.get(f'walk_down')
        current_animation.rotation_offset = 90
        animate = False

        super(CowActor, self).__init__(birth_date, sprite_sheet_image_path, animation_data, current_animation, color_key, animate)

        self.scale = 1.2
        self.well_being.sustenance.hunger_rate = 0.01
        self.destination_position = None
        self.max_speed = 230
        self.velocity = Vec2d(0,0)
        self.acceleration = Vec2d(0,0)
        self.elasticity = 0.2
        self.friction = 0.8
        self.desired_vector = None
        self.approach_radius = self.max_speed * 0.4
        self.mouse_position = None
        self.mass = 300
        self.steering_force = 2.2


        self.redraw()
        self.construct_physical_body()
        
        

    def construct_physical_body(self):
        body_type = pymunk.Body.DYNAMIC
        radius = self.rect.width/4 if self.rect.width > self.rect.height else self.rect.height/4
        moment = pymunk.moment_for_circle(self.mass, 0, radius)

        self.body = pymunk.Body(self.mass, moment, body_type)
        self.body.angle = math.radians(self.angle)
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = self.elasticity
        self.shape.friction = self.friction

    def construct_animation_data(self):
        animation_data: Dict[str, SpriteAnimationConfig] = dict()

        label = 'eat_up'
        position = (0,0)
        size = (28, 72)
        steps = 4
        speed = 350
        anim_eat_up = SpriteAnimationConfig(label, position, size, steps, speed)
        animation_data[label] = anim_eat_up

        label = 'eat_down'
        position = (28*4,0)
        size = (28, 72)
        steps = 4
        speed = 350
        anim_eat_down = SpriteAnimationConfig(label, position, size, steps, speed)
        animation_data[label] = anim_eat_down

        label = 'eat_left'
        position = (0,144)
        size = (72, 44)
        steps = 4
        speed = 350
        anim_eat_left = SpriteAnimationConfig(label, position, size, steps, speed)
        animation_data[label] = anim_eat_left

        label = 'eat_right'
        position = (0,188)
        size = (71, 44)
        steps = 4
        speed = 350
        anim_eat_right = SpriteAnimationConfig(label, position, size, steps, speed)
        animation_data[label] = anim_eat_right

        label = 'walk_up'
        position = (0,72)
        size = (28, 72)
        steps = 4
        speed = 350
        anim_walk_up = SpriteAnimationConfig(label, position, size, steps, speed)
        animation_data[label] = anim_walk_up

        label = 'walk_down'
        position = (28*4,72)
        size = (28, 72)
        steps = 4
        speed = 350
        anim_walk_down = SpriteAnimationConfig(label, position, size, steps, speed)
        animation_data[label] = anim_walk_down

        label = 'walk_left'
        position = (0,234)
        size = (72, 44)
        steps = 4
        speed = 350
        anim_walk_left = SpriteAnimationConfig(label, position, size, steps, speed)
        animation_data[label] = anim_walk_left

        label = 'walk_right'
        position = (0,279)
        size = (72, 44)
        steps = 4
        speed = 350
        anim_walk_right = SpriteAnimationConfig(label, position, size, steps, speed)
        animation_data[label] = anim_walk_right

        return animation_data
    
    def test_steering_behaviour(self, time_lapsed):
        acceleration_towards_target = self.seek_and_steer_towards_target_with_approach(self.mouse_position, self.approach_radius)
        
        self.acceleration = Vec2d(acceleration_towards_target.x, acceleration_towards_target.y)
        self.velocity += self.acceleration
        if self.velocity.length > self.max_speed:
            self.velocity = self.velocity.scale_to_length(self.max_speed)
        
        velocity_dampener = 0.1
        slowest_anim_speed = 5000
        anim_speed = self.current_animation.animation_speed / (self.velocity.length*velocity_dampener)
        self.animate = anim_speed < slowest_anim_speed
        self.set_animation_speed(anim_speed, False)

        self.body._set_velocity(self.velocity)
        self.body.angle = self.velocity.angle
    
    def seek_and_steer_towards_target_with_approach(self, target: Vector2, approach_radius):
        pos_vec = Vector2(self.position[0], self.position[1])
        self.desired_vector = (target - pos_vec)
        distance = self.desired_vector.length()
        self.desired_vector.normalize_ip()

        if distance < approach_radius:
            self.desired_vector *= distance / approach_radius * self.max_speed
        else:
            self.desired_vector *= self.max_speed

        steering = self.desired_vector - Vector2(self.velocity)
        if steering.length() > self.steering_force:
            steering.scale_to_length(self.steering_force)

        return steering

    def update(self, time_lapsed, mouse_position: Vector2, *args, **kwargs):
        self.mouse_position = mouse_position
        if self.is_active:
            self.test_steering_behaviour(time_lapsed)

        redraw = False
        if self.position != self.body.position:
            self.position = self.body.position
            redraw = True

        angle = math.degrees(self.body.angle)
        if self.angle != angle:
            self.angle = angle
            redraw = True

        if redraw:
            self.redraw()
        
        return super().update(time_lapsed, *args, **kwargs)
    
    def draw_vectors(self, surface: pygame.Surface):
        vec_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

        scale = 1
        # pos_vec = Vector2(self.position)
        vel_vec = Vector2(self.velocity.x, self.velocity.y)
        # desired
        color = pygame.Color('red')
        start_pos = Vector2(self.position)
        end_pos = (start_pos + self.desired_vector * scale)
        pygame.draw.line(vec_surface, color, start_pos, end_pos, 3)
        # current velocity
        color = pygame.Color('green')
        end_pos = (start_pos + vel_vec * scale)
        pygame.draw.line(vec_surface, color, start_pos, end_pos, 3)
        # approach radius
        color = pygame.Color('white')
        pygame.draw.circle(vec_surface, color, self.mouse_position, self.approach_radius, 1)

        vec_surface.set_alpha(120)
        surface.blit(vec_surface, (0,0))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

        self.draw_vectors(surface)