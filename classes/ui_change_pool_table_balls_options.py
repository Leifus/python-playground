from classes.game_mode_enum import GameModeEnum
from classes.game_sprite import GameSprite
from config import pygame, pool_balls_config
from classes.draw_mode_enum import DrawModeEnum
from classes.button import Button
from globals import media_manager

class UIChangePoolTableBallsOptions(GameSprite):
    def __init__(self, draw_mode, size, position, on_change_balls):
        super(GameSprite, self).__init__()
        
        self.draw_mode = draw_mode
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
        self.game_mode: GameModeEnum = GameModeEnum.NONE

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

        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)

        self.title_orig_image: pygame.Surface | None = None
        self.housing_orig_image: pygame.Surface | None = None

        self.relative_mouse_position = None
        self.hovered_component = None

        self.ball_sets = []

        self.setup_visuals()
        self.recreate_buttons()
        self.redraw()

    def redraw(self):
        self.image.fill((0,0,0,0))

        # Title
        title_image = self.title_orig_image
        title_rect = title_image.get_rect(topleft=(self.outer_margin, 0))
        
        # Housing
        size = (self.size[0], self.size[1] - title_rect.height)
        housing_image = pygame.transform.scale(self.housing_orig_image, size)
        housing_rect = housing_image.get_rect(topleft=(0, title_rect.height))

        # Buttons
        for button in self.buttons_group:
            housing_image.blit(button.image, button.rect)

        self.image.blit(housing_image, housing_rect)
        self.image.blit(title_image, title_rect)
     
    def setup_visuals(self):
        self.title_orig_image = self.font.render(self.title, True, self.font_color)

        if self.draw_mode in DrawModeEnum.RICH:
            # Housing
            self.housing_orig_image = media_manager.get(self.housing_RICH_media)

        # title = self.font.render(self.title, True, self.font_color)
        # self.title_rect = title.get_rect(topleft=(self.outer_margin, 0))

        # if self.draw_mode in DrawModeEnum.RAW | DrawModeEnum.WIREFRAME:
        #     outline_width = 0
        #     if self.draw_mode in DrawModeEnum.WIREFRAME:
        #         outline_width = self.WIREFRAME_outline_width

        #     # Housing
        #     rect = self.housing_surface.get_rect(topleft=(0, self.title_rect.height))
        #     pygame.draw.rect(self.housing_surface, self.housing_RAW_color, rect, outline_width)
        # elif self.draw_mode in DrawModeEnum.RICH:
        #     # Housing
        #     img = media_manager.get(self.housing_RICH_media)
        #     size = (self.size[0], self.size[1] - self.title_rect.height)
        #     self.housing_RICH_surface = pygame.transform.scale(img, size)
        #     rect = self.housing_RICH_surface.get_rect(topleft=(0, self.title_rect.height))

        #     self.housing_surface.blit(self.housing_RICH_surface, rect)

        # self.housing_surface.blit(title, self.title_rect)

    def recreate_buttons(self):
        self.buttons_group.empty()

        row = 0
        col = 0
        on_hover = self.on_button_hover
        on_press = self.on_button_press
        on_release = None
        font_family = 'freesansbold.ttf'
        font_size = 12
        font_color = pygame.Color('black')
        font = pygame.font.Font(font_family, font_size)
        button_color = pygame.Color('white')
        for i, ball_set in enumerate(self.ball_sets):
            x = self.outer_margin + self.button_size[0]*col + self.button_spacing*col
            y = self.outer_margin + self.button_size[1]*row + self.button_spacing + self.button_spacing*row
            if x > self.size[0]:
                col = 0
                row += 1
            else:
                col += 1
            
            button_image = pygame.Surface(self.button_size, pygame.SRCALPHA)
            button_image.fill(button_color)

            label = ball_set[0]
            text = font.render(label, True, font_color)
            text_rect = text.get_rect(center=button_image.get_rect().center)
            button_image.blit(text, text_rect)

            position = (x, y)
            value = i
            button = Button(button_image, position, value, on_hover, on_press, on_release)
            self.buttons_group.add(button)

    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        self.hovered_component = None

        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return
        
        self.relative_mouse_position = (parent_mouse_position[0] - self.rect.left, parent_mouse_position[1] - self.rect.top)
        
        relative_button_mouse_pos = (self.relative_mouse_position[0], self.relative_mouse_position[1] - self.title_height)
        for button in self.buttons_group:
            button.on_event(relative_button_mouse_pos, event)

    def on_button_hover(self, button: Button):
        self.hovered_component = button
         
    def on_button_press(self, button: Button):
        self.on_change_balls(button.value)

    def update_game_mode(self, game_mode: GameModeEnum):
        self.game_mode = game_mode

        if self.game_mode is GameModeEnum.BILLIARDS:
            self.ball_sets = pool_balls_config.billiard_ball_sets
        elif self.game_mode is GameModeEnum.SNOOKER:
            self.ball_sets = pool_balls_config.snooker_ball_sets

        self.recreate_buttons()
        self.redraw()

    def update(self, game_mode: GameModeEnum, *args, **kwargs):
        if game_mode != self.game_mode:
            self.update_game_mode(game_mode)
            
        return super().update(*args, **kwargs)