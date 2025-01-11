from classes.enums.game_mode_enum import GameModeEnum
from classes.game.game_session import GameSession
from config import pygame
import config

class App:
    def __init__(self):
        self.surface = None
        self.rect = None
        self.app_is_running = False
        self.mouse_position = None

        self.game_session: GameSession = None
        self.game_surface: pygame.Surface = None

    def on_init(self):
        pygame.init()

        self.surface = pygame.display.set_mode(config.display_size, config.display_flags, config.display_depth)
        self.rect = self.surface.get_rect()
        self.game_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.game_surface_rect = self.game_surface.get_rect()

        self.create_new_game_session(GameModeEnum.Default)

        self.app_is_running = True

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.app_is_running = False
            return
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app_is_running = False
            return
        
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            self.mouse_position = event.pos
        
        if self.game_session is not None and self.game_session.is_running:
            self.game_session.on_event(event)

    def create_new_game_session(self, game_mode: GameModeEnum):
        game_id = f'{game_mode.name} Game'
        self.game_session = GameSession(self.rect.size, game_id, game_mode)
        self.game_session.is_running = True
        
    def update(self):
        if self.game_session is not None and self.game_session.is_running:
            self.game_session.update()

    def draw(self):
        bg_fill = config.display_bg_color
        self.surface.fill(bg_fill)

        if self.game_session is not None and self.game_session.is_running:
            self.game_session.draw(self.surface)

        pygame.display.update()
 
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.app_is_running = False
 
        pygame.display.set_caption("Gravity Merge")

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
