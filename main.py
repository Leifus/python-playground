from pygame import Vector2
from classes.common import media_manager
from classes.image_panel import ImagePanel
from classes.image_panel_toolbar import ImagePanelToolbar
from classes.main_draw_space import MainDrawSpace
from classes.media_explorer import MediaExplorer
from classes.menu import Menu
from classes.toolbar import Toolbar
from config import *
import config
from globals import media_manager

class App:
    def __init__(self):
        self.surface = None
        self.rect = None
        self.app_is_running = False
        self.mouse_position: Vector2 = None

        self.game_surface: pygame.Surface = None

        self.sprites_group = pygame.sprite.Group()

        self.media_explorer: MediaExplorer = None
        self.main_draw_space: MainDrawSpace = None
        self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW
        self.tooltip_image: pygame.Surface = None
        self.tooltip_rect: pygame.Rect = None
        self.menu: Menu = None

    def on_init(self):
        pygame.init()

        self.surface = pygame.display.set_mode(config.display_size, config.display_flags, config.display_depth)
        self.rect = self.surface.get_rect()
        self.game_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.game_surface_rect = self.game_surface.get_rect()

        self.orig_image: pygame.Surface = None
        self.floating_toolbar: ImagePanelToolbar = None

        self.active_image_panel: ImagePanel = None

        self.setup_menu()
        self.setup_media_explorer()
        self.setup_main_toolbar()
        self.setup_main_draw_space()
        self.setup_image_panel_toolbar()

        self.app_is_running = True

    def setup_main_toolbar(self):
        size = (200, self.rect.height-self.menu.rect.height)
        position = (size[0]/2, self.menu.rect.height/2 + self.rect.height/2)
        self.toolbar = Toolbar(position, size)
        if self.menu.active_button and self.menu.active_button.value == 'Tools':
            self.toolbar.is_active = True

    def setup_image_panel_toolbar(self):
        self.floating_toolbar = ImagePanelToolbar()

    def setup_media_explorer(self):
        size = (250, self.rect.height-self.menu.rect.height)
        position = (size[0]/2, self.menu.rect.height/2 + self.rect.height/2)
        self.media_explorer = MediaExplorer(size, position)
        if self.menu.active_button and self.menu.active_button.value == 'Media':
            self.media_explorer.is_active = True

    def setup_main_draw_space(self):
        size = (self.rect.width,self.rect.height)
        position = (self.rect.width/2, self.rect.height/2)
        self.main_draw_space = MainDrawSpace(size, position)

    def setup_menu(self):
        size = (250, 40)
        position = (size[0]/2, size[1]/2)
        self.menu = Menu(size, position)

    def set_active_panel(self, active_panel):
        if self.active_image_panel:
            self.active_image_panel.is_active = False
            self.active_image_panel.redraw_housing_box()

        self.active_image_panel = active_panel
        self.active_image_panel.is_active = True
        self.active_image_panel.redraw_housing_box()

        self.toolbar.set_active_image_panel(self.active_image_panel)

    def on_event(self, event: pygame.event.Event):
        if event.type == QUIT:
            self.app_is_running = False
            return
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.app_is_running = False
            return
        
        if event.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]:
            self.mouse_position = Vector2(event.pos[0], event.pos[1])

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if not self.toolbar.is_hovered and not self.menu.is_hovered and not self.media_explorer.is_hovered:
                #Nothing demands focus.

                hovered_panel = None
                for panel in self.main_draw_space.image_panels:
                    panel: ImagePanel
                    if panel.is_hovered:
                        hovered_panel = panel
                
                if hovered_panel is not None and hovered_panel is not self.active_image_panel:
                    self.set_active_panel(hovered_panel)
                    
            # if not self.active_image_panel: # or not self.active_image_panel.is_hovered:
            #     if not self.floating_toolbar.is_hovered and not self.floating_toolbar.move_by_mouse:
            #         self.floating_toolbar.unlink_image_panel()
            #         self.active_image_panel = None

            #         active_panel = None
            #         for panel in self.main_draw_space.image_panels:
            #             panel: ImagePanel
            #             if panel.is_hovered:
            #                 active_panel = panel
            #                 self.floating_toolbar.link_to_image_panel(self.active_image_panel)
            #                 break

            #         if not active_panel:

                    
        self.menu.on_event(self.mouse_position, event)
        self.toolbar.on_event(self.mouse_position, event)
        self.media_explorer.on_event(event)
        self.floating_toolbar.on_event(self.mouse_position, event)
        self.main_draw_space.on_event(event)
        
        if self.floating_toolbar.has_killed_panel:
            self.active_image_panel = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: # zoom in
                if self.active_image_panel:
                    self.active_image_panel.zoom_at_scale(1.1)
                    self.floating_toolbar.stick_to_top_of_image_panel()
            elif event.key == pygame.K_z: # zoom out
                if self.active_image_panel:
                    self.active_image_panel.zoom_at_scale(0.9)
                    self.floating_toolbar.stick_to_top_of_image_panel()

    def create_image_panel_from_poly_points(self):
        if not self.active_image_panel:
            return
        
        base_polygon = pygame.Surface(self.active_image_panel.sprite_rect.size, pygame.SRCALPHA)
        poly_points = self.active_image_panel.live_poly_points
        pygame.draw.polygon(base_polygon, pygame.Color('red'), poly_points, 0)

        position = self.active_image_panel.position
        self.active_image_panel.panel_copy_count += 1
        identifier = f'{self.active_image_panel.identifier} [{self.active_image_panel.panel_copy_count}]'
        panel = ImagePanel(identifier, position, base_polygon, self.main_draw_space.max_sprite_loading_size)
        panel.poly_points = poly_points.copy()
        self.main_draw_space.add_image_panel(panel)

    def add_selected_media(self):
        media = self.media_explorer.selected_media_item
        identifier = media.file_name
        file_path = os.path.join(media.folder_name, media.file_name)
        orig_image = media_manager.get(file_path, convert_alpha=True)
        position = (self.main_draw_space.rect.width/2, self.main_draw_space.rect.height/2)
        image_panel = ImagePanel(identifier, position, orig_image, self.main_draw_space.max_sprite_loading_size)
        self.main_draw_space.add_image_panel(image_panel)
        self.set_active_panel(image_panel)
        self.media_explorer.add_selected_media = False

        return image_panel

    def set_tooltip(self, tooltip):
        tooltip_font = pygame.font.Font('freesansbold.ttf', 12)
        tooltip_color = pygame.Color('black')
        tooltip_surface = tooltip_font.render(tooltip, True, tooltip_color)
        tooltip_rect = tooltip_surface.get_rect()

        housing_color = pygame.Color('lightcyan')
        housing_surface = pygame.Surface((tooltip_rect.width*1.2, tooltip_rect.height*1.2))
        housing_rect = housing_surface.get_rect()
        housing_surface.fill(housing_color)
        housing_surface.blit(tooltip_surface, (housing_rect.width/2-tooltip_rect.width/2, housing_rect.height/2-tooltip_rect.height/2))
        
        offset_from_mouse = 20
        position = (housing_rect.width/2 + self.mouse_position[0] + offset_from_mouse, self.mouse_position[1] + offset_from_mouse/2)
        self.tooltip_image = housing_surface
        self.tooltip_rect = housing_surface.get_rect(center=position)

    def update(self):
        self.menu.update()
        
        self.media_explorer.is_active = self.menu.active_button and self.menu.active_button.value == 'Media'
        self.media_explorer.update()
        if self.media_explorer.add_selected_media:
            self.add_selected_media()

        self.toolbar.is_active = self.menu.active_button and self.menu.active_button.value == 'Tools'
        self.toolbar.update()
        self.menu.update()
        self.floating_toolbar.update()

        if self.floating_toolbar.copy_poly_points:
            self.create_image_panel_from_poly_points()
            self.floating_toolbar.copy_poly_points = False

        self.main_draw_space.update()

        self.tooltip_image = None
        mouse_cursor = pygame.SYSTEM_CURSOR_ARROW
        if self.menu.is_hovered:
            mouse_cursor = self.menu.mouse_cursor
        elif self.toolbar.is_hovered:
            mouse_cursor = self.toolbar.mouse_cursor
            if self.toolbar.hovered_button and self.toolbar.hovered_button.tooltip:
                self.set_tooltip(self.toolbar.hovered_button.tooltip)
        elif self.media_explorer.is_hovered:
            mouse_cursor = self.media_explorer.mouse_cursor
            if self.media_explorer.hovered_button and self.media_explorer.hovered_button.tooltip:
                self.set_tooltip(self.media_explorer.hovered_button.tooltip)


        if mouse_cursor is not self.mouse_cursor:
            self.mouse_cursor = mouse_cursor
            pygame.mouse.set_cursor(self.mouse_cursor)

    def draw(self):
        bg_fill = config.display_bg_color
        self.surface.fill(bg_fill)

        self.main_draw_space.draw(self.surface)
        self.media_explorer.draw(self.surface)
        self.floating_toolbar.draw(self.surface)
        self.toolbar.draw(self.surface)
        self.menu.draw(self.surface)

        if self.tooltip_image:
            self.surface.blit(self.tooltip_image, self.tooltip_rect)

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
