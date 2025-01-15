from classes.common.game_sprite import GameSprite
from config import pygame

class TextBox(GameSprite):
    def __init__(self, label, textbox_size, position, value, on_submit, font_size=14):
        super(TextBox, self).__init__()

        self.label = label
        self.position = position
        self.value: str = str(value)
        self.is_focused = False
        self.is_hovered = False
        self.font_size = font_size
        self.textbox_size = textbox_size
        self.label_font_size = 12
        self.font_color = pygame.Color('black')
        self.on_submit = on_submit

        self.label_surface: pygame.Surface = None
        self.label_rect: pygame.Rect = None
        self.textbox_surface: pygame.Surface = None

        self.setup_visuals()

    def setup_visuals(self):
        # Label
        font = pygame.font.Font('freesansbold.ttf', self.label_font_size)
        self.label_surface = font.render(self.label, True, self.font_color)
        label_rect = self.label_surface.get_rect()

        # Main Surface
        label_margin_x = 10
        height = self.textbox_size[1] if label_rect.height < self.textbox_size[1] else label_rect.height
        self.size = (self.textbox_size[0] + label_margin_x + label_rect.width, height)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=self.position)
        
        # Textbox
        self.textbox_surface = pygame.Surface(self.textbox_size, pygame.SRCALPHA)
        self.textbox_surface.fill('white')
        pygame.draw.rect(self.textbox_surface, self.font_color, (0,0,self.textbox_size[0], self.textbox_size[1]), 1)
        textbox_rect = self.textbox_surface.get_rect()
        label_rect.midleft = (textbox_rect.right + label_margin_x, textbox_rect.height/2)
        self.label_rect = label_rect


    def on_event(self, mouse_position: pygame.Vector2, event: pygame.event.Event):
        is_in_x = False
        is_in_y = False
        if mouse_position:
            is_in_x = mouse_position[0] >= self.rect.left and mouse_position[0] <= self.rect.right
            is_in_y = mouse_position[1] >= self.rect.top and mouse_position[1] <= self.rect.bottom

        self.is_hovered = is_in_x and is_in_y

        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            buttons_pressed = pygame.mouse.get_pressed()
            if self.is_hovered and event.type == pygame.MOUSEBUTTONDOWN and buttons_pressed[0]:
                self.is_focused = True
            elif not self.is_hovered:
                self.is_focused = False

        if self.is_focused and event.type == pygame.KEYDOWN:
            keys_pressed = pygame.key.get_pressed()
            key_pressed = pygame.key.name(event.key)
            if keys_pressed[pygame.K_BACKSPACE]:
                self.remove_character()
            elif keys_pressed[pygame.K_RETURN]:
                self.is_focused = False
                if self.on_submit:
                    self.on_submit(self)
            elif key_pressed.isdigit():
                self.add_character(key_pressed)

    def remove_character(self):
        if len(self.value) > 0:
            self.value = self.value[:-1]
            
    def add_character(self, char):
        self.value = f'{self.value}{char}'

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        # Textbox
        self.surface.blit(self.textbox_surface, (0,0))

        # Label
        self.surface.blit(self.label_surface, self.label_rect)

        # Value
        value_font = pygame.font.Font('freesansbold.ttf', self.font_size)
        value_image = value_font.render(f'{self.value}', True, self.font_color)
        value_rect = value_image.get_rect(topleft=(3, self.textbox_size[1]/2 - self.font_size/2))
        self.surface.blit(value_image, value_rect)

        if self.is_focused:
            # Input Cursor line
            start_pos = (value_rect.right, value_rect.top)
            end_pos = (start_pos[0], value_rect.bottom)
            width = 2
            cursor_color = pygame.Color('darkgoldenrod1')
            pygame.draw.line(self.surface, cursor_color, start_pos, end_pos, width)
        
        surface.blit(self.surface, self.rect)

        