from classes.common.button import Button
from classes.common.game_sprite import GameSprite
from config import pygame
from globals import media_manager

class InstructionsPanel(GameSprite):
    def __init__(self, position):
        super().__init__()

        self.size = (180, 200)
        self.position = position
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=self.position)
        self.housing_surface: pygame.Surface = None 
        self.title_image: pygame.Surface = None 
        self.info_button_image: pygame.Surface = None 
        self.bg_color = pygame.Color('white')
        self.border_color = pygame.Color('gray80')
        self.instructions = []
        self.is_active = False
        self.info_button: Button = None
        self.button_group = pygame.sprite.Group()
        self.button_size = 32

        self.setup_visuals()
        self.setup_button()

    def on_button_press(self, button: Button):
        self.is_active = not self.is_active

    def setup_button(self):
        on_press = self.on_button_press
        active_surface = None
        self.info_button = Button(self.info_button_image, (0,0), 1, on_hover=None, on_press=on_press, on_release=None, active_surface=active_surface)
        self.button_group.add(self.info_button)

    def setup_visuals(self):
        # Housing
        self.housing_surface = self.surface.copy()
        self.housing_surface.fill(self.bg_color)

        pygame.draw.rect(self.housing_surface, self.border_color, pygame.Rect(0,0,self.rect.width, self.rect.height), 2)

        #Instructions Icon Button
        image = media_manager.get('icons/infomark_icon.png', convert_alpha=True)
        icon_scale = 0.7
        button_icon = pygame.transform.scale(image, (self.button_size*icon_scale, self.button_size*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size/2, self.button_size/2))
        button_surface = pygame.Surface((self.button_size, self.button_size), pygame.SRCALPHA)
        button_border_surface = button_surface.copy()
        button_surface.fill(self.bg_color)
        pygame.draw.rect(button_border_surface, self.border_color, pygame.Rect(0,0,self.button_size, self.button_size), 2)

        button_image = button_surface.copy()
        button_image.blit(button_border_surface, (0,0))
        button_image.blit(button_icon, icon_rect)
        self.info_button_image = button_image


        # Instructions
        font_size = 12
        font_color = pygame.Color('black')
        font = pygame.font.Font('freesansbold.ttf', font_size)

        self.title_image = font.render('INSTRUCTIONS', True, font_color, self.bg_color)
        title_image_rect = self.title_image.get_rect()
        instructions = [
            'A = Zoom in (0.1)',
            'Z = Zoom out (-0.1)',
            'D = Delete poly point',
            'SHIFT = Add poly point'
        ]

        line_gap = 10
        x = 10
        y = title_image_rect.height + line_gap*3
        for instruction in instructions:
            surface = font.render(instruction, True, font_color, self.bg_color)
            rect = surface.get_rect(topleft=(x, y))
            self.instructions.append((surface, rect))
            y += rect.height + line_gap


    def on_event(self, mouse_position: pygame.Vector2, event: pygame.event.Event):
        if mouse_position:
            relative_mouse_position = (mouse_position.x - self.rect.left, mouse_position.y - self.rect.top)
            for button in self.button_group:
                button: Button
                button.on_event(relative_mouse_position, event)

    def update(self, *args, **kwargs):
        self.button_group.update()
        return super().update(*args, **kwargs)
    
    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        if self.is_active:
            self.surface.blit(self.housing_surface, (0,0))
            self.surface.blit(self.title_image, (self.info_button.rect.right + 6, 10))
            self.surface.blits(self.instructions)

        self.button_group.draw(self.surface)

        self.image = self.surface
        surface.blit(self.image, self.rect)