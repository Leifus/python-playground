from config import pymunk, pygame, math, COLLISION_TYPE_BALLOON
from classes.balloon_string import BalloonString

class Balloon:
    def __init__(self, image, alpha, radius, position, base_gravity, base_gravity_radius_multiplier, base_mass, base_mass_radius_multiplier, elasticity, friction, space: pymunk.Space):
        self.radius = radius
        self.position = (position[0] + self.radius, position[1] + self.radius)

        self._orig_surface = pygame.transform.scale(image, (self.radius*2, self.radius*2))
        self.surface = self._orig_surface
        
        #self.surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.surface.set_alpha(alpha)
        self.rect = self.surface.get_rect(center=self.position)
        
        gravity = base_gravity - (radius * base_gravity_radius_multiplier)
        self.gravity = (0, gravity)
        # color = pygame.Color('blue')
        # width = 1
        # pygame.draw.circle(self.surface, color, (self.radius, self.radius), self.radius, width)
        
        mass = base_mass + (radius * base_mass_radius_multiplier)
        inertia_moment = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, inertia_moment)
        body.position = self.position
        body.velocity_func = self.set_gravity
        body._set_center_of_gravity((0,-radius/2))
        self.shape = pymunk.Circle(body, self.radius)
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.shape.collision_type = COLLISION_TYPE_BALLOON
        space.add(self.shape.body, self.shape)
        self.space = space

        self.string = None

        if 1 == 999:
            self.add_string()

    def add_string(self):
        position = (self.rect.centerx, self.rect.bottom)
        length = 30
        thickness = 1
        self.string = BalloonString(position, length, thickness, self, self.space)

    def set_gravity(self, body, gravity, damping, dt):
        pymunk.Body.update_velocity(body, self.gravity, damping, dt)

    def on_loop(self):
        # self.rect = self.surface.get_rect(center=self.shape.body.position)
        angle = -math.degrees(self.shape.body.angle)
        self.surface = pygame.transform.rotate(self._orig_surface, angle)
        self.rect = self.surface.get_rect(center=self.shape.body.position)
        if self.string:
            self.string.on_loop()

    def on_render(self, display_surface: pygame.Surface):
        display_surface.blit(self.surface, self.rect)
        if self.string:
            self.string.on_render(display_surface)
