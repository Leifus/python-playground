

from classes.common.game_sprite import GameSprite
from classes.common.sprite_sheet import SpriteSheet
from classes.enums.merge_object_size_enum import MergeObjectSizeEnum
from config import pymunk, pygame, math, random

class MergeObject(GameSprite):
    def __init__(self, collision_type, size: MergeObjectSizeEnum, sprite_sheet_image_path, sprite_config, current_animation, color_key):
        super(MergeObject, self).__init__()

        self.label = ''
        self.object_size = size
        self.size = self.get_rect_size()
        animate = False
        self.position = (-100,-100)
        self.collision_type = collision_type
        self.sprite_sheet = SpriteSheet(sprite_sheet_image_path, sprite_config, current_animation, color_key, animate)
        self.sprite_sheet.redraw()  # Initially setup the sprite image
        
        self.body: pymunk.Body = None
        self.shapes: list[pymunk.Shape] = []
        self.angle = random.randint(0, 360)
        self.elasticity = 0.1
        self.friction = 0.8
        
        self.construct_physical_body()
        self.redraw()

    def construct_physical_body(self):
        # mass_scale = 1.0
        # self.object_size == MergeObjectSizeEnum.Large:

        base_mass = 1
        base_vertices_dimensions = self.sprite_sheet.current_animation.size
        base_vertices = self.sprite_sheet.current_animation.poly_points
        
        point_scale_x = self.size[0] / base_vertices_dimensions[0]
        point_scale_y = self.size[0] / base_vertices_dimensions[1]
        scaled_points = []
        for point in base_vertices:
            scaled_point = (point[0]*point_scale_x,point[1]*point_scale_y)
            scaled_points.append(scaled_point)


        # moment = pymunk.moment_for_poly(base_mass, scaled_points)
        self.body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.DYNAMIC)
        self.body.position = self.position

        shape = pymunk.Poly(self.body, scaled_points)
        shape.sprite = self
        shape.mass = math.sqrt(shape.area) * base_mass
        shape.elasticity = self.elasticity
        shape.friction = self.friction
        # TODO: Handle Categories
        shape.collision_type = self.collision_type
        self.shapes.append(shape)

    def set_position(self, position):
        self.position = position
        self.body.position = position
        self.body.angle = math.radians(self.angle)
        self.rect = self.image.get_rect(center=self.position)
        
    def redraw(self):
        orig_image = self.sprite_sheet.image
        
        scaled_image = pygame.transform.scale(orig_image, self.size).convert_alpha()
        rotated_image = pygame.transform.rotate(scaled_image, self.angle)
        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.position)

    def get_rect_size(self):
        if self.object_size == MergeObjectSizeEnum.Large:
            return (75,75)
        elif self.object_size == MergeObjectSizeEnum.Medium:
            return (51,51)
        else: # self.object_size == MergeObjectSizeEnum.Small:
            return (32,32)

    def update(self, time_lapsed, *args, **kwargs):
        if self.body.space and not self.body.is_sleeping:
            self.position = self.body.position
            self.rect = self.image.get_rect(center=self.position)
            self.angle = -math.degrees(self.body.angle)
            self.redraw()

        return super().update(*args, **kwargs)