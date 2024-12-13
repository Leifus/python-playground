from config import pygame
from classes.draw_mode import DrawMode
from classes.media_manager import MediaManager
from classes.button import Button

class UIChangePoolTableBallsOptions():
    def __init__(self, draw_mode, size, position, on_change_balls, media_manager: MediaManager):
        self.draw_mode = draw_mode
        self.media_manager = media_manager
        self.position = position
        self.size = size
        self.on_change_balls = on_change_balls
        self.WIREFRAME_outline_width = 2
        self.housing_RAW_color = pygame.Color('white')
        self.housing_RICH_media = 'UI/spr_UI_Popup.png'
        self.outer_margin = 10
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.font_color = pygame.Color('white')
        self.title = 'Change Balls'
        self.title_height = 18
        self.ball_RAW_color_options = []

        floor_DM_RAW_colors = [
            pygame.Color('black'),
            pygame.Color('blue'),
            pygame.Color('pink'),
            pygame.Color('brown'),
            pygame.Color('turquoise'),
            pygame.Color('violetred'),
            pygame.Color('wheat'),
            pygame.Color('yellow2'),
            pygame.Color('salmon'),
            pygame.Color('seagreen1'),
            pygame.Color('mediumpurple2'),
            pygame.Color('indigo'),
        ]

        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)
        self.housing_surface = self.surface.copy()
        self.housing_RICH_surface = None
        self.relative_mouse_position = None
        self.hovered_component = None
        self.title_rect = None

    def setup_visuals(self):
        title = self.font.render(self.title, True, self.font_color)
        self.title_rect = title.get_rect(topleft=(self.outer_margin, 0))

        if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
            outline_width = 0
            if self.draw_mode in DrawMode.WIREFRAME:
                outline_width = self.WIREFRAME_outline_width

            # Housing
            rect = pygame.Rect(0, 0, self.size[0], self.size[1])
            pygame.draw.rect(self.housing_surface, self.housing_RAW_color, rect, outline_width)
        elif self.draw_mode in DrawMode.RICH:
            img = self.media_manager.get(self.housing_RICH_media)
            size = (self.size[0], self.size[1] - self.title_rect.height)
            self.housing_RICH_surface = pygame.transform.scale(img, size)
            rect = self.housing_RICH_surface.get_rect(topleft=(0, self.title_rect.height))

            self.housing_surface.blit(self.housing_RICH_surface, rect)

        self.housing_surface.blit(title, self.title_rect)

    # def setup_change_floor_buttons(self):
    #     font_family = 'freesansbold.ttf'
    #     font_size = 14
    #     font_color = pygame.Color('black')

    #     button_protos = []
    #     if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME:
    #         for color in self.ball_RAW_color_options:
    #             media = None
    #             button_protos.append([
    #                 color, media
    #             ])
    #     elif self.draw_mode in DrawMode.RICH:
    #         color = pygame.Color('black')
    #         for media, scale in self.ball_DM_RICH_medias:
    #             button_protos.append([
    #                 color, media
    #             ])

    #     row = 0
    #     col = 0
    #     for i, data in enumerate(button_protos):
    #         color, media = data
    #         x = self.outer_margin + self.floor_button_size[0]*col + self.floor_button_spacing + self.floor_button_spacing*col
    #         y = self.title_height + self.outer_margin + self.floor_button_size[1]*row + self.floor_button_spacing + self.floor_button_spacing*row
    #         if x > self.size[0]:
    #             col = 0
    #             row += 1
    #         else:
    #             col += 1
            
    #         position = (x + self.floor_button_size[0]/2, y + self.floor_button_size[1]/2)
    #         label = f'{i}'
    #         on_hover = self.on_change_floor_button_hover
    #         on_press = self.on_change_floor_button_press
    #         button = Button(self.floor_button_size, color, label, i, self.draw_mode, position, font_family, font_size, font_color, media, on_hover, on_press, self.media_manager)
    #         self.change_floor_buttons.append(button)
                 
    def on_init(self):
        # self.setup_change_balls_buttons()
        self.setup_visuals()

    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        self.hovered_component = None

        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return
        
        self.relative_mouse_position = (parent_mouse_position[0] - self.rect.left, parent_mouse_position[1] - self.rect.top)

    def update(self):
        pass
        
    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        self.surface.blit(self.housing_surface, (0,0))

        surface.blit(self.surface, self.rect)
