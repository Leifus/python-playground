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
        animate = True

        super(CowActor, self).__init__(birth_date, sprite_sheet_image_path, animation_data, current_animation, color_key, animate)

        self.well_being.sustenance.hunger_rate = 0.01
        self.destination_position = None
        self.max_speed = 80
        self.velocity = Vec2d(0,0)
        self.acceleration = Vec2d(0,0)
        self.elasticity = 0.2
        self.friction = 0.8
        self.desired_vector = None
        self.approach_radius = self.max_speed * 1.7
        self.mouse_position = None
        self.mass = 300
        self.steering_force = 0.8


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
        # Follow mouse
        # pos_vec = Vector2(self.position[0], self.position[1])
        # acceleration = (mouse_position-pos_vec).normalize() * 0.5

        acceleration = self.seek_and_steer_towards_target_with_approach(self.mouse_position, self.approach_radius)
        
        self.acceleration = Vec2d(acceleration.x, acceleration.y)
        self.velocity += self.acceleration
        if self.velocity.length > self.max_speed:
            self.velocity = self.velocity.scale_to_length(self.max_speed)
        
        self.body._set_velocity(self.velocity)
        self.body.angle = self.velocity.angle

    # def seek_and_steer_towards_target(self, target: Vector2):
    #     pos_vec = Vector2(self.position[0], self.position[1])
    #     self.desired_vector = (target - pos_vec).normalize() * self.max_speed
    #     steering = self.desired_vector - Vector2(self.velocity)
    #     max_seek_force = 0.9
    #     if steering.length() > max_seek_force:
    #         steering.scale_to_length(max_seek_force)

    #     return steering
    
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

    # def test_steering_behaviour_set_initial_velocity(self):
    #     self.velocity = Vec2d(self.max_speed, 0).rotated_degrees(self.angle)
    #     self.acceleration = Vec2d(0,0)
    #     self.body._set_velocity(self.velocity)

    def update(self, time_lapsed, mouse_position: Vector2, *args, **kwargs):
        self.mouse_position = mouse_position
        if self.is_active:
            self.test_steering_behaviour(time_lapsed)

        # if self.is_active and self.destination_position is not None:
        #     if self.destination_position == self.position:
        #         self.destination_position = None
        #         self.animate = False
        #     else:
        #         # Move towards position
        #         # Force position move for now..
        #         dest_x, dest_y = self.destination_position
        #         x, y = self.position
        #         dx = dest_x - x
        #         dy = dest_y - y
        #         angle_to_destination = math.atan2(dy, dx)
        #         distance = int(math.sqrt((x-dest_x)**2 + (y-dest_y)**2))
        #         angle_diff = abs(angle_to_destination - self.body.angle)
        #         min_angle_diff = 0.2
        #         if angle_diff >= min_angle_diff:
        #             self.body.angle = angle_to_destination
        #             # print('angle_diff', angle_diff, min_angle_diff, angle_to_destination)
        #         next_x = x
        #         next_y = y
        #         move_by = 1
        #         if move_by > distance:
        #             move_by = distance

        #         # print('distance', distance, angle_to_destination)
        #         if dest_x > x:
        #             next_x = x + move_by
        #         elif dest_x < x:
        #             next_x = x - move_by
        #         if dest_y > y:
        #             next_y = y + move_by
        #         elif dest_y < y:
        #             next_y = y - move_by
        #         self.body.position = (next_x, next_y)

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
    
    # def move_to_new_position(self, new_position):
    #     x, y = self.position
    #     new_x, new_y = new_position
    #     dx = new_x - x
    #     dy = new_y - y
    #     angle_to_new_position = math.atan2(dy, dx)
    #     self.body.angle = angle_to_new_position
    #     self.animate = True
    #     self.destination_position = new_position

    #     print('move_to_new_position', self.body.angle, angle_to_new_position, dx, dy)

    def draw_vectors(self, surface: pygame.Surface):
        scale = 1
        pos_vec = Vector2(self.position)
        vel_vec = Vector2(self.velocity.x, self.velocity.y)
        # desired
        color = pygame.Color('red')
        start_pos = pos_vec
        end_pos = (pos_vec + self.desired_vector * scale)
        pygame.draw.line(surface, color, start_pos, end_pos, 3)
        # current velocity
        color = pygame.Color('green')
        start_pos = pos_vec
        end_pos = (pos_vec + vel_vec * scale)
        pygame.draw.line(surface, color, start_pos, end_pos, 3)
        # approach radius
        color = pygame.Color('white')
        pygame.draw.circle(surface, color, self.mouse_position, self.approach_radius, 1)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

        self.draw_vectors(surface)