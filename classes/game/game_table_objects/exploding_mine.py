from pygame import Vector2
from classes.enums.collision_type_enum import CollisionTypeEnum
from classes.game.game_table_objects.game_table_object import GameTableObject
from classes.game.pool_ball import PoolBall
from config import pygame, pymunk, math, Dict
from globals import media_manager

class ExplodingMine(GameTableObject):
    def __init__(self, impact_radius, mine_radius, position):
        size = (impact_radius*2, impact_radius*2)
        super(ExplodingMine, self).__init__(size, position)

        self.impact_radius = impact_radius
        self.mine_radius = mine_radius
        self.shape_collision_type = CollisionTypeEnum.COLLISION_TYPE_FLAT_GAME_OBJECT.value

        self.impact_radius_shape: pymunk.Shape | None = None

        self.on_collide_pre_solve_func = self.on_collide_pre_solve
        self.time_till_detonation = None
        self.detonation_time = 2000
        self.is_triggered = False
        self.has_detonated = False
        self.detonation_force = 700000

        self.setup_visuals()
        self.setup_physical_space()
        self.redraw()

    def redraw(self):
        self.surface.fill((0,0,0,0))

        image = pygame.transform.scale(self.orig_image, self.size)
        self.surface.blit(image, (0,0))
        self.image = self.surface
        self.rect = self.image.get_rect(center=self.position)

    def setup_physical_space(self):
        # Mine
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = self.position
        self.shape = pymunk.Circle(self.body, self.mine_radius)
        self.shape.sensor = True
        self.shape.collision_type = self.shape_collision_type
        # self.shape.elasticity = self.elasticity
        # self.shape.friction = self.friction

        # Mine Impact Sensor
        self.impact_radius_shape = pymunk.Circle(self.body, self.impact_radius)
        self.impact_radius_shape.sensor = True
        self.impact_radius_shape.collision_type = self.shape_collision_type
        
    def setup_visuals(self):
        self.orig_image = self.surface.copy()
        color = pygame.Color('grey20')
        center = (self.rect.width/2, self.rect.height/2)
        pygame.draw.circle(self.orig_image, color, center, self.mine_radius)

        color = pygame.Color('chocolate1')
        pygame.draw.circle(self.orig_image, color, center, self.mine_radius/2)

    def on_collide_pre_solve(self, ball: PoolBall, arbiter: pymunk.Arbiter, space, data):
        if self.has_detonated or not arbiter.is_first_contact or self.is_triggered:
            return True

        self.is_triggered = True
        print('ExplodingMine triggered!')

        return True
    
    def detonate(self):
        print('ExplodingMine detonated!')
        
        self.time_till_detonation = None

        space = self.shape.space
        if space is None:
            return
        
        # Find objects impacted by detonation
        affected_shapes = space.shape_query(self.impact_radius_shape)

        if len(affected_shapes) > 0:
            # Set affect to objects
            for shape_info in affected_shapes:
                body: pymunk.Body = shape_info.shape.body
                if body.body_type is not pymunk.Body.DYNAMIC:
                    continue

                contact_normal = shape_info.contact_point_set.normal
                
                angle = contact_normal.angle
                angle_degrees = contact_normal.angle_degrees
                distance_to_ground_zero = Vector2(body.position).distance_to(Vector2(self.position))

                #Where does the body go!? Up!?
                #TEMP: Move it slightly
                if distance_to_ground_zero == 0:
                    distance_to_ground_zero = 0.1
                    
                force_scale = distance_to_ground_zero / self.impact_radius
                force_power = self.detonation_force / force_scale
                force_x = (force_power * math.cos(angle))
                force_y = (force_power * math.sin(angle))

                # if force_x > self.detonation_force or force_y > self.detonation_force:
                    #cap force

                force = (force_x, force_y)
                # print('force', distance_to_ground_zero, force_scale, force_power, force)
                body.apply_force_at_world_point(force, self.position)
    
        self.has_detonated = True

        # Detonation visuals

        # Kill self
        self.kill()

    def set_trigger(self, time_lapsed):
        # Add Impact Radius Sensor
        self.body.space.add(self.impact_radius_shape)
        # self.body.space.remove(self.shape)
        self.time_till_detonation = time_lapsed + self.detonation_time
        self.is_triggered = False

    def update(self, time_lapsed, *args, **kwargs):
        if not self.has_detonated:
            if self.time_till_detonation is not None:
                if time_lapsed > self.time_till_detonation:
                    self.detonate()
            elif self.is_triggered:
                self.set_trigger(time_lapsed)

        return super().update(*args, time_lapsed, **kwargs)
        
    def kill(self):
        if self.impact_radius_shape.space:
            self.impact_radius_shape.space.remove(self.impact_radius_shape)

        super().kill()