from classes.OLDimage_source import ImageSource
from classes.common.helper_methods import aspect_scale
from classes.image_panel import ImagePanel
from classes.image_panel_toolbar import ImagePanelToolbar
from classes.main_draw_space import MainDrawSpace
from classes.ui.left_menu_ui import LeftMenuUI
from config import *
import config
from globals import media_manager

class App:
    def __init__(self):
        self.surface = None
        self.rect = None
        self.app_is_running = False
        self.mouse_position = None

        self.game_surface: pygame.Surface = None

        # self.image_source: ImageSource = None
        # self.sprites_group = pygame.sprite.Group()
        self.left_menu: LeftMenuUI = None
        self.main_draw_space: MainDrawSpace = None
        self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW

    def on_init(self):
        pygame.init()

        self.surface = pygame.display.set_mode(config.display_size, config.display_flags, config.display_depth)
        self.rect = self.surface.get_rect()
        self.game_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.game_surface_rect = self.game_surface.get_rect()

        self.orig_image: pygame.Surface = None
        self.toolbar: ImagePanelToolbar = None

        self.active_image_panel: ImagePanel = None

        self.setup_main_interface()
        self.setup_image_panel_toolbar()

        image_path = 'sandground_3.png'
        orig_image = media_manager.get(image_path, convert_alpha=True)
        image_panel = self.create_image_panel(orig_image)
        self.active_image_panel = image_panel
        self.toolbar.link_to_image_panel(self.active_image_panel)

        self.app_is_running = True

    def create_image_panel(self, image_surface: pygame.Surface):
        position = (self.rect.width/2, self.rect.height/2)
        image_panel = ImagePanel(position, image_surface, self.main_draw_space.max_sprite_loading_size)
        self.main_draw_space.add_image_panel(image_panel)

        return image_panel
    
    def setup_image_panel_toolbar(self):
        self.toolbar = ImagePanelToolbar()

    def setup_left_menu(self):
        size = (150,self.rect.height)
        position = (size[0]/2,size[1]/2)
        self.left_menu = LeftMenuUI(size, position)
        # self.sprites_group.add(self.left_menu)

    def setup_main_draw_space(self):
        size = (self.rect.width-self.left_menu.rect.width,self.rect.height)
        position = (self.rect.width/2+self.left_menu.rect.width/2, self.rect.height/2)
        self.main_draw_space = MainDrawSpace(size, position)

    def setup_main_interface(self):
        self.setup_left_menu()
        self.setup_main_draw_space()

    def on_event(self, event: pygame.event.Event):
        if event.type == QUIT:
            self.app_is_running = False
            return
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.app_is_running = False
            return
        
        if event.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]:
            self.mouse_position = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.active_image_panel or not self.active_image_panel.is_hovered:
                if not self.toolbar.is_hovered and not self.toolbar.move_by_mouse:
                    self.toolbar.unlink_image_panel()
                    self.active_image_panel = None

                    for panel in self.main_draw_space.image_panels:
                        panel: ImagePanel
                        if panel.is_hovered:
                            self.active_image_panel = panel
                            self.toolbar.link_to_image_panel(self.active_image_panel)
                            break
                    
        self.left_menu.on_event(event)
        self.toolbar.on_event(self.mouse_position, event)
        self.main_draw_space.on_event(event)
        
        if self.toolbar.has_killed_panel:
            self.active_image_panel = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: # zoom in
                if self.active_image_panel:
                    self.active_image_panel.zoom_at_scale(1.1)
                    self.toolbar.stick_to_top_of_image_panel()
            elif event.key == pygame.K_z: # zoom out
                if self.active_image_panel:
                    self.active_image_panel.zoom_at_scale(0.9)
                    self.toolbar.stick_to_top_of_image_panel()

    def create_image_panel_from_poly_points(self):
        if not self.active_image_panel:
            return
        
        base_polygon = pygame.Surface(self.active_image_panel.sprite_rect.size, pygame.SRCALPHA)
        poly_points = self.active_image_panel.live_poly_points
        pygame.draw.polygon(base_polygon, pygame.Color('red'), poly_points, 0)

        position = self.active_image_panel.position
        panel = ImagePanel(position, base_polygon, self.main_draw_space.max_sprite_loading_size)
        panel.poly_points = poly_points.copy()
        self.main_draw_space.add_image_panel(panel)

    def update(self):
        self.left_menu.update()
        self.toolbar.update()

        if self.toolbar.copy_poly_points:
            self.create_image_panel_from_poly_points()
            self.toolbar.copy_poly_points = False

        self.main_draw_space.update()

        if not self.left_menu.is_hovered and not self.toolbar.is_hovered:
            self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW
            pygame.mouse.set_cursor(self.mouse_cursor)
        else:
            if self.left_menu.is_hovered and self.mouse_cursor is not self.left_menu.mouse_cursor:
                self.mouse_cursor = self.left_menu.mouse_cursor
                pygame.mouse.set_cursor(self.mouse_cursor)
            elif self.toolbar.is_hovered and self.mouse_cursor is not self.toolbar.mouse_cursor:
                self.mouse_cursor = self.toolbar.mouse_cursor
                pygame.mouse.set_cursor(self.mouse_cursor)

    def draw(self):
        bg_fill = config.display_bg_color
        self.surface.fill(bg_fill)

        self.left_menu.draw(self.surface)
        self.main_draw_space.draw(self.surface)
        self.toolbar.draw(self.surface)
        
        pygame.display.update()
 
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.app_is_running = False
 
        pygame.display.set_caption("Polygon Tracer")

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
