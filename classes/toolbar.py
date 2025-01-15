from classes.common.button import Button
from classes.common.game_sprite import GameSprite
from classes.common.text_box import TextBox
from classes.image_panel import ImagePanel
from config import pygame
from globals import media_manager

class Toolbar(GameSprite):
    def __init__(self, position, size):
        super(Toolbar, self).__init__()

        self.position = position
        self.size = size
        self.is_hovered = False
        self.is_active = False
        self.button_size = 28
        self.button_gap = 10
        self.move_button_default_image: pygame.Surface = None
        self.move_button_hover_image: pygame.Surface = None
        self.move_button_active_image: pygame.Surface = None
        self.show_button_image: pygame.Surface = None
        self.hide_button_image: pygame.Surface = None
        self.buttons_group = pygame.sprite.Group()
        self.inputs_group = pygame.sprite.Group()
        self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW
        self.active_image_panel: ImagePanel = None
        self.hovered_button: Button = None
        self.button_labels = []
        self.relative_mouse_position = None

        self.toggle_show_image_button: Button = None
        self.image_alpha_textbox: TextBox = None
        self.toggle_show_poly_points_button: Button = None

        self.show_image = False
        self.show_poly_points = False

        self.setup_visuals()
        self.setup_toolbar()
        self.redraw()

    def setup_visuals(self):
        # Housing 
        self.housing_image = pygame.Surface(self.size, pygame.SRCALPHA)
        color = pygame.Color('gray90')
        self.housing_image.fill(color)

        # Housing Edge
        color = pygame.Color('gray70')
        thickness = 2
        start_pos = (self.size[0]-thickness, 0)
        end_pos = (self.size[0]-thickness, self.size[1])
        pygame.draw.line(self.housing_image, color, start_pos, end_pos, thickness)

        # Buttons
        button_default_bg_color = pygame.Color('gray95')
        button_hover_bg_color = pygame.Color('gray80')
        button_active_bg_color = pygame.Color('gold')
        button_border_color = pygame.Color('gray80')
        button_border_width = 1
        button_surface = pygame.Surface((self.button_size, self.button_size), pygame.SRCALPHA)
        button_border_surface = button_surface.copy()
        button_surface.fill(button_default_bg_color)
        pygame.draw.rect(button_border_surface, button_border_color, pygame.Rect(0,0,self.button_size,self.button_size), button_border_width)

        # Show Button
        image = media_manager.get('icons/show_icon.png', convert_alpha=True)
        icon_scale = 0.7
        button_icon = pygame.transform.scale(image, (self.button_size*icon_scale, self.button_size*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size/2, self.button_size/2))
        button_image = button_surface.copy()
        button_image.blit(button_border_surface, (0,0))
        button_image.blit(button_icon, icon_rect)
        self.show_button_image = button_image

        # Hide Button
        image = media_manager.get('icons/hide_icon.png', convert_alpha=True)
        icon_scale = 0.7
        button_icon = pygame.transform.scale(image, (self.button_size*icon_scale, self.button_size*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size/2, self.button_size/2))
        button_image = button_surface.copy()
        button_image.blit(button_border_surface, (0,0))
        button_image.blit(button_icon, icon_rect)
        self.hide_button_image = button_image


        # Move Button
        image = media_manager.get('icons/move_icon.png', convert_alpha=True)
        icon_scale = 0.8
        button_icon = pygame.transform.scale(image, (self.button_size*icon_scale, self.button_size*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size/2, self.button_size/2))

        # default
        button_image = button_surface.copy()
        button_image.blit(button_border_surface, (0,0))
        button_image.blit(button_icon, icon_rect)
        self.move_button_default_image = button_image

        # hover
        button_image = button_surface.copy()
        button_image.fill(button_hover_bg_color)
        button_image.blit(button_border_surface, (0,0))
        button_image.blit(button_icon, icon_rect)
        self.move_button_hover_image = button_image

        # active
        button_image = button_surface.copy()
        button_image.fill(button_active_bg_color)
        button_image.blit(button_border_surface, (0,0))
        button_image.blit(button_icon, icon_rect)
        self.move_button_active_image = button_image

    def on_event(self, mouse_position: pygame.Vector2, event: pygame.event.Event):
        self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW
        self.relative_mouse_position = None

        is_in_x = False
        is_in_y = False
        if mouse_position:
            self.relative_mouse_position = (mouse_position.x - self.rect.left, mouse_position.y - self.rect.top)
            is_in_x = self.relative_mouse_position[0] >= self.rect.left and self.relative_mouse_position[0] <= self.rect.right
            is_in_y = self.relative_mouse_position[1] >= self.rect.top and self.relative_mouse_position[1] <= self.rect.bottom

        self.is_hovered = is_in_x and is_in_y

        self.hovered_button = None
        if self.active_image_panel: # Only check toolbar when there's an active panel
            for button in self.buttons_group:
                button: Button
                button.on_event(self.relative_mouse_position, event)
                if button.is_hovered:
                    self.hovered_button = button

            for input in self.inputs_group:
                input: TextBox
                input.on_event(self.relative_mouse_position, event)
                if input.is_hovered: 
                    pass
                    # self.input_is_hovered = True

        if self.hovered_button:
            self.mouse_cursor = pygame.SYSTEM_CURSOR_HAND

    def update(self, *args, **kwargs):
        self.inputs_group.update(self, self.relative_mouse_position)

        return super().update(*args, **kwargs)

    def redraw(self):
        self.image = pygame.transform.scale(self.housing_image, self.size)
        self.rect = self.image.get_rect(center=self.position)

    def draw(self, surface: pygame.Surface):
        if not self.is_active:
            return
        
        self.buttons_group.draw(self.image)
        for button_label, position in self.button_labels:
            self.image.blit(button_label, position)

        for input in self.inputs_group:
            input: TextBox
            input.draw(self.image)

        surface.blit(self.image, self.rect)

    
    def setup_toolbar(self):
        x = self.button_gap/2
        y = self.button_gap

        font = pygame.font.Font('freesansbold.ttf', 12)
        color = pygame.Color('black')

        # Show/Hide Image Button
        button_y = y
        position = (x,y)
        value = False
        tooltip = 'Show/Hide Image'
        on_hover = None
        on_press = self.on_toggle_show_image_button_press
        on_release = None
        self.toggle_show_image_button = Button(self.show_button_image, position, value, on_hover, on_press, on_release, active_surface=self.hide_button_image, tooltip=tooltip)
        self.buttons_group.add(self.toggle_show_image_button)
        
        label_surface = font.render('Image', True, color)
        label_rect = label_surface.get_rect()
        x += 5 + self.toggle_show_image_button.rect.width
        this_y = y + self.toggle_show_image_button.rect.height/2 - label_rect.height/2
        position = (x, this_y)
        self.button_labels.append((label_surface, position))

        # Image Alpha TextBox
        textbox_size = (27,20)
        x = self.size[0] - textbox_size[0] - self.button_gap
        this_y = y + self.toggle_show_image_button.rect.height/2 - textbox_size[1]/2
        position = (x, this_y)
        value = 255
        on_submit = self.on_image_alpha_submit
        font_size = 11
        self.image_alpha_textbox = TextBox('', textbox_size, position, value, on_submit, font_size)
        self.inputs_group.add(self.image_alpha_textbox)



        # Show/Hide Poly Points
        x = self.button_gap/2
        y += self.button_size + self.button_gap
        position = (x,y)
        value = False
        tooltip = 'Show/Hide Poly Points'
        on_hover = None
        on_press = self.on_toggle_show_poly_points_button_press
        on_release = None
        self.toggle_show_poly_points_button = Button(self.show_button_image, position, value, on_hover, on_press, on_release, active_surface=self.hide_button_image, tooltip=tooltip)
        self.buttons_group.add(self.toggle_show_poly_points_button)
        
        label_surface = font.render('Poly Points', True, color)
        label_rect = label_surface.get_rect()
        x += 5 + self.toggle_show_poly_points_button.rect.width
        y += self.toggle_show_poly_points_button.rect.height/2 - label_rect.height/2
        position = (x, y)
        self.button_labels.append((label_surface, position))

        # # Move Button
        # position = (x,y)
        # value = 'move'
        # tooltip = 'Move panels'
        # on_hover = None
        # on_press = self.on_move_button_press
        # on_release = None
        # self.move_button = Button(self.move_button_default_image, position, value, on_hover, on_press, on_release, hover_surface=self.move_button_hover_image, active_surface=self.move_button_active_image, tooltip=tooltip)
        # self.buttons_group.add(self.move_button)

    def update_buttons(self):
        self.toggle_show_image_button.image = self.show_button_image if self.show_image else self.hide_button_image
        self.toggle_show_poly_points_button.image = self.show_button_image if self.show_poly_points else self.hide_button_image

    def set_active_image_panel(self, image_panel: ImagePanel):
        self.show_image = image_panel.show_image
        self.toggle_show_image_button.value = not self.show_image
        self.image_alpha_textbox.value = str(image_panel.image_alpha)
        self.show_poly_points = image_panel.show_live_polys
        self.toggle_show_poly_points_button.value = not self.show_poly_points
        self.update_buttons()

        image_panel.is_active = True
        image_panel.redraw_housing_box()
        self.active_image_panel = image_panel

    def on_image_alpha_submit(self, textbox: TextBox):
        self.active_image_panel.image_alpha = int(textbox.value)
        self.active_image_panel.redraw_sprite_image()
        self.image_alpha_textbox.is_focused = True
        
    def on_toggle_show_image_button_press(self, button: Button):
        if not self.active_image_panel:
            return
        
        show_image = bool(button.value)
        self.show_image = show_image
        self.active_image_panel.show_image = self.show_image
        
        button.value = not show_image
        self.update_buttons()

    def on_toggle_show_poly_points_button_press(self, button: Button):
        if not self.active_image_panel:
            return
        
        show_poly_points = bool(button.value)
        self.show_poly_points = show_poly_points
        self.active_image_panel.show_live_polys = self.show_poly_points
        
        button.value = not show_poly_points
        self.update_buttons()

    def on_move_button_press(self, button):
        pass