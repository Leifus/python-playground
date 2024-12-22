from classes.button import Button
from classes.game_mode_enum import GameModeEnum
from classes.game_sprite import GameSprite
from config import pygame
from globals import media_manager

class GameLobby(GameSprite):
    def __init__(self, size, position):
        super(GameSprite, self).__init__()
        
        self.size = size
        self.position = position
        self.is_active = False
        self.button_group = pygame.sprite.Group()
        self.start_new_game = False
        self.selected_game_mode: GameModeEnum = GameModeEnum.NONE

        self.setup_visuals()

    def setup_visuals(self):
        #Housing
        media = 'UI/spr_UI_Popup.png'
        img = media_manager.get(media)
        img = pygame.transform.scale(img, self.size)
        self.orig_image = img
        self.image = self.orig_image
        self.rect = self.image.get_rect(center=self.position)

        #Buttons
        outer_margin_x = 40
        outer_margin_y = 50
        button_size = (200, 80)
        button_spacing = 10
        button_surface = pygame.Surface(button_size, pygame.SRCALPHA)
        
        row = 0
        col = 0
        for i, game_mode in enumerate(GameModeEnum):
            if game_mode == GameModeEnum.NONE:
                continue

            x = outer_margin_x + button_size[0]*col + button_spacing + button_spacing*col
            y = outer_margin_y + button_size[1]*row + button_spacing + button_spacing*row
            if x > self.size[0]:
                col = 0
                row += 1
            else:
                col += 1

            button_color = pygame.Color('cadetblue1')
            font_family = 'freesansbold.ttf'
            font_size = 20
            font_color = pygame.Color('black')
            font = pygame.font.Font(font_family, font_size)
            value = game_mode.name
            position = (x, y)
            label = value
            on_hover = self.on_button_hover
            on_press = self.on_button_press
            on_release = None
            
            surface = button_surface.copy()
            surface.fill(button_color)

            text = font.render(label, True, font_color)
            text_rect = text.get_rect(center=surface.get_rect().center)
            surface.blit(text, text_rect)

            button = Button(surface, position, value, on_hover, on_press, on_release)
            self.button_group.add(button)

    def on_event(self, parent_mouse_position, event: pygame.event.Event):
        self.hovered_component = None

        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return
        
        self.relative_mouse_position = (parent_mouse_position[0] - self.rect.left, parent_mouse_position[1] - self.rect.top)
        
        for button in self.button_group:
            button.on_event(self.relative_mouse_position, event)

    def on_button_hover(self, button: Button):
        self.hovered_component = button
         
    def on_button_press(self, button: Button):
        self.start_new_game = True
        self.selected_game_mode = button.value

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def draw(self, surface: pygame.Surface):
        for button in self.button_group:
            self.image.blit(button.image, button.position)

        surface.blit(self.image, self.rect)