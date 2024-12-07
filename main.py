from config import *
from classes.walled_room import WalledRoom
from classes.box_with_lid import BoxWithLid
from classes.balloon import Balloon
from classes.wind_source import WindSource

# random.seed(0)

class MouseInput:
    def __init__(self):
        self.body = None
        self.joint = None
        self.space = None

    def on_init(self, space):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.space = space

    def on_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.joint is not None:
                self.space.remove(self.joint)
                self.joint = None

            p = pymunk.Vec2d(*event.pos)
            hit = self.space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit is not None and hit.shape.body.body_type == pymunk.Body.DYNAMIC:
                shape = hit.shape
                # Use the closest point on the surface if the click is outside
                # of the shape.
                if hit.distance > 0:
                    nearest = hit.point
                else:
                    nearest = p
                self.joint = pymunk.PivotJoint(
                    self.body,
                    shape.body,
                    (0, 0),
                    shape.body.world_to_local(nearest),
                )
                self.joint.max_force = 200000
                self.joint.error_bias = (1 - 0.15) ** 60
                self.space.add(self.joint)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.joint is not None:
                self.space.remove(self.joint)
                self.joint = None

    def on_loop(self):
        self.body.position = pygame.mouse.get_pos()

class App:
    def __init__(self):
        self.surface = None
        self.space = None
        self.clock = None
        self._running = False
        self.draw_options = None
        
        self.walled_room = None
        self.balloons = []
        self.balloon_box = None
        self.background_surface = None
        self.wind_source = None
        
        self.mouse_input = MouseInput()

    def setup_wind_source(self):
        self.wind_source = WindSource(wind_cfg.position, wind_cfg.cone_angle, wind_cfg.angle, wind_cfg.strength, wind_cfg.cone_length, wind_cfg.height, wind_cfg.width)
        self.wind_source.on_init(self.space)

    def setup_box_with_lid(self):
        # position = ((self.surface.get_width()/2) - (width/2) - (self.bounding_box.radius*2), self.surface.get_height() - height - self.bounding_box.radius)
        position = (150, self.surface.get_height() - box_cfg.box_height - self.walled_room.radius)
        self.balloon_box = BoxWithLid(box_cfg, position, self.space)
    
    def fill_box_with_balloons(self):
        blue_balloon = pygame.image.load('media/BlueBalloon.webp').convert_alpha()
        green_balloon = pygame.image.load('media/GreenBalloon.webp').convert_alpha()
        orange_balloon = pygame.image.load('media/OrangeBalloon.webp').convert_alpha()
        purple_balloon = pygame.image.load('media/PurpleBalloon.webp').convert_alpha()
        red_balloon = pygame.image.load('media/RedBalloon.webp').convert_alpha()

        balloon_images = [
            blue_balloon, green_balloon, orange_balloon, purple_balloon, red_balloon
        ]

        for _ in range(app_cfg.balloon_count):
            balloon_image = random.choice(balloon_images)
            radius = random.uniform(app_cfg.balloon_min_radius, app_cfg.balloon_max_radius)
            
            rand_x = random.uniform(self.balloon_box.rect.left + (radius*2), self.balloon_box.rect.right - (radius*2))
            rand_y = random.uniform(self.balloon_box.rect.bottom - (radius*2), self.balloon_box.rect.top + (radius*2))

            position = (rand_x, rand_y)
            cfg = balloon_cfg
            balloon = Balloon(balloon_image, cfg.alpha, radius, position, cfg.base_gravity, cfg.base_gravity_radius_multiplier, cfg.base_mass, cfg.base_mass_radius_multiplier, cfg.elasticity, cfg.friction, self.space)
            self.balloons.append(balloon)

    def setup_scene(self):
        background = pygame.image.load('media/room.jpg').convert()
        self.background_surface = pygame.transform.scale(background, app_cfg.window_size)

        self.walled_room = WalledRoom(self.space, self.surface.get_size(), app_cfg.wall_thickness)


    def on_init(self):
        pygame.init()

        self.surface = pygame.display.set_mode(app_cfg.window_size, DOUBLEBUF, 32)
        if app_cfg.debug_draw_pymunk_space:
            self.draw_options = pymunk.pygame_util.DrawOptions(self.surface)


        self.space = pymunk.Space()
        self.space.iterations = phys_cfg.space_iterations
        self.space.gravity = phys_cfg.space_gravity
        self.space.damping = phys_cfg.space_damping
        self.space.sleep_time_threshold = phys_cfg.space_sleep_time_threshold
        
        self.clock = pygame.time.Clock()
        # pygame.event.set_allowed([QUIT])

        self.mouse_input.on_init(self.space)

        self.setup_scene()
        self.setup_wind_source()
        self.setup_box_with_lid()
        self.fill_box_with_balloons()

        self._running = True
        
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
            return
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self._running = False
            return

        self.mouse_input.on_event(event)

    def on_loop(self):
        self.mouse_input.on_loop()
        self.wind_source.on_loop(self.space)

        for balloon in self.balloons:
            balloon.on_loop()
        
        self.balloon_box.on_loop()

    def on_render(self):
        bg_fill = pygame.Color('white')
        self.surface.fill(bg_fill)
        self.surface.blit(self.background_surface, (0,0))

        if app_cfg.debug_draw_pymunk_space:
            self.space.debug_draw(self.draw_options)

        self.wind_source.on_render(self.surface)

        for balloon in self.balloons:
            balloon.on_render(self.surface)

        self.balloon_box.on_render(self.surface)

        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)

            for _ in range(app_cfg.dt_steps):
                self.space.step(app_cfg.dt / app_cfg.dt_steps)
            
            self.on_loop()
            self.on_render()
            
            self.clock.tick(app_cfg.fps)
            pygame.display.set_caption("fps: " + str(int(self.clock.get_fps())))

        self.on_cleanup()

 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
    pygame.quit()
