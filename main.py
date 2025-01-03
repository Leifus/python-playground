from classes.sandbox import Sandbox
from config import *
import config

class App:
    def __init__(self):
        self.surface = None
        self.rect = None
        self.app_is_running = False
        self.mouse_position = None

        self.game_surface: pygame.Surface = None
        
        self.sandbox: Sandbox = None

    def on_init(self):
        pygame.init()

        self.surface = pygame.display.set_mode(config.display_size, config.display_flags, config.display_depth)
        self.rect = self.surface.get_rect()
        self.game_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.game_surface_rect = self.game_surface.get_rect()

        self.setup_sandbox()

        self.app_is_running = True

    def setup_sandbox(self):
        size = (self.rect.width * 0.8, self.rect.height * 0.8)
        position = self.rect.center
        self.sandbox = Sandbox(size, position)
        self.sandbox.add_food_sources()
        self.sandbox.add_water_source()
        self.sandbox.add_cow_actor()

    def on_event(self, event: pygame.event.Event):
        if event.type == QUIT:
            self.app_is_running = False
            return
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.app_is_running = False
            return
        
        if event.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]:
            self.mouse_position = event.pos

        self.sandbox.on_event(event)
        
    def update(self):
        self.sandbox.update()

    def draw(self):
        bg_fill = config.display_bg_color
        self.surface.fill(bg_fill)

        self.sandbox.draw(self.surface)

        pygame.display.update()
 
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.app_is_running = False
 
        pygame.display.set_caption("Herd Sim")

        while( self.app_is_running ):
            for event in pygame.event.get():
                self.on_event(event)

            self.update()
            self.draw()

        self.on_cleanup()

 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
    pygame.quit()
