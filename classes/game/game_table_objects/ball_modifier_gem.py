from classes.common import media_manager
from classes.common.helper_methods import aspect_scale, scale_poly_points
from classes.enums.ball_modification_enum import BallModificationEnum
from classes.enums.collision_type_enum import CollisionTypeEnum
from classes.game.game_table_objects.game_table_object import GameTableObject
from classes.game.pool_ball import PoolBall
from config import pygame, pymunk, math, Dict
from globals import media_manager

class BallModifierGem(GameTableObject):
    def __init__(self, gem_color, ball_modification: BallModificationEnum, effect_value, size, position):
        super(BallModifierGem, self).__init__(size, position)

        self.ball_modification = ball_modification
        self.effect_value = effect_value
        self.gem_color = gem_color
        
        self.shape_collision_type = CollisionTypeEnum.COLLISION_TYPE_FLAT_GAME_OBJECT.value

        self.on_collide_pre_solve_func = self.on_collide_pre_solve

        # TODO: What about resizing this?
        # Gem Poly Points
        self.shape_poly_points = [(-11, -13), (11, -13), (17, -4), (0, 22), (-17, -5)]

        self.balls_to_modify = pygame.sprite.Group()
        self.is_active = True

        self.setup_visuals()
        self.setup_physical_space()
        self.redraw()

    def redraw(self):
        self.surface.fill((0,0,0,0))
        
        image = aspect_scale(self.orig_image, self.size)
        self.surface.blit(image, (0,0))
        self.image = self.surface
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def setup_physical_space(self):
        orig_size = self.orig_image.get_size()
        x_scale = self.size[0] / orig_size[0]
        y_scale = self.size[1] / orig_size[1]
        scale = (x_scale, y_scale)
        scaled_points = scale_poly_points(scale, self.shape_poly_points)

        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        physical_position_offset = (0, -6)  #cheap hack for physical obj from visual img.
        self.body.position = (self.position[0] + physical_position_offset[0], self.position[1] + physical_position_offset[1])
        self.shape = pymunk.Poly(self.body, scaled_points)
        self.shape.sensor = True
        self.shape.collision_type = self.shape_collision_type

    def setup_visuals(self):
        media = f'gems/gem_{self.gem_color}.png'
        self.orig_image = media_manager.get(media)

    def set_ball_radius(self, ball: PoolBall, effect_value):
        new_radius = ball.radius + effect_value
        ball.set_radius(new_radius)

    def set_ball_mass(self, ball: PoolBall, effect_value):
        new_mass = ball.mass * effect_value
        ball.set_mass(new_mass)

    def apply_ball_modifications(self):
        print('BallModifierGem apply_ball_effects!')

        balls = list(self.balls_to_modify)
        if len(self.balls_to_modify) > 0:
            self.balls_to_modify.empty()

        for ball in balls:
            if self.ball_modification == BallModificationEnum.RadiusIncrease:
                self.set_ball_radius(ball, self.effect_value)
            elif self.ball_modification == BallModificationEnum.RadiusDecrease:
                self.set_ball_radius(ball, -self.effect_value)
            elif self.ball_modification in BallModificationEnum.MassIncrease | BallModificationEnum.MassDecrease:
                self.set_ball_mass(ball, self.effect_value)

        self.is_active = False
        self.kill()

    def on_collide_pre_solve(self, ball: PoolBall, arbiter: pymunk.Arbiter, space, data):
        if not ball or not ball.is_in_active_play or ball.is_picked_up or not self.is_active or not arbiter.is_first_contact:
            return True

        if not self.balls_to_modify.has(ball):
            self.balls_to_modify.add(ball)
            print('BallModifierGem triggered!', ball)

        return True 
    
    def update(self, time_lapsed, *args, **kwargs):
        if self.is_active and len(self.balls_to_modify) > 0:
            self.apply_ball_modifications()

        return super().update(*args, time_lapsed, **kwargs)
    
    def kill(self):
        if self.shape.space:
            self.shape.space.remove(self.body, self.shape)

        super().kill()