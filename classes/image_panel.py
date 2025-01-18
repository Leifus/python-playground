from classes.common.game_sprite import GameSprite
from classes.common.helper_methods import aspect_scale
from classes.physical_shape_output import PhysicalShapeOutput
from config import pygame, pymunk, json, os

class ImagePanel(GameSprite):
    def __init__(self, identifier, position, orig_image: pygame.Surface, max_sprite_loading_size):
        super(ImagePanel, self).__init__()

        self.identifier = identifier
        self.position = position
        self.orig_image = orig_image
        self.orig_mask: pygame.Mask = None
        self.mask_setcolor = pygame.Color('black')
        self.show_image = True
        self.image_alpha = 255
        self.show_mask = False
        self.housing_box_spacing = 25
        self.sprite_image: pygame.Surface = None
        self.sprite_mask_image: pygame.Surface = None
        self.housing_box_image: pygame.Surface = None
        self.mask_alpha = 255
        self.pixel_length_per_poly_point = 15
        self.sprite_rect: pygame.Rect = None
        self.sprite_mask: pygame.Mask = None
        self.mouse_position = None
        self.show_poly_points = False
        self.show_poly_point_numbers = False
        self.poly_points = []
        self.poly_point_radius = 3
        self.poly_line_width = 2
        self.draw_scale = 1.0
        self.housing_border_color = pygame.Color('gray80')
        self.housing_border_width = 2
        self.housing_border_color_active = pygame.Color('gray60')
        self.housing_border_width_active = 3
        self.is_hovered = False
        self.is_active = False
        self.parent_rect: pygame.Rect = None
        self.hovered_poly_point = None
        self.active_poly_point = None
        self.move_active_poly_point = False
        self.edit_cut_shapes = False
        self.relative_mouse_position = None
        self.cut_points = []
        self.start_cut_poly_point_idx = None
        self.end_cut_poly_point_idx = None
        self.show_physical_body = False
        self.physical_shapes = []
        self.panel_copy_count = 0
        self.move_panel = False
        self.is_locked = False
        self.flip_x = False
        self.flip_y = False


        self.space = pymunk.Space()
        self.body: pymunk.Body = None

        # Make initial calculations for image size and housing box
        self.orig_image_rect = self.orig_image.get_rect()
        if self.orig_image_rect.width > max_sprite_loading_size[0] or self.orig_image_rect.height > max_sprite_loading_size[1]:
            scaled_image = aspect_scale(orig_image, max_sprite_loading_size)
            self.image_size = scaled_image.get_size()
        else:
            self.image_size = self.orig_image_rect.size

        # Adjust Parent surface to fit scaled image
        self.size = (self.image_size[0]+self.housing_box_spacing*2, self.image_size[1]+self.housing_box_spacing*2)
        
        self.redraw()
        self.create_new_poly_points(self.pixel_length_per_poly_point)
        self.construct_physical_body()

    def move_by(self, offset):
        self.position = (self.position[0] + offset[0], self.position[1] + offset[1])
        self.rect.center = self.position
        self.construct_physical_body()

    def move_panel_with_mouse(self):
        if self.is_locked:
            return
        
        offset = self.mouse_position - self.move_initial_position
        if offset.x != 0 or offset.y != 0:
            self.move_initial_position = self.mouse_position
            self.move_by(offset)

    def deactivate(self):
        self.is_active = False
        self.active_poly_point = None
        self.move_active_poly_point = False
        self.move_initial_position = None
        self.start_cut_poly_point_idx = None
        self.end_cut_poly_point_idx = None

    def construct_physical_body(self):
        if self.space.bodies:
            self.space.remove(self.body, *self.body.shapes)
            
        if len(self.poly_points) == 0:
            return

        body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.DYNAMIC)
        body.position = self.position
        
        shape_count = len(self.cut_points)+1
        shape_point_sets = []
        
        shape_start_idx = 0
        for shape_iter in range(shape_count):
            current_idx = shape_start_idx
            point_set = []
            cut_at_point_idx = None
            # print(f'shape {shape_iter}:', shape_start_idx)
            while current_idx < len(self.poly_points):
                point_set.append(self.poly_points[current_idx])

                cut_point = None
                if len(point_set) > 0:
                    # Check for any cut points
                    for cut in self.cut_points:
                        if current_idx in [*cut]:
                            cut_point = cut
                            break
                
                if cut_point and current_idx != shape_start_idx:
                    if current_idx == cut_point[0]:
                        if cut_at_point_idx is None and cut_point[1] != shape_start_idx:
                            cut_at_point_idx = current_idx
                            current_idx = cut_point[1]
                        elif cut_point[1] == shape_start_idx:
                            break
                        else:
                            current_idx += 1
                    elif current_idx == cut_point[1]:
                        if cut_at_point_idx is None and cut_point[0] != shape_start_idx:
                            cut_at_point_idx = current_idx
                            current_idx = cut_point[0]
                        elif cut_point[0] == shape_start_idx:
                            break
                        else:
                            current_idx += 1
                    else:
                        current_idx += 1
                else:
                    current_idx += 1

            if cut_at_point_idx:
                shape_start_idx = cut_at_point_idx

            shape_point_sets.append(point_set)
        
        shape_colors = ["cadetblue3", "chartreuse3", "coral", "darkolivegreen3", "darksalmon"]
        shape_color_idx = 0
        shapes = []
        self.physical_shapes = []
        for shape_iter, points in enumerate(shape_point_sets):
            positioned_points = []
            for point in points:
                scaled_point = (point[0] * self.draw_scale, point[1] * self.draw_scale)

                offset_x = -self.sprite_rect.width/2
                offset_y = -self.sprite_rect.height/2
                positioned_point = (offset_x + scaled_point[0], offset_y + scaled_point[1])
                positioned_points.append(positioned_point)

            physical_shape_output = PhysicalShapeOutput(f'Shape {shape_iter}', positioned_points)
            self.physical_shapes.append(physical_shape_output)
            shape = pymunk.Poly(body, positioned_points)
            shape.mass = 10
            color = pygame.Color(shape_colors[shape_color_idx])
            shape.color = color
            shapes.append(shape)
            shape_color_idx += 1
            if shape_color_idx >= len(shape_colors):
                shape_color_idx = 0

        self.body = body
        self.space.add(self.body, *shapes)
        self.is_saved = False
    
    def redraw_mask_image(self):
        self.sprite_mask_image = self.sprite_mask.to_surface(setcolor=self.mask_setcolor, unsetcolor=None)
        self.sprite_mask_image.set_alpha(self.mask_alpha)

    def redraw_sprite_image(self, orig_image):
        self.sprite_image = aspect_scale(orig_image, self.image_size)
        self.sprite_rect = self.sprite_image.get_rect()
        self.sprite_mask = pygame.mask.from_surface(self.sprite_image)
        self.sprite_image.set_alpha(self.image_alpha)
        self.sprite_rect.center = (self.rect.width/2, self.rect.height/2)

    def redraw_housing_box(self):
        color = self.housing_border_color_active if self.is_active else self.housing_border_color
        border = self.housing_border_width_active if self.is_active else self.housing_border_width
        
        self.housing_box_image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(self.housing_box_image, color, (0,0,self.size[0], self.size[1]), border)

    def redraw(self):
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)

        orig_image = self.orig_image
        if self.flip_x or self.flip_y:
            orig_image = pygame.transform.flip(orig_image, flip_x=self.flip_x, flip_y=self.flip_y)

        self.orig_mask = pygame.mask.from_surface(orig_image)

        self.redraw_sprite_image(orig_image)
        self.redraw_mask_image()
        self.redraw_housing_box()

    def create_new_poly_points(self, pixel_length_per_poly_point):
        self.pixel_length_per_poly_point = pixel_length_per_poly_point

        #Ensure to use the original size for poly construction.
        self.poly_points = self.orig_mask.outline(self.pixel_length_per_poly_point)
        self.construct_physical_body()

    def flip(self, flip_x: bool, flip_y: bool):
        self.hovered_poly_point = None
        self.active_poly_point = None

        if len(self.poly_points) > 0:
            flipped_points = []
            for point in self.poly_points:
                x, y = point

                if flip_x:
                    x = self.sprite_rect.width - x
                if flip_y:
                    y = self.sprite_rect.height - y

                flipped_points.append((x, y))

            self.poly_points = flipped_points

        if flip_x:
            self.flip_x = not self.flip_x
        if flip_y:
            self.flip_y = not self.flip_y

        self.redraw()
        # self.construct_physical_body()

    def finish_shape_cutting(self):
        if self.end_cut_poly_point_idx:
            self.cut_points.append((self.start_cut_poly_point_idx, self.end_cut_poly_point_idx))
            
        self.start_cut_poly_point_idx = None
        self.end_cut_poly_point_idx = None

        self.construct_physical_body()

    def stop_moving_poly_point(self):
        self.move_active_poly_point = False
        self.move_initial_position = None
        self.is_saved = False
        if self.active_poly_point and self.hovered_poly_point is not self.active_poly_point:
            self.active_poly_point = None
        self.construct_physical_body()

    def on_event(self, mouse_position: pygame.Vector2, event: pygame.event.Event):
        self.mouse_position = mouse_position
        if mouse_position:
            mouse_x, mouse_y = mouse_position
            self.relative_mouse_position = pygame.Vector2(mouse_x - self.rect.left, mouse_y - self.rect.top)
            
        self.is_hovered = False
        self.hovered_poly_point = None

        if self.mouse_position:
            is_in_x = mouse_position.x >= self.rect.left and mouse_position.x <= self.rect.right
            is_in_y = mouse_position.y >= self.rect.top and mouse_position.y <= self.rect.bottom
            self.is_hovered = is_in_x and is_in_y

        if not self.is_active:
            return
        
        hovered_point_index = None
        if self.is_hovered:
            if self.show_poly_points or self.edit_cut_shapes:
                # check if hovering over a poly point.
                relative_mouse_pos = (self.mouse_position[0] - self.sprite_rect.left - self.rect.left, self.mouse_position[1] - self.sprite_rect.top - self.rect.top)
                bleed = 10
                
                for i, point in enumerate(self.poly_points):
                    scaled_point = (point[0] * self.draw_scale, point[1] * self.draw_scale)
                    is_within_point_x = relative_mouse_pos[0] >= scaled_point[0] - bleed and relative_mouse_pos[0] <= scaled_point[0] + bleed
                    is_within_point_y = relative_mouse_pos[1] >= scaled_point[1] - bleed and relative_mouse_pos[1] <= scaled_point[1] + bleed
                    is_point_hovered = is_within_point_x and is_within_point_y
                    if is_point_hovered:
                        self.hovered_poly_point = point
                        hovered_point_index = i
                        break

        if event.type == pygame.MOUSEBUTTONUP:
            self.move_panel = False
            if self.move_active_poly_point:
                self.stop_moving_poly_point()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.edit_cut_shapes:
                if not self.start_cut_poly_point_idx:
                    self.start_cut_poly_point_idx = hovered_point_index
                else:
                    self.end_cut_poly_point_idx = hovered_point_index
                    self.finish_shape_cutting()
            elif not self.move_active_poly_point and self.hovered_poly_point:
                self.active_poly_point = self.hovered_poly_point
                self.move_active_poly_point = True
                self.move_initial_position = self.mouse_position
            elif self.is_hovered: # Move panel
                self.move_panel = True
                self.move_initial_position = self.mouse_position
        
                
        if event.type == pygame.KEYDOWN:
            if self.active_poly_point:
                if event.key in [pygame.K_d, pygame.K_BACKSPACE, pygame.K_DELETE] and len(self.poly_points) > 3:
                    # Delete poly point: Badly
                    new_points = []
                    for point in self.poly_points:
                        if point is not self.active_poly_point:
                            new_points.append(point)
                    
                    self.active_poly_point = None
                    self.poly_points = new_points

    def zoom_at_scale(self, scale):
        self.draw_scale += scale
        self.image_size = (int(self.orig_image_rect.width * self.draw_scale), int(self.orig_image_rect.height * self.draw_scale))
        self.size = (self.image_size[0]+(self.housing_box_spacing*2), self.image_size[1]+(self.housing_box_spacing*2))

        self.redraw()
        self.construct_physical_body()

    def save_to_file(self):
        physical_shapes = []
        for shape in self.physical_shapes:
            shape: PhysicalShapeOutput
            physical_shapes.append({
                'label': shape.label,
                'points': shape.points
            })

        data = {
            'dimensions': self.sprite_rect.size,
            'poly_points': self.poly_points,
            'physical_shapes': physical_shapes
        }

        json_string = json.dumps(data, indent=2)
        folder = f'{os.getcwd()}/outputs'
        try:
            with open(f"{folder}/output_{self.identifier}.txt", 'w') as filehandle:
                filehandle.write(json_string)

            self.is_saved = True
        except:
            print(f"Error occurred while writing to file.")

    def update_poly_point(self, existing_point, new_point):
        idx = -1
        for i, point in enumerate(self.poly_points):
            if point is not existing_point:
                continue
            else:
                idx = i
                break
        
        if idx != -1:
            self.poly_points[idx] = new_point

    def update(self, *args, **kwargs):
        if not self.is_active:
            return super().update(*args, **kwargs)
        
        if self.move_panel:
            self.move_panel_with_mouse()

        if self.body:
            self.body.position = self.position

        if self.move_active_poly_point:
            offset = (self.mouse_position.x - self.move_initial_position[0], self.mouse_position.y - self.move_initial_position[1])
            scaled_back_offset = (offset[0] * (1.0/self.draw_scale), offset[1] * (1.0/self.draw_scale))
            if scaled_back_offset[0] != 0 or scaled_back_offset[1] != 0:
                self.has_moved_a_point = True
                new_point = (round(self.active_poly_point[0] + scaled_back_offset[0],3), round(self.active_poly_point[1] + scaled_back_offset[1],3))
                self.update_poly_point(self.active_poly_point, new_point)
                self.active_poly_point = new_point
                self.move_initial_position = self.mouse_position

        return super().update(*args, **kwargs)
    
    def draw_image_info(self):
        orig_size = self.orig_image_rect.size
        current_size = self.sprite_rect.size
        
        font_size = 12
        font_color = pygame.Color('black')
        font_bg = pygame.Color('gray90')
        font = pygame.font.Font('freesansbold.ttf', font_size)

        text = f'{current_size[0]} x {current_size[1]}  (orig: {orig_size[0]} x {orig_size[1]}) -- {self.identifier}'
        text_surface = font.render(text, True, font_color, font_bg)
        text_rect = text_surface.get_rect()
        # text_surface.set_alpha(170)
        self.surface.blit(text_surface, (5, 5))

    def draw_poly_shape(self):
        if len(self.poly_points) < 2:
            return

        poly_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        if self.edit_cut_shapes:
            poly_surface.set_alpha(100)
            line_color = pygame.Color('darkgreen')
            point_color = pygame.Color('darkgreen')
        else:
            line_color = pygame.Color('red')
            point_color = pygame.Color('blue')
        
        point_radius = self.poly_point_radius
        line_width = self.poly_line_width
        scaled_and_positioned_poly_points = []
        for point in self.poly_points:
            scaled_point = (point[0] * self.draw_scale, point[1] * self.draw_scale)
            x = self.sprite_rect.left + scaled_point[0]
            y = self.sprite_rect.top + scaled_point[1]
            positioned_point = (x, y)
            scaled_and_positioned_poly_points.append(positioned_point)

        pygame.draw.polygon(poly_surface, line_color, scaled_and_positioned_poly_points, line_width)
        
        # Points
        font_size = 11
        font_color = pygame.Color('black')
        font_bg = pygame.Color('lightcyan')
        font = pygame.font.Font('freesansbold.ttf', font_size)
        for idx, point in enumerate(self.poly_points):
            scaled_point = (point[0] * self.draw_scale, point[1] * self.draw_scale)
            x = self.sprite_rect.left + scaled_point[0]
            y = self.sprite_rect.top + scaled_point[1]
            positioned_point = (x, y)
            dot_point = (positioned_point[0] + point_radius/2, positioned_point[1] + point_radius/2)
            pygame.draw.circle(poly_surface, point_color, dot_point, point_radius)
            if self.show_poly_point_numbers:
                label = font.render(str(idx), True, font_color, font_bg)
                poly_surface.blit(label, (dot_point[0]+2, dot_point[1]+2))

        self.surface.blit(poly_surface, (0,0))

    def draw_focused_poly_points(self):
        if not self.show_poly_points:
            return
        
        focused_points = []
        if self.active_poly_point:
            focused_points.append(self.active_poly_point)
        if self.hovered_poly_point and self.hovered_poly_point is not self.active_poly_point:
            focused_points.append(self.hovered_poly_point)

        font_size = 11
        font_color = pygame.Color('black')
        font_bg = pygame.Color('gold')
        font = pygame.font.Font('freesansbold.ttf', font_size)
        
        for point in focused_points:
            scaled_point = (point[0] * self.draw_scale, point[1] * self.draw_scale)
            x = self.sprite_rect.left + scaled_point[0]
            y = self.sprite_rect.top + scaled_point[1]
            positioned_point = (x, y)

            point_label = f'{int(point[0]),int(point[1])}'
            point_label_surface = font.render(point_label, True, font_color, font_bg)
            point_label_rect = point_label_surface.get_rect()
            offset = (0, -5-point_label_rect.height)
            point_label_rect.center = (positioned_point[0] + offset[0], positioned_point[1] + offset[1])

            self.surface.blit(point_label_surface, point_label_rect)

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))
        
        # Image
        if self.show_image:
            self.surface.blit(self.sprite_image, self.sprite_rect)

        # Mask
        if self.show_mask and self.sprite_mask_image:
            self.surface.blit(self.sprite_mask_image, self.sprite_rect)

        # Poly Shape
        if self.show_poly_points or self.edit_cut_shapes:
            self.draw_poly_shape()

        if self.is_hovered or self.is_active:
            # Housing Box
            self.surface.blit(self.housing_box_image, (0,0))

            self.draw_focused_poly_points()


            # Hovered Poly Point
            if self.hovered_poly_point:
                point = self.hovered_poly_point
                scaled_point = (point[0] * self.draw_scale, point[1] * self.draw_scale)

                if self.edit_cut_shapes or (point is not self.active_poly_point and not self.move_active_poly_point):
                    color = pygame.Color('gray50')
                    position = (self.sprite_rect.left + scaled_point[0] + self.poly_point_radius/2, self.sprite_rect.top + scaled_point[1] + self.poly_point_radius/2)
                    pygame.draw.circle(self.surface, color, position, self.poly_point_radius*2, 2)
            
            if self.is_active:
                if self.active_poly_point and self.show_poly_points:
                    scaled_point = (self.active_poly_point[0] * self.draw_scale, self.active_poly_point[1] * self.draw_scale)

                    color = pygame.Color('black')
                    position = (self.sprite_rect.left + scaled_point[0] + self.poly_point_radius/2, self.sprite_rect.top + scaled_point[1] + self.poly_point_radius/2)
                    pygame.draw.circle(self.surface, color, position, self.poly_point_radius*2, 2)
                
                if self.edit_cut_shapes:
                    if self.start_cut_poly_point_idx:
                        point = self.poly_points[self.start_cut_poly_point_idx]
                        color = pygame.Color('darkgreen')
                        position = (self.sprite_rect.left + point[0] + self.poly_point_radius/2, self.sprite_rect.top + point[1] + self.poly_point_radius/2)
                        pygame.draw.circle(self.surface, color, position, self.poly_point_radius*2, 2)
                        pygame.draw.line(self.surface, 'darkgreen', position, self.relative_mouse_position, 2)

                    color = pygame.Color('black')

                    for cut in self.cut_points:
                        start_point = self.poly_points[cut[0]]
                        end_point = self.poly_points[cut[1]]
                        start_pos = (self.sprite_rect.left + start_point[0] + self.poly_point_radius/2, self.sprite_rect.top + start_point[1] + self.poly_point_radius/2)
                        pygame.draw.circle(self.surface, color, start_pos, self.poly_point_radius*2, 2)

                        end_pos = (self.sprite_rect.left + end_point[0] + self.poly_point_radius/2, self.sprite_rect.top + end_point[1] + self.poly_point_radius/2)
                        pygame.draw.circle(self.surface, color, end_pos, self.poly_point_radius*2, 2)

                        pygame.draw.line(self.surface, 'darkgreen', start_pos, end_pos, 2)

            # Image Dimensions
            self.draw_image_info()
            
        if self.show_physical_body:
            space_draw_options = pymunk.pygame_util.DrawOptions(surface)
            self.space.debug_draw(space_draw_options)

        surface.blit(self.surface, self.rect)