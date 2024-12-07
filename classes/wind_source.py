from config import pymunk, pygame, math, COLLISION_TYPE_WIND, COLLISION_TYPE_BALLOON

class WindSource:
    def __init__(self, position, cone_angle, angle=0, strength=5000, cone_length=300, height=200, width=200):
        self.position = position
        self.angle = math.radians(angle)
        self.strength = strength
        self.active = True
        self.cone_length = cone_length
        self.cone_angle = cone_angle
        self.cone_points = self.get_cone_points()
        
        max_x = self.cone_points[1][0]
        if self.cone_points[2][0] > max_x:
            max_x = self.cone_points[1][0]
        max_y = self.cone_points[1][1]
        if self.cone_points[2][1] > max_y:
            max_y = self.cone_points[2][1]
        self.surface = pygame.Surface((max_x, max_y), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=(0, 0))

        fan_image = pygame.image.load('media/desk-fan.png').convert_alpha()
        fan_image = pygame.transform.flip(fan_image, flip_x=1, flip_y=0)
        self.fan_image = pygame.transform.scale(fan_image, (width, height))
        self.fan_rect = self.fan_image.get_rect(center=(self.position[0],self.position[1]+14))
        
        self.space = None
        self.body = None
        self.shape = None
        
        self.create_sensor_shape()
        self.draw()
        
    def on_init(self, space):
        self.space = space
        self.space.add(self.body, self.shape)

        self.setup_collision_handlers()

    def draw(self):
        # Draw wind source
        # pygame.draw.circle(
        #     self.surface,
        #     (255,255,0) if self.active else (0,0,0), 
        #     self.position,
        #     10
        # )

        # # Draw wind cone when active
        if self.active:
            # load windy gif
            pygame.draw.polygon(self.surface, pygame.Color('cyan3'), self.cone_points, 2)
        
        # Draw direction indicator
        # end_x = self.position[0] + math.cos(self.angle) * 20
        # end_y = self.position[1] + math.sin(self.angle) * 20
        # pygame.draw.line(
        #     self.surface,
        #     pygame.Color('white'),
        #     self.position,
        #     (end_x, end_y),
        #     3
        # )

    def setup_collision_handlers(self):
        handler = self.space.add_collision_handler(COLLISION_TYPE_WIND, COLLISION_TYPE_BALLOON)
        handler.separate = self.on_separate_from_balloon
        handler.pre_solve = self.on_collide_with_balloon
        
    def on_collide_with_balloon(self, arbiter, space, data):
        if not self.active:
            return True
            
        target_shape = arbiter.shapes[1]  # Get the target shape
        # Point of collision is the target's position
        collision_point = target_shape.body.position
        
        # Calculate and apply wind force
        force = self.calculate_wind_force(collision_point)
        target_shape.body.apply_force_at_world_point(force, collision_point)
        
        return True  # Keep the collision active
        
    def on_separate_from_balloon(self, arbiter, space, data):
        return True

    def create_sensor_shape(self):
        # Create a static body for the sensor
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = self.position
        
        # Create points for a triangle/cone shape
        points = self.get_cone_points()
        
        # Convert points to local coordinates relative to body position
        local_points = [(p[0] - self.position[0], p[1] - self.position[1]) for p in points]
        print('local_points=',local_points, 'poitns=', points)
        
        # Create a poly shape for the sensor
        self.shape = pymunk.Poly(self.body, local_points)
        self.shape.sensor = True  # Make it a sensor so it doesn't collide
        self.shape.collision_type = COLLISION_TYPE_WIND  # if needed
        
    def get_cone_points(self):
        left_angle = self.angle - self.cone_angle/2
        right_angle = self.angle + self.cone_angle/2
        
        left_point = (
            self.position[0] + math.cos(left_angle) * self.cone_length,
            self.position[1] + math.sin(left_angle) * self.cone_length
        )
        right_point = (
            self.position[0] + math.cos(right_angle) * self.cone_length,
            self.position[1] + math.sin(right_angle) * self.cone_length
        )
        
        return [self.position, left_point, right_point]

    def calculate_wind_force(self, collision_point):
        if not self.active:
            return (0, 0)
            
        # Vector from wind source to collision point
        dx = collision_point[0] - self.position[0]
        dy = collision_point[1] - self.position[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Calculate force magnitude with distance falloff
        force_magnitude = self.strength * (1 - (distance/self.cone_length)**2)
        
        # Make sure force direction is always the wind direction
        force_x = force_magnitude * math.cos(self.angle)
        force_y = force_magnitude * math.sin(self.angle)
        
        return (force_x, force_y)

    def on_loop(self, space: pymunk.Space):
        pass

    def on_render(self, display_surface: pygame.Surface):
        display_surface.blit(self.fan_image, self.fan_rect)
        display_surface.blit(self.surface, self.rect)
       