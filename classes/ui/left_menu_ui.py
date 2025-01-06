
from classes.common.button import Button
from classes.common.game_sprite import GameSprite
from classes.common.text_box import TextBox
from globals import media_manager
from config import pygame

class LeftMenuUI(GameSprite):
    def __init__(self, size, position):
        super(LeftMenuUI, self).__init__()

        self.size = size
        self.position = position
        self.padding = 12
        self.font_size = 14
        self.font_color = pygame.Color('black')

        self.checkbox_unchecked: pygame.Surface = None
        self.checkbox_checked: pygame.Surface = None
        self.show_image_btn_on_surface: pygame.Surface = None
        self.show_image_btn_off_surface: pygame.Surface = None
        self.show_mask_btn_on_surface: pygame.Surface = None
        self.show_mask_btn_off_surface: pygame.Surface = None
        self.show_poly_btn_on_surface: pygame.Surface = None
        self.show_poly_btn_off_surface: pygame.Surface = None
        self.buttons_group = pygame.sprite.Group()
        self.inputs_group = pygame.sprite.Group()
        self.mouse_position: pygame.Vector2 = None
        self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW
        self.show_image = True
        self.show_mask = False
        self.show_poly = True
        self.poly_points_every = 30
        self.poly_line_width = 2
        self.poly_point_radius = 2
        self.image_alpha = 160
        self.mask_alpha = 150
        self.poly_points_every_input: TextBox = None
        self.is_hovered = False

        self.create_default_surface()
        self.setup_visuals()
        self.setup_image_options()
        self.setup_mask_options()
        self.setup_poly_trace_options()
        self.redraw()

    def on_event(self, event: pygame.event.Event):
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            mouse_x, mouse_y = event.pos
            self.mouse_position = pygame.Vector2(mouse_x - self.rect.left, mouse_y - self.rect.top)

        for button in self.buttons_group:
            button: Button
            button.on_event(self.mouse_position, event)

        for input in self.inputs_group:
            input: TextBox
            input.on_event(self.mouse_position, event)

    def on_show_mask_button_press(self, button: Button):
        self.show_mask = button.value
        button.value = not self.show_mask
        if self.show_mask:
            button.image = self.show_mask_btn_on_surface
        else:
            button.image = self.show_mask_btn_off_surface

    def on_show_poly_trace_button_press(self, button: Button):
        self.show_poly = button.value
        button.value = not self.show_poly
        if self.show_poly:
            button.image = self.show_poly_btn_on_surface
        else:
            button.image = self.show_poly_btn_off_surface

    def on_show_image_button_press(self, button: Button):
        self.show_image = button.value
        button.value = not self.show_image
        if self.show_image:
            button.image = self.show_image_btn_on_surface
        else:
            button.image = self.show_image_btn_off_surface

    def set_poly_points_every(self, poly_points_every):
        self.poly_points_every = poly_points_every
        self.poly_points_every_input.value = str(poly_points_every)

    def setup_poly_trace_options(self):
        start_y = 190
        position = (self.padding, start_y)
        value = not self.show_poly
        on_hover = None
        on_press = self.on_show_poly_trace_button_press
        on_release = None
        button = Button(self.show_poly_btn_on_surface, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(button)

        textbox_size = (40, 22)
        start_y += 25
        position = (self.padding, start_y)
        on_submit = self.on_poly_trace_points_change
        label = 'point every'
        value = self.poly_points_every
        self.poly_points_every_input = TextBox(label, textbox_size, position, value, on_submit)
        self.inputs_group.add(self.poly_points_every_input)

        textbox_size = (40, 22)
        start_y += 25
        position = (self.padding, start_y)
        on_submit = self.on_poly_trace_line_width_change
        label = 'line width'
        value = self.poly_line_width
        poly_line_width_input = TextBox(label, textbox_size, position, value, on_submit)
        self.inputs_group.add(poly_line_width_input)

        textbox_size = (40, 22)
        start_y += 25
        position = (self.padding, start_y)
        on_submit = self.on_poly_trace_point_radius_change
        label = 'point radius'
        value = self.poly_point_radius
        poly_point_radius_input = TextBox(label, textbox_size, position, value, on_submit)
        self.inputs_group.add(poly_point_radius_input)

    def on_mask_alpha_change(self, textbox: TextBox):
        self.mask_alpha = int(textbox.value)

    def on_image_alpha_change(self, textbox: TextBox):
        self.image_alpha = int(textbox.value)

    def on_poly_trace_point_radius_change(self, textbox: TextBox):
        self.poly_point_radius = int(textbox.value)

    def on_poly_trace_line_width_change(self, textbox: TextBox):
        self.poly_line_width = int(textbox.value)

    def on_poly_trace_points_change(self, textbox: TextBox):
        self.poly_points_every = int(textbox.value)

    def setup_mask_options(self):
        # Show Mask Button
        start_y = 110
        position = (self.padding, start_y)
        value = not self.show_mask
        on_hover = None
        on_press = self.on_show_mask_button_press
        on_release = None
        button = Button(self.show_mask_btn_off_surface, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(button)

        # Mask Alpha
        textbox_size = (40, 22)
        start_y += 30
        position = (self.padding, start_y)
        on_submit = self.on_mask_alpha_change
        label = 'alpha'
        value = self.mask_alpha
        alpha_input = TextBox(label, textbox_size, position, value, on_submit)
        self.inputs_group.add(alpha_input)

    def setup_image_options(self):
        # Show image button
        position = (self.padding, 40)
        value = not self.show_image
        on_hover = None
        on_press = self.on_show_image_button_press
        on_release = None
        button = Button(self.show_image_btn_on_surface, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(button)

        # Image Alpha
        textbox_size = (40, 22)
        position = (self.padding, 70)
        on_submit = self.on_image_alpha_change
        label = 'alpha'
        value = self.image_alpha
        alpha_input = TextBox(label, textbox_size, position, value, on_submit)
        self.inputs_group.add(alpha_input)


    def setup_visuals(self):
        # Housing
        color = pygame.Color('gray80')
        self.orig_image.fill(color)

        # Housing Edge
        color = pygame.Color('gray70')
        width = 2
        start_pos = (self.size[0]-width, 0)
        end_pos = (self.size[0]-width, self.size[1])
        pygame.draw.line(self.orig_image, color, start_pos, end_pos, width)

        # Image Options
        title = 'Image Options'
        title_font = pygame.font.Font('freesansbold.ttf', self.font_size)
        
        title_image = title_font.render(title, True, self.font_color)
        title_rect = title_image.get_rect(topleft=(self.padding, self.padding))
        self.orig_image.blit(title_image, title_rect)

        # Checkbox unchecked
        checkbox_size = (self.font_size,self.font_size)
        checkbox_surface = pygame.Surface(checkbox_size, pygame.SRCALPHA)
        line_width = 2
        pygame.draw.rect(checkbox_surface, self.font_color, checkbox_surface.get_rect(), line_width)
        self.checkbox_unchecked = checkbox_surface

        # Checkbox checked
        checkbox_surface = pygame.Surface(checkbox_size, pygame.SRCALPHA)
        checked_color = pygame.Color('green')
        checkbox_surface.fill(checked_color)
        checkbox_rect = checkbox_surface.get_rect()
        pygame.draw.rect(checkbox_surface, self.font_color, checkbox_rect, line_width)
        pygame.draw.line(checkbox_surface, self.font_color, (0-line_width/2, 0-line_width/2), (checkbox_rect.width-line_width/2, checkbox_rect.height-line_width/2), line_width)
        pygame.draw.line(checkbox_surface, self.font_color, (0-line_width/2, checkbox_rect.height-line_width/2), (checkbox_rect.width-line_width/2, 0-line_width/2), line_width)
        self.checkbox_checked = checkbox_surface

        # Show Image Button
        button_size = (120, 20)
        button_surface = pygame.Surface(button_size, pygame.SRCALPHA)
        title = 'show image'
        smaller_font_size = round(self.font_size*0.9)
        smaller_font = pygame.font.Font('freesansbold.ttf', smaller_font_size)
        title_image = smaller_font.render(title, True, self.font_color)
        title_rect = title_image.get_rect()
        line_heght = self.font_size
        button_surface.blit(title_image, (24, (button_size[1]/2)-line_heght/2))
        self.show_image_btn_on_surface = button_surface.copy()
        self.show_image_btn_on_surface.blit(self.checkbox_checked, (4, (button_size[1]/2)-checkbox_rect.height/2))
        self.show_image_btn_off_surface = button_surface.copy()
        self.show_image_btn_off_surface.blit(self.checkbox_unchecked, (4, (button_size[1]/2)-checkbox_rect.height/2))

        # Show Mask Button
        button_size = (120, 20)
        button_surface = pygame.Surface(button_size, pygame.SRCALPHA)
        title = 'show mask'
        smaller_font_size = round(self.font_size*0.9)
        smaller_font = pygame.font.Font('freesansbold.ttf', smaller_font_size)
        title_image = smaller_font.render(title, True, self.font_color)
        title_rect = title_image.get_rect()
        line_heght = self.font_size
        button_surface.blit(title_image, (24, (button_size[1]/2)-line_heght/2))
        self.show_mask_btn_on_surface = button_surface.copy()
        self.show_mask_btn_on_surface.blit(self.checkbox_checked, (4, (button_size[1]/2)-checkbox_rect.height/2))
        self.show_mask_btn_off_surface = button_surface.copy()
        self.show_mask_btn_off_surface.blit(self.checkbox_unchecked, (4, (button_size[1]/2)-checkbox_rect.height/2))

        # Show Poly Button
        button_size = (120, 20)
        button_surface = pygame.Surface(button_size, pygame.SRCALPHA)
        title = 'show poly'
        smaller_font_size = round(self.font_size*0.9)
        smaller_font = pygame.font.Font('freesansbold.ttf', smaller_font_size)
        title_image = smaller_font.render(title, True, self.font_color)
        title_rect = title_image.get_rect()
        line_heght = self.font_size
        button_surface.blit(title_image, (24, (button_size[1]/2)-line_heght/2))
        self.show_poly_btn_on_surface = button_surface.copy()
        self.show_poly_btn_on_surface.blit(self.checkbox_checked, (4, (button_size[1]/2)-checkbox_rect.height/2))
        self.show_poly_btn_off_surface = button_surface.copy()
        self.show_poly_btn_off_surface.blit(self.checkbox_unchecked, (4, (button_size[1]/2)-checkbox_rect.height/2))

    def redraw(self):
        self.image = pygame.transform.scale(self.orig_image, self.size)
        self.rect = self.image.get_rect(center=self.position)

    def update(self, *args, **kwargs):
        self.buttons_group.update(self.mouse_position)
        self.inputs_group.update(self.mouse_position)

        hovered_button: Button = None
        for button in self.buttons_group:
            button: Button
            if button.is_hovered:
                hovered_button = button
                break

        self.is_hovered = hovered_button is not None
        
        if hovered_button:
            self.mouse_cursor = pygame.SYSTEM_CURSOR_HAND
        else:
            self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW

        for input in self.inputs_group:
            input: TextBox
            if input.is_hovered:
                self.mouse_cursor = pygame.SYSTEM_CURSOR_IBEAM
                break
            
        return super().update(*args, **kwargs)
    
    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))
        self.surface.blit(self.image, (0,0))

        for button in self.buttons_group:
            button: Button
            self.surface.blit(button.image, button.rect)

        for input in self.inputs_group:
            input: TextBox
            input.draw(self.surface)

        surface.blit(self.surface, self.rect)
