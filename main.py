from config import *
import config
from classes.pool_table import PoolTable
from classes.pool_cue import PoolCue
from classes.path_tracer import PathTracer

class App:
    def __init__(self):
        # Base config
        self.surface = None
        # self.space = None
        self.clock = None
        self.is_running = False

        # App config
        self.pool_table = None
        self.pool_cue = None

        self.mouse_position = None
        self.path_tracer = None


    def on_init(self):
        pygame.init()

        self.surface = pygame.display.set_mode(config.display_size, config.display_flags, config.display_depth)
        self.clock = pygame.time.Clock()

        self.setup_pool_table()
        self.setup_pool_cue()
        self.setup_path_tracer()

        self.is_running = True
        
    def setup_path_tracer(self):
        self.path_tracer = PathTracer(self.surface)

    def setup_pool_cue(self):
        self.pool_cue = PoolCue()
        self.pool_cue.on_init()

    def setup_pool_table(self):
        size = config.pool_table_size
        color = config.pool_table_color
        surface_size = self.surface.get_size()
        position = (surface_size[0]/2, surface_size[1]/2)
        self.pool_table = PoolTable(size, color, position)
        self.pool_table.on_init()

    def on_event(self, event: pygame.event.Event):
        if event.type == QUIT:
            self.is_running = False
            return
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.is_running = False
            return
        
        if event.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]:
            self.mouse_position = event.pos
        
        self.pool_table.on_event(event)
        self.pool_cue.on_event(event)

    def update(self):
        self.pool_table.update()
        self.pool_cue.update()
        self.path_tracer.update(self.pool_table.cue_ball.position, self.mouse_position)

        if self.pool_cue.is_picked_up:
            cue_ball = self.pool_table.cue_ball
            
            #get angle from mouse to ball
            cue_x = cue_ball.position[0]
            cue_y = cue_ball.position[1]
            dx = self.mouse_position[0] - (self.pool_table.rect.x + cue_x)
            dy = self.mouse_position[1] - (self.pool_table.rect.y + cue_y)
            mouse_to_ball_angle = math.atan2(dy, dx)

            cue_angle = 0
            cue_x_offset = 0
            if dx < 0:
                cue_angle -= 90
            elif dx > 0:
                cue_angle += 90
                cue_x_offset += cue_ball.radius*2 + self.pool_cue.length
            
            self.pool_cue.angle = cue_angle + (mouse_to_ball_angle*0.3)
            
            # self.pool_cue.position = (self.pool_table.rect.x + cue_ball.rect.left + cue_x_offset - (self.pool_cue.length/2), self.pool_table.rect.y + cue_ball.rect.centery)

            # print('dx',dx,'dy',dy)
            # print('angle',mouse_to_ball_angle)

            
            # if distance < force_radius:
            #     # Calculate force intensity based on distance
            #     force_intensity = (force_radius - distance) / force_radius * 2000
            #     angle = math.atan2(dy, dx)
                
            #     # Apply rotational impulse
            #     triangle.body.apply_impulse_at_local_point(
            #         (-math.sin(angle) * force_intensity, math.cos(angle) * force_intensity),
            #         (0, 0)
            #     )

            #self.mouse_position
            # print('cue_ball.position',cue_ball.position)
            # print('dx',dx,'dy', dy, 'angle', angle)

    def draw(self):
        bg_fill = config.display_bg_color
        self.surface.fill(bg_fill)

        self.pool_table.draw(self.surface)
        self.pool_cue.draw(self.surface)
        self.path_tracer.draw(self.surface)

        pygame.display.update()
 
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.is_running = False
 
        while( self.is_running ):
            for event in pygame.event.get():
                self.on_event(event)

            self.update()
            self.draw()
            
            self.clock.tick(config.time_fps)
            pygame.display.set_caption("Pool Table - fps: " + str(int(self.clock.get_fps())))

        self.on_cleanup()

 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
    pygame.quit()
