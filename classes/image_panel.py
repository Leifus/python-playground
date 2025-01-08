from pygame import Vector2
from classes.common.game_sprite import GameSprite
from classes.common.helper_methods import aspect_scale
from config import pygame, pymunk

class ImagePanel(GameSprite):
    def __init__(self, position, orig_image: pygame.Surface, max_sprite_loading_size):
        super(ImagePanel, self).__init__()

        self.position = position
        self.orig_image = orig_image
        self.mask_setcolor = pygame.Color('black')
        self.show_image = True
        self.image_alpha = 160
        self.show_mask = False
        self.housing_box_spacing = 25
        self.sprite_image: pygame.Surface = None
        self.sprite_mask_image: pygame.Surface = None
        self.housing_box_image: pygame.Surface = None
        self.mask_alpha = 160
        self.live_poly_points_every = 15
        self.sprite_rect: pygame.Rect = None
        self.sprite_mask: pygame.Mask = None
        self.mouse_position = None
        self.show_live_polys = False
        self.live_poly_points = []
        self.poly_points = []
        self.poly_point_radius = 3
        self.poly_line_width = 2
        # self.draw_scale = 1.0
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
        self.show_physics = False

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
        self.construct_physical_body()

    def move_by(self, offset):
        self.position = (self.position[0] + offset[0], self.position[1] + offset[1])
        self.rect.center = self.position

    def deactivate(self):
        self.is_active = False
        self.active_poly_point = None
        self.move_active_poly_point = False
        self.move_active_poly_point_initial_position = None
        self.start_cut_poly_point_idx = None
        self.end_cut_poly_point_idx = None

    def construct_physical_body(self):
        if self.space.bodies:
            self.space.remove(self.body, *self.body.shapes)
            
        body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.DYNAMIC)
        body.position = self.position
        
        poly_points = self.poly_points if len(self.poly_points) > 0 else self.live_poly_points
        
        shape_count = len(self.cut_points)+1
        shape_point_sets = []
        
        shape_start_idx = 0
        for shape_iter in range(shape_count):
            current_idx = shape_start_idx
            point_set = []
            cut_at_point_idx = None
            # print(f'shape {shape_iter}:', shape_start_idx)
            while current_idx < len(poly_points):
                point_set.append(poly_points[current_idx])

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
                            hey = 1
                            break
                        else:
                            current_idx += 1
                    elif current_idx == cut_point[1]:
                        if cut_at_point_idx is None and cut_point[0] != shape_start_idx:
                            cut_at_point_idx = current_idx
                            current_idx = cut_point[0]
                        elif cut_point[0] == shape_start_idx:
                            hey = 1
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
        for i, points in enumerate(shape_point_sets):
            positioned_points = []
            for point in points:
                offset_x = -self.sprite_rect.width/2
                offset_y = -self.sprite_rect.height/2
                positioned_point = (offset_x + point[0], offset_y + point[1])
                positioned_points.append(positioned_point)

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
    
    def redraw_mask_image(self):
        self.sprite_mask_image = self.sprite_mask.to_surface(setcolor=self.mask_setcolor, unsetcolor=None)
        self.sprite_mask_image.set_alpha(self.mask_alpha)

    def redraw_sprite_image(self):
        # Setup Main Image
        self.sprite_image = aspect_scale(self.orig_image, self.image_size)
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

        self.redraw_sprite_image()
        self.redraw_mask_image()
        self.redraw_housing_box()

        # Guess the initial poly points
        biggest_side = self.image_size[0] if self.image_size[0] > self.image_size[1] else self.image_size[1]
        min_points = 3
        max_points = 20
        log = (biggest_side / max_points / min_points)
        self.live_poly_points_every = int(biggest_side / log)
        self.live_poly_points = self.sprite_mask.outline(self.live_poly_points_every)

    def update_poly_points_every(self, point_every):
        self.live_poly_points_every = point_every
        self.live_poly_points = self.sprite_mask.outline(self.live_poly_points_every)

    def finish_shape_cutting(self):
        if self.end_cut_poly_point_idx:
            self.cut_points.append((self.start_cut_poly_point_idx, self.end_cut_poly_point_idx))
            
        self.start_cut_poly_point_idx = None
        self.end_cut_poly_point_idx = None

        self.construct_physical_body()

    def stop_moving_poly_point(self):
        self.move_active_poly_point = False
        self.move_active_poly_point_initial_position = None
        if self.active_poly_point and self.hovered_poly_point is not self.active_poly_point:
            self.active_poly_point = None
        self.construct_physical_body()

    def on_event(self, mouse_position: Vector2, event: pygame.event.Event):
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
            if self.show_live_polys or self.edit_cut_shapes:
                # check if hovering over a poly point.
                relative_mouse_pos = (self.mouse_position[0] - self.sprite_rect.left - self.rect.left, self.mouse_position[1] - self.sprite_rect.top - self.rect.top)
                bleed = 10
                
                points = self.live_poly_points if len(self.poly_points) == 0 else self.poly_points
                for i, point in enumerate(points):
                    is_within_point_x = relative_mouse_pos[0] >= point[0] - bleed and relative_mouse_pos[0] <= point[0] + bleed
                    is_within_point_y = relative_mouse_pos[1] >= point[1] - bleed and relative_mouse_pos[1] <= point[1] + bleed
                    is_point_hovered = is_within_point_x and is_within_point_y
                    if is_point_hovered:
                        self.hovered_poly_point = point
                        hovered_point_index = i
                        break

        if event.type == pygame.MOUSEBUTTONUP:
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
                self.move_active_poly_point_initial_position = self.mouse_position
        
                
        if event.type == pygame.KEYDOWN:
            if self.active_poly_point:
                if event.key in [pygame.K_d, pygame.K_BACKSPACE, pygame.K_DELETE] and len(self.live_poly_points) > 3:
                    # Delete poly point: Badly
                    new_points = []
                    for point in self.live_poly_points:
                        if point is not self.active_poly_point:
                            new_points.append(point)
                    
                    self.active_poly_point = None
                    self.live_poly_points = new_points

    def copy_live_poly(self):
        self.poly_points = self.live_poly_points

    def zoom_at_scale(self, scale):
        # self.draw_scale = 1.0 * scale
        self.image_size = (int(self.image_size[0] * scale), int(self.image_size[1] * scale))
        self.size = (self.image_size[0]+(self.housing_box_spacing*2), self.image_size[1]+(self.housing_box_spacing*2))
        scaled_poly_points = []
        if len(self.poly_points) > 0:
            for point in self.poly_points:
                scaled = (point[0] * scale, point[1] * scale)
                scaled_poly_points.append(scaled)
            
            self.poly_points = scaled_poly_points

        self.redraw()

    def update_poly_point(self, existing_point, new_point):
        idx = -1
        use_baked_poly_points = len(self.poly_points) > 0
        points = self.live_poly_points if not use_baked_poly_points else self.poly_points
        for i, point in enumerate(points):
            if point is not existing_point:
                continue
            else:
                idx = i
                break
        
        if idx != -1:
            if use_baked_poly_points:
                self.poly_points[idx] = new_point
            else:
                self.live_poly_points[idx] = new_point

    def update(self, *args, **kwargs):
        if not self.is_active:
            return super().update(*args, **kwargs)

        self.body.position = self.position

        if self.move_active_poly_point:
            offset = (self.mouse_position.x - self.move_active_poly_point_initial_position[0], self.mouse_position.y - self.move_active_poly_point_initial_position[1])
            if offset[0] != 0 or offset[1] != 0:
                new_point = (self.active_poly_point[0] + offset[0], self.active_poly_point[1] + offset[1])
                self.update_poly_point(self.active_poly_point, new_point)
                self.active_poly_point = new_point
                self.move_active_poly_point_initial_position = self.mouse_position

        # print('polys', self.live_poly_points)

        return super().update(*args, **kwargs)
    
    def draw_image_dimensions(self):
        orig_size = self.orig_image_rect.size
        current_size = self.sprite_rect.size
        
        font_size = 12
        font_color = pygame.Color('black')
        font_bg = pygame.Color('gray90')
        font = pygame.font.Font('freesansbold.ttf', font_size)

        text = f'{current_size[0]} x {current_size[1]}  (orig: {orig_size[0]} x {orig_size[1]})'
        text_surface = font.render(text, True, font_color, font_bg)
        text_rect = text_surface.get_rect()
        # text_surface.set_alpha(170)
        self.surface.blit(text_surface, (5, 5))

    def draw_live_poly(self):   
        points = self.live_poly_points if len(self.poly_points) == 0 else self.poly_points

        if len(points) < 2:
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
        
        pygame.draw.polygon(poly_surface, line_color, points, line_width)
        font_size = 12
        font_color = pygame.Color('black')
        font_bg = pygame.Color('gold')
        font = pygame.font.Font('freesansbold.ttf', font_size)
        for idx, point in enumerate(points):
            label = font.render(str(idx), True, font_color, font_bg)
            dot_point = (point[0] + point_radius/2, point[1] + point_radius/2)
            pygame.draw.circle(poly_surface, point_color, dot_point, point_radius)
            poly_surface.blit(label, dot_point)

        rect = poly_surface.get_rect(topleft=(self.sprite_rect.left, self.sprite_rect.top))
        self.surface.blit(poly_surface, rect)

    def draw(self, surface: pygame.Surface):
        self.surface.fill((0,0,0,0))
        
        # Image
        if self.show_image:
            self.surface.blit(self.sprite_image, self.sprite_rect)

        # Mask
        if self.show_mask and self.sprite_mask_image:
            self.surface.blit(self.sprite_mask_image, self.sprite_rect)

        # Live Poly
        if self.show_live_polys or self.edit_cut_shapes:
            self.draw_live_poly()

        if self.is_hovered or self.is_active:
            # Housing Box
            self.surface.blit(self.housing_box_image, (0,0))

            # Hovered Poly Point
            if self.hovered_poly_point and (self.edit_cut_shapes or self.hovered_poly_point is not self.active_poly_point):
                color = pygame.Color('gray50')
                position = (self.sprite_rect.left + self.hovered_poly_point[0] + self.poly_point_radius/2, self.sprite_rect.top + self.hovered_poly_point[1] + self.poly_point_radius/2)
                pygame.draw.circle(self.surface, color, position, self.poly_point_radius*2, 2)
            
            if self.is_active:
                if self.active_poly_point and self.show_live_polys:
                    color = pygame.Color('blue')
                    position = (self.sprite_rect.left + self.active_poly_point[0] + self.poly_point_radius/2, self.sprite_rect.top + self.active_poly_point[1] + self.poly_point_radius/2)
                    pygame.draw.circle(self.surface, color, position, self.poly_point_radius*2, 2)
                
                if self.edit_cut_shapes:
                    points = self.poly_points if len(self.poly_points) > 0 else self.live_poly_points
                    if self.start_cut_poly_point_idx:
                        point = points[self.start_cut_poly_point_idx]
                        color = pygame.Color('darkgreen')
                        position = (self.sprite_rect.left + point[0] + self.poly_point_radius/2, self.sprite_rect.top + point[1] + self.poly_point_radius/2)
                        pygame.draw.circle(self.surface, color, position, self.poly_point_radius*2, 2)
                        pygame.draw.line(self.surface, 'darkgreen', position, self.relative_mouse_position, 2)

                    color = pygame.Color('black')

                    for cut in self.cut_points:
                        start_point = points[cut[0]]
                        end_point = points[cut[1]]
                        start_pos = (self.sprite_rect.left + start_point[0] + self.poly_point_radius/2, self.sprite_rect.top + start_point[1] + self.poly_point_radius/2)
                        pygame.draw.circle(self.surface, color, start_pos, self.poly_point_radius*2, 2)

                        end_pos = (self.sprite_rect.left + end_point[0] + self.poly_point_radius/2, self.sprite_rect.top + end_point[1] + self.poly_point_radius/2)
                        pygame.draw.circle(self.surface, color, end_pos, self.poly_point_radius*2, 2)

                        pygame.draw.line(self.surface, 'darkgreen', start_pos, end_pos, 2)

            # Image Dimensions
            self.draw_image_dimensions()
            
        if self.show_physics:
            space_draw_options = pymunk.pygame_util.DrawOptions(surface)
            self.space.debug_draw(space_draw_options)

        surface.blit(self.surface, self.rect)