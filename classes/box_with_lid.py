from config import pymunk, pygame, math, BoxWithLidConfig

class BoxWithLid:
    def __init__(self, cfg: BoxWithLidConfig, position, space: pymunk.Space):
        self.position = position
        
        # box
        box_image = pygame.image.load('media/crate.png').convert_alpha()
        self.surface = pygame.transform.scale(box_image, (cfg.box_width, cfg.box_height))
        self.rect = self.surface.get_rect(topleft=self.position)
        self.surface.set_alpha(cfg.box_alpha)

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (self.rect.topleft[0], self.rect.topleft[1] + (cfg.box_height/2))
        side = pymunk.Poly.create_box(body, (cfg.box_edge_thickness, self.rect.height))
        space.add(side.body, side)

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (self.rect.topright[0], self.rect.topright[1] + (cfg.box_height/2))
        side = pymunk.Poly.create_box(body, (cfg.box_edge_thickness, self.rect.height))
        space.add(side.body, side)

        # lid
        inertia_moment = pymunk.moment_for_box(cfg.lid_mass, (cfg.lid_width, cfg.lid_height))
        body = pymunk.Body(cfg.lid_mass, inertia_moment)
        body.position = (self.rect.centerx, self.rect.top - cfg.box_edge_thickness - (cfg.lid_height/2))
        self.lid = pymunk.Poly.create_box(body, (cfg.lid_width, cfg.lid_height))
        space.add(self.lid.body, self.lid)
        
        lid_image = pygame.image.load('media/cardboard_texture.jpg').convert_alpha()
        self._orig_lid_image = pygame.transform.scale(lid_image, (cfg.lid_width, cfg.lid_height))
        self.lid_surface = self._orig_lid_image
        self.lid_rect = self.lid_surface.get_rect(center=body.position)



    def on_loop(self):
        body = self.lid.body
        angle = math.degrees(-body.angle)
        self.lid_surface = pygame.transform.rotate(self._orig_lid_image, angle)
        self.lid_rect = self.lid_surface.get_rect(center=body.position)

    def on_render(self, display_surface: pygame.Surface):
        display_surface.blit(self.lid_surface, self.lid_rect)
        display_surface.blit(self.surface, self.rect)
