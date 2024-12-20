from config import pygame, pool_balls_config
from classes.draw_mode import DrawMode
from classes.media_manager import MediaManager
from classes.button import Button
import config

class UIChangePoolTableBallsOptions():
    def __init__(self, draw_mode, size, position, on_change_balls, media_manager: MediaManager):
        self.draw_mode = draw_mode
        self.media_manager = media_manager
        self.position = position
        self.size = size
        self.button_size = (100, 40)
        self.on_change_balls = on_change_balls
        self.WIREFRAME_outline_width = 2
        self.housing_RAW_color = pygame.Color('gray45')
        self.housing_RICH_media = 'UI/spr_UI_Popup.png'
        self.outer_margin = 10
        self.button_spacing = 10
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.font_color = pygame.Color('white')
        self.title = 'Change Balls'
        self.title_height = 18
        self.ball_RAW_color_options = []
        self.buttons_group = pygame.sprite.Group()

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
            rect = self.housing_surface.get_rect(topleft=(0, self.title_rect.height))
            pygame.draw.rect(self.housing_surface, self.housing_RAW_color, rect, outline_width)
        elif self.draw_mode in DrawMode.RICH:
            # Housing
            img = self.media_manager.get(self.housing_RICH_media)
            size = (self.size[0], self.size[1] - self.title_rect.height)
            self.housing_RICH_surface = pygame.transform.scale(img, size)
            rect = self.housing_RICH_surface.get_rect(topleft=(0, self.title_rect.height))

            self.housing_surface.blit(self.housing_RICH_surface, rect)

        self.housing_surface.blit(title, self.title_rect)

    def setup_change_balls_buttons(self):
        font_family = 'freesansbold.ttf'
        font_size = 12
        font_color = pygame.Color('black')
        font = pygame.font.Font(font_family, font_size)

        ball_sets = []

        #TODO: Replace this with the game's game mode and not a fixed config value. 
        game_mode = config.game_types[config.active_game_type_index]
        if game_mode == 'Billiards':
            ball_sets = pool_balls_config.billiard_ball_sets
        elif game_mode == 'Snooker':
            ball_sets = pool_balls_config.snooker_ball_sets

        # TODO: FIX THIS CONSTRAINT: THE FOLLOWING WILL ONLY WORK FOR BILLIARDS AT THE MOMENT
        row = 0
        col = 0
        on_hover = self.on_button_hover
        on_press = self.on_button_press
        on_release = None
        button_color = pygame.Color('white')
        media = None
        
        #TODO: Fix this for RICH AND OTHER DRAW MODES
        button_surface = pygame.Surface(self.button_size, pygame.SRCALPHA)
        for i, ball_set_config in enumerate(ball_sets):
            title, radius, use_ball_identifier_as_media, media_folder, mass, elasticity, friction, cue_ball_config, eight_ball_config, spot_ball_config, stripe_ball_config = ball_set_config
            
            x = self.outer_margin + self.button_size[0]*col + self.button_spacing + self.button_spacing*col
            y = self.title_height + self.outer_margin + self.button_size[1]*row + self.button_spacing + self.button_spacing*row
            if x > self.size[0]:
                col = 0
                row += 1
            else:
                col += 1

            value = i
            position = (x, y)
            label = title
            
            surface = button_surface.copy()
            surface.fill(button_color)

            text = font.render(label, True, font_color)
            text_rect = text.get_rect(center=surface.get_rect().center)
            surface.blit(text, text_rect)

            button = Button(surface, position, value, on_hover, on_press, on_release)
            self.buttons_group.add(button)
                 
    def on_init(self):
        self.setup_change_balls_buttons()
        self.setup_visuals()

    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        self.hovered_component = None

        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return
        
        self.relative_mouse_position = (parent_mouse_position[0] - self.rect.left, parent_mouse_position[1] - self.rect.top)
        
        for button in self.buttons_group:
            button.on_event(self.relative_mouse_position, event)

    def on_button_hover(self, button: Button):
        self.hovered_component = button
         
    def on_button_press(self, button: Button):
        self.on_change_balls(button.value)

    def update(self):
        pass
        
    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        self.surface.blit(self.housing_surface, (0,0))

        #TODO: Use .blits()
        for button in self.buttons_group:
            self.surface.blit(button.image, button.position)

        surface.blit(self.surface, self.rect)
