from classes.common.button import Button
from classes.common.game_sprite import GameSprite
from classes.common.text_box import TextBox
from classes.image_panel import ImagePanel
from config import pygame, os
from globals import media_manager

class ImagePanelToolbar(GameSprite):
    def __init__(self):
        super(ImagePanelToolbar, self).__init__()

        self.button_size = 26
        self.linked_image_panel: ImagePanel = None
        self.housing_image: pygame.Surface = None
        self.move_button_image: pygame.Surface = None
        self.toggle_image_button_off_image: pygame.Surface = None
        self.toggle_image_button_on_image: pygame.Surface = None
        self.toggle_mask_button_off_image: pygame.Surface = None
        self.toggle_mask_button_on_image: pygame.Surface = None
        self.toggle_poly_trace_button_off_image: pygame.Surface = None
        self.toggle_poly_trace_button_on_image: pygame.Surface = None
        self.copy_poly_off_image: pygame.Surface = None
        self.cut_button_on_image: pygame.Surface = None
        self.cut_button_off_image: pygame.Surface = None
        self.physics_button_on_image: pygame.Surface = None
        self.physics_button_off_image: pygame.Surface = None
        self.save_button_off_image: pygame.Surface = None
        self.save_button_on_image: pygame.Surface = None
        self.buttons_group = pygame.sprite.Group()
        self.inputs_group = pygame.sprite.Group()
        self.input_size = (34, self.button_size-4)
        self.is_hovered = False
        self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW
        self.mouse_position = None
        self.move_by_mouse = False
        self.move_initial_position = None
        self.move_initial_position_offset = None
        self.parent_mouse_position = None
        self.show_image = True
        self.show_mask = False
        self.show_live_polys = False
        self.copy_poly_points = False
        self.button_gap = 5
        self.has_killed_panel = False
        self.trash_button_gap = 40
        self.button_is_hovered = False
        self.input_is_hovered = False
        self.cut_shape = False
        self.show_physics = False
        self.is_saved = False

        self.move_button: Button = None
        self.show_image_button: Button = None
        self.set_image_alpha_input: TextBox = None
        self.show_mask_button: Button = None
        self.show_live_polys_button: Button = None
        self.copy_poly_button: Button = None
        self.set_poly_points_input: TextBox = None
        self.cut_shape_button: Button = None
        self.physics_button: Button = None
        self.save_button: Button = None
        self.trash_panel_button: Button = None

        self.setup_button_visuals()
        self.setup_toolbar()

        buttons_width = self.button_size*len(self.buttons_group) + self.button_gap*(len(self.buttons_group)+1) + self.trash_button_gap
        width = buttons_width + len(self.inputs_group)*self.input_size[0] + self.button_gap*(len(self.inputs_group))
        height = self.button_size + self.button_gap*2
        self.size = (width, height)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=(self.size[0]/2, self.size[1]/2))
        
        self.setup_visuals()

    def setup_visuals(self):
        # Housing 
        self.housing_image = self.surface.copy()
        self.housing_image.fill('white')
        pygame.draw.rect(self.housing_image, 'gray60', (0,0,self.size[0],self.size[1]), 1)

    def setup_button_visuals(self):
        button_bg_color = pygame.Color('gray92')
        button_active_bg_color = pygame.Color('gold')

        # Button
        button_surface = pygame.Surface((self.button_size, self.button_size), pygame.SRCALPHA)
        button_surface.fill(button_bg_color)

        # Move Button
        image = media_manager.get('icons/move_icon.png', convert_alpha=True)
        icon_scale = 0.8
        button_icon = pygame.transform.scale(image, (self.button_size*icon_scale, self.button_size*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size/2, self.button_size/2))
        button_image = button_surface.copy()
        button_image.blit(button_icon, icon_rect)
        self.move_button_image = button_image

        # Cut Button
        image = media_manager.get('icons/cut_icon.png', convert_alpha=True)
        icon_scale = 0.8
        button_icon = pygame.transform.scale(image, (self.button_size*icon_scale, self.button_size*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size/2, self.button_size/2))
        button_image = button_surface.copy()
        button_image.blit(button_icon, icon_rect)
        self.cut_button_off_image = button_image

        button_image = button_surface.copy()
        button_image.fill(button_active_bg_color)
        button_image.blit(button_icon, icon_rect)
        self.cut_button_on_image = button_image

        # Physics Button
        image = media_manager.get('icons/gravity_icon.png', convert_alpha=True)
        icon_scale = 0.8
        button_icon = pygame.transform.scale(image, (self.button_size*icon_scale, self.button_size*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size/2, self.button_size/2))
        button_image = button_surface.copy()
        button_image.blit(button_icon, icon_rect)
        self.physics_button_off_image = button_image

        button_image = button_surface.copy()
        button_image.fill(button_active_bg_color)
        button_image.blit(button_icon, icon_rect)
        self.physics_button_on_image = button_image

        # Trash Button
        image = media_manager.get('icons/bin_icon.png', convert_alpha=True)
        icon_scale = 0.8
        button_icon = pygame.transform.scale(image, (self.button_size*icon_scale, self.button_size*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size/2, self.button_size/2))
        button_image = button_surface.copy()
        color = pygame.Color('lightpink1')
        button_image.fill(color)
        button_image.blit(button_icon, icon_rect)
        self.trash_button_image = button_image

        # Save Button
        image = media_manager.get('icons/save_icon.png', convert_alpha=True)
        icon_scale = 0.8
        button_icon = pygame.transform.scale(image, (self.button_size*icon_scale, self.button_size*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size/2, self.button_size/2))
        button_image = button_surface.copy()
        button_image.blit(button_icon, icon_rect)
        self.save_button_off_image = button_image

        button_image = button_surface.copy()
        button_image.fill(button_active_bg_color)
        button_image.blit(button_icon, icon_rect)
        self.save_button_on_image = button_image

        # Toggle Image Button
        image = media_manager.get('icons/image_icon.png', convert_alpha=True)
        icon_scale = 0.8
        button_icon = pygame.transform.scale(image, (self.button_size*icon_scale, self.button_size*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size/2, self.button_size/2))
        button_image = button_surface.copy()
        button_image.blit(button_icon, icon_rect)
        self.toggle_image_button_off_image = button_image

        button_image = button_surface.copy()
        button_image.fill(button_active_bg_color)
        button_image.blit(button_icon, icon_rect)
        self.toggle_image_button_on_image = button_image
        
        # Toggle Mask Button
        image = media_manager.get('icons/mask_icon.png', convert_alpha=True)
        icon_scale = 0.8
        button_icon = pygame.transform.scale(image, (self.button_size*icon_scale, self.button_size*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size/2, self.button_size/2))
        button_image = button_surface.copy()
        button_image.blit(button_icon, icon_rect)
        self.toggle_mask_button_off_image = button_image

        button_image = button_surface.copy()
        button_image.fill(button_active_bg_color)
        button_image.blit(button_icon, icon_rect)
        self.toggle_mask_button_on_image = button_image

        # Toggle Poly Trace Button
        image = media_manager.get('icons/poly_icon.png', convert_alpha=True)
        icon_scale = 0.8
        button_icon = pygame.transform.scale(image, (self.button_size*icon_scale, self.button_size*icon_scale))
        icon_rect = button_icon.get_rect(center=(self.button_size/2, self.button_size/2))
        button_image = button_surface.copy()
        button_image.blit(button_icon, icon_rect)
        self.toggle_poly_trace_button_off_image = button_image

        button_image = button_surface.copy()
        button_image.fill(button_active_bg_color)
        button_image.blit(button_icon, icon_rect)
        self.toggle_poly_trace_button_on_image = button_image

        # Copy Poly Button
        scale = 0.55
        button_size = (self.button_size*scale, self.button_size*scale)
        button_image = button_surface.copy()
        # button_image.fill('white')
        button_image = pygame.transform.scale(button_image, button_size)
        small_button_rect = button_image.get_rect(bottomright=(self.button_size, self.button_size))
        
        image = media_manager.get('icons/copy_icon.png', convert_alpha=True)
        icon_scale = 0.9
        button_icon = pygame.transform.scale(image, (button_size[0]*icon_scale, button_size[1]*icon_scale))
        icon_rect = button_icon.get_rect(center=(button_size[0]/2, button_size[1]/2))
        button_image.blit(button_icon, icon_rect)

        main_button_image = self.toggle_poly_trace_button_off_image.copy()
        main_button_image.blit(button_image, small_button_rect)
        self.copy_poly_off_image = main_button_image

    def setup_toolbar(self):
        x = self.button_gap
        y = self.button_gap

        # Move Button
        position = (x,y)
        value = 1,
        on_hover = None
        on_press = self.on_move_button_press
        on_release = None
        self.move_button = Button(self.move_button_image, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(self.move_button)

        # Show Image Button
        x += self.button_size + self.button_gap
        position = (x, y)
        value = 1,
        on_hover = None
        on_press = self.on_toggle_image_button_press
        on_release = None
        image = self.toggle_image_button_on_image if self.show_image else self.toggle_image_button_off_image
        self.show_image_button = Button(image, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(self.show_image_button)

        # Set Image Alpha
        x += self.button_size + self.button_gap
        position = (x, y+2)
        value = 255
        on_submit = self.on_set_image_alpha_input_submit
        font_size = 12
        self.set_image_alpha_input = TextBox('', self.input_size, position, value, on_submit, font_size)
        self.inputs_group.add(self.set_image_alpha_input)

        # Show Mask Button
        x += self.input_size[0] + self.button_gap
        position = (x, y)
        value = 1,
        on_hover = None
        on_press = self.on_toggle_mask_button_press
        on_release = None
        image = self.toggle_mask_button_on_image if self.show_mask else self.toggle_mask_button_off_image
        self.show_mask_button = Button(image, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(self.show_mask_button)

        # Show Polys Button
        x += self.button_size + self.button_gap
        position = (x, y)
        value = 1,
        on_hover = None
        on_press = self.on_toggle_live_polys_button_press
        on_release = None
        image = self.toggle_poly_trace_button_on_image if self.show_live_polys else self.toggle_poly_trace_button_off_image
        self.show_live_polys_button = Button(image, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(self.show_live_polys_button)

        # Set Poly Points Every
        x += self.button_size + self.button_gap
        position = (x, y+2)
        value = ''
        on_submit = self.on_set_poly_points_input_submit
        font_size = 12
        self.set_poly_points_input = TextBox('', self.input_size, position, value, on_submit, font_size)
        self.inputs_group.add(self.set_poly_points_input)

        # Copy Polys Button
        x += self.input_size[0] + self.button_gap
        position = (x, y)
        value = 1,
        on_hover = None
        on_press = self.on_copy_poly_button_press
        on_release = None
        image = self.copy_poly_off_image
        self.copy_poly_button = Button(image, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(self.copy_poly_button)

        # Cut Shape Button
        x += self.button_size + self.button_gap
        position = (x, y)
        value = 1,
        on_hover = None
        on_press = self.on_cut_shape_button_press
        on_release = None
        image = self.cut_button_on_image if self.cut_shape else self.cut_button_off_image
        self.cut_shape_button = Button(image, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(self.cut_shape_button)

        # Physics Button
        x += self.button_size + self.button_gap
        position = (x, y)
        value = 1,
        on_hover = None
        on_press = self.on_toggle_show_physics_button_press
        on_release = None
        image = self.physics_button_on_image if self.show_physics else self.physics_button_off_image
        self.physics_button = Button(image, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(self.physics_button)

        # Save Button
        x += self.button_size + self.button_gap
        position = (x, y)
        value = 1,
        on_hover = None
        on_press = self.on_save_button_press
        on_release = None
        image = self.save_button_on_image if self.is_saved else self.save_button_off_image
        self.save_button = Button(image, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(self.save_button)

        # Trash Panel Button
        x += self.button_size + self.button_gap + self.trash_button_gap
        position = (x, y)
        value = 1,
        on_hover = None
        on_press = self.on_trash_button_press
        on_release = None
        image = self.trash_button_image
        self.trash_panel_button = Button(image, position, value, on_hover, on_press, on_release)
        self.buttons_group.add(self.trash_panel_button)

    def on_toggle_image_button_press(self, button: Button):
        self.show_image = not self.show_image
        button.image = self.toggle_image_button_on_image if self.show_image else self.toggle_image_button_off_image

    def on_toggle_mask_button_press(self, button: Button):
        self.show_mask = not self.show_mask
        button.image = self.toggle_mask_button_on_image if self.show_mask else self.toggle_mask_button_off_image

    def on_trash_button_press(self, button: Button):
        self.unlink_image_panel(kill_panel=True)

    def on_save_button_press(self, button: Button):
        self.linked_image_panel.save_to_file()
        self.toggle_save_button(True)

    def toggle_save_button(self, is_saved):
        self.is_saved = is_saved
        self.save_button.image = self.save_button_on_image if self.is_saved else self.save_button_off_image
        self.save_button

    def on_copy_poly_button_press(self, button: Button):
        self.copy_poly_points = True

    def on_cut_shape_button_press(self, button: Button):
        self.cut_shape = not self.cut_shape

        if self.cut_shape and self.show_live_polys: # Hacky
            self.on_toggle_live_polys_button_press(self.show_live_polys_button)

        button.image = self.cut_button_on_image if self.cut_shape else self.cut_button_off_image
        self.linked_image_panel.edit_cut_shapes = self.cut_shape

    def on_toggle_live_polys_button_press(self, button: Button):
        self.show_live_polys = not self.show_live_polys
        if self.show_live_polys and self.cut_shape: # Hacky
            self.on_cut_shape_button_press(self.cut_shape_button)

        button.image = self.toggle_poly_trace_button_on_image if self.show_live_polys else self.toggle_poly_trace_button_off_image

    def on_toggle_show_physics_button_press(self, button: Button):
        self.show_physics = not self.show_physics
        button.image = self.physics_button_on_image if self.show_physics else self.physics_button_off_image
        self.linked_image_panel.show_physics = self.show_physics

    def on_set_poly_points_input_submit(self, textbox: TextBox):
        point_every = int(textbox.value)
        if point_every != self.linked_image_panel.live_poly_points_every:
            self.linked_image_panel.update_poly_points_every(point_every)
            self.toggle_save_button(False)

    def on_set_image_alpha_input_submit(self, textbox: TextBox):
        self.linked_image_panel.image_alpha = int(textbox.value)
        self.linked_image_panel.redraw_sprite_image()

    def on_move_button_press(self, button: Button):
        # print('on_move_button_press', self.follow_mouse)
        if self.move_by_mouse:
            self.move_by_mouse = False
            self.move_initial_position = None
            return
        
        self.move_by_mouse = True
        self.move_initial_position = self.mouse_position
        # self.move_initial_position_offset = (self.mouse_position.x - self.linked_image_panel.rect.left, self.mouse_position.y - self.linked_image_panel.rect.top)
        # self.move_offset = (self.linked_image_panel.rect.left)
        
        # x = self.linked_image_panel.position[0] - self.rect.left
        # y = self.linked_image_panel.position[1] - self.rect.top
        # self.move_offset = (x, y)

    def on_event(self, parent_mouse_position, event):
        self.has_killed_panel = False
        self.is_hovered = False
        self.button_is_hovered = False
        self.input_is_hovered = False
        
        if not self.linked_image_panel:
            return
        
        self.parent_mouse_position = parent_mouse_position

        if self.parent_mouse_position:
            mouse_x, mouse_y = self.parent_mouse_position
            self.mouse_position = pygame.Vector2(mouse_x - self.rect.left, mouse_y - self.rect.top)
            
        for input in self.inputs_group:
            input: TextBox
            input.on_event(self.mouse_position, event)
            if input.is_hovered: 
                self.input_is_hovered = True

        button_pressed = None
        if not self.move_by_mouse:
            for button in self.buttons_group:
                button: Button
                button.on_event(self.mouse_position, event)
                if button.is_hovered:
                    self.button_is_hovered = True
                
                if button.is_pressed:
                    button_pressed = button

        self.is_hovered = self.button_is_hovered or self.input_is_hovered

        if not button_pressed and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.move_by_mouse:
                self.move_by_mouse = False
                self.move_initial_position = None
                self.stick_to_top_of_image_panel()
            # else:
            #     self.move_by_mouse = True
            #     self.move_initial_position = self.mouse_position

    def move_by(self, offset):
        position = (self.rect.left + offset[0], self.rect.bottom + offset[1])
        self.rect.bottomleft = position

    def move_linked_image_panel(self):
        offset = self.mouse_position - self.move_initial_position
        if offset.x != 0 or offset.y != 0:
            self.move_initial_position = self.mouse_position
            self.linked_image_panel.move_by(offset)
            # self.move_by(offset)
            # self.stick_to_top_of_image_panel()

    def update(self, *args, **kwargs):
        self.buttons_group.update()
        self.inputs_group.update(self.mouse_position)

        for input in self.inputs_group:
            input: TextBox
            if input.is_hovered:
                self.mouse_cursor = pygame.SYSTEM_CURSOR_IBEAM
                break

        if self.button_is_hovered:
            self.mouse_cursor = pygame.SYSTEM_CURSOR_HAND
        elif self.input_is_hovered:
            self.mouse_cursor = pygame.SYSTEM_CURSOR_IBEAM
        else:
            self.mouse_cursor = pygame.SYSTEM_CURSOR_ARROW

        if self.linked_image_panel:
            self.toggle_save_button(self.linked_image_panel.is_saved)
                
            if self.move_by_mouse and self.mouse_position != self.move_initial_position:
                self.move_linked_image_panel()

            self.linked_image_panel.show_image = self.show_image
            self.linked_image_panel.show_mask = self.show_mask
            self.linked_image_panel.show_live_polys = self.show_live_polys
        
        return super().update(*args, **kwargs)
    
    def stick_to_top_of_image_panel(self):
        if not self.linked_image_panel:
            return
        
        x = self.linked_image_panel.parent_rect.left + self.linked_image_panel.rect.left
        y = self.linked_image_panel.parent_rect.top + self.linked_image_panel.rect.top
        position = (x, y)
        self.rect.bottomleft = position

    def update_buttons(self):
        self.show_image_button.image = self.toggle_image_button_on_image if self.show_image else self.toggle_image_button_off_image
        self.show_mask_button.image = self.toggle_mask_button_on_image if self.show_mask else self.toggle_mask_button_off_image
        self.show_live_polys_button.image = self.toggle_poly_trace_button_on_image if self.show_live_polys else self.toggle_poly_trace_button_off_image
        self.cut_shape_button.image = self.cut_button_on_image if self.cut_shape else self.cut_button_off_image

    def unlink_image_panel(self, kill_panel=False):
        self.show_image = False
        self.show_mask = False
        self.show_live_polys = False
        self.button_is_hovered = False
        self.input_is_hovered = False
        self.copy_poly_points = False
        self.has_killed_panel = False
        self.cut_shape = False
        self.update_buttons()
        
        if self.linked_image_panel:
            if not kill_panel:
                self.linked_image_panel.deactivate()
                self.linked_image_panel.redraw_housing_box()
            else:
                self.linked_image_panel.kill()
                self.has_killed_panel = True

        self.linked_image_panel = None

    def link_to_image_panel(self, image_panel: ImagePanel):
        self.show_image = image_panel.show_image
        self.show_mask = image_panel.show_mask
        self.show_live_polys = image_panel.show_live_polys
        self.set_image_alpha_input.value = str(image_panel.image_alpha)
        self.set_poly_points_input.value = str(image_panel.live_poly_points_every)
        self.update_buttons()

        image_panel.is_active = True
        image_panel.redraw_housing_box()
        self.linked_image_panel = image_panel
        self.stick_to_top_of_image_panel()

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))

        if self.linked_image_panel:
            if self.move_by_mouse:
                self.surface.set_alpha(80)
            else:
                self.surface.set_alpha(255)

            self.surface.blit(self.housing_image, (0,0))
            self.buttons_group.draw(self.surface)

            for input in self.inputs_group:
                input: TextBox
                input.draw(self.surface)

        
        surface.blit(self.surface, self.rect)
