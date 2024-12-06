from config import pymunk, pygame, COLLISION_TYPE_BALLOON_STRING

class BalloonString:
    def __init__(self, position, length, thickness, parent_balloon, space: pymunk.Space):
        self.length = length
        self.thickness = thickness
        self.surface = pygame.Surface((self.thickness, self.length), pygame.SRCALPHA)
        self.surface.fill(pygame.Color('red')) #debugging
        self.rect = self.surface.get_rect(center=position)

        mass = 0.001
        a = position
        b = (position[0], position[1] + self.length)
        inertia_moment = pymunk.moment_for_segment(mass, a, b, self.thickness)
        string_body = pymunk.Body(mass, inertia_moment)
        string_body.position = position
        #self.shape = pymunk.Segment(body, a, b, self.thickness)
        self.shape = pymunk.Poly.create_box(string_body, (thickness, length))
        self.shape.collision_type = COLLISION_TYPE_BALLOON_STRING
        self.shape.color = pygame.Color('blue')

        pinjoint = pymunk.constraints.PinJoint(parent_balloon.shape.body, string_body, (0, parent_balloon.radius), (0, 7-(length/2)))
        
        space.add(self.shape.body, self.shape, pinjoint)


    def on_loop(self):
        self.rect = self.surface.get_rect(center=self.shape.body.position)

    def on_loop_no_physics(self, balloon_rect):
        self.rect = self.surface.get_rect(center=(balloon_rect.centerx, balloon_rect.bottom))

    def on_render(self, display_surface: pygame.Surface):
        display_surface.blit(self.surface, self.rect)
