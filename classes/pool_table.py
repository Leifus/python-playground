from classes.decal import Decal
from classes.game_space_config import GameSpaceConfig
from classes.game_sprite import GameSprite
from classes.player import Player
from config import pygame, pymunk, pool_table_config, pool_balls_config, math, Dict
from pygame.locals import *

from classes.light_source import LightSource
from classes.shadow import Shadow
from classes.pool_ball import PoolBall
from classes.pool_table_cushion import PoolTableCushion
from classes.pool_table_pocket import PoolTablePocket
from classes.draw_mode_enum import DrawModeEnum
from classes.__helpers__ import draw_poly_points_around_rect
from globals import media_manager, sound_manager

class PoolTable(GameSprite):
    def __init__(self, size, position, space_config: GameSpaceConfig):
        super(PoolTable, self).__init__()

        self.draw_mode = pool_table_config.pool_table_draw_mode
        self.raw_color = pool_table_config.pool_table_DM_RAW_color
        self.size = size
        self.WIREFRAME_outline_width = pool_table_config.pool_table_DM_WIREFRAME_outline_width
        self.WIREFRAME_poly_point_radius = pool_table_config.pool_table_DM_WIREFRAME_poly_point_radius
        # self.chalk_line_RAW_color = pool_table_config.pool_table_chalk_line_DM_RAW_color
        # self.chalk_line_width = pool_table_config.pool_table_chalk_line_width
        # self.chalk_dot_RAW_color = pool_table_config.pool_table_chalk_dot_DM_RAW_color
        # self.chalk_dot_radius = pool_table_config.pool_table_chalk_dot_radius
        self.table_RICH_media = pool_table_config.pool_table_DM_RICH_media
        # self.chalk_dot_radius = pool_table_config.pool_table_chalk_dot_radius
        
        self.space_config: GameSpaceConfig = space_config
        self.position = position
        # self.width = self.size[0]
        # self.height = self.size[1]

        self.space: pymunk.Space = None
        self.space_draw_options: pymunk.pygame_util.DrawOptions | None = None
        
        self.surface: pygame.Surface | None = pygame.Surface(self.size, pygame.SRCALPHA)

        self.image: pygame.Surface | None = None
        self.orig_image: pygame.Surface | None = None
        self.mask: pygame.mask.Mask | None = None
        self.rect: pygame.Rect | None = self.surface.get_rect(center=self.position)

        self.chalk_line_orig_image: pygame.Surface | None = None
        self.chalk_dot_orig_image: pygame.Surface | None = None
        self.decal_orig_images = []
        self.light_source_overlap_mask: pygame.mask.Mask = None

        self.handlers = []
        self.hovered_ball = None
        self.line_of_sight = None
        self.hit_point = None
        self.hit_shape = None
        self.rays = []
        self.ball_collisions = dict()
        self.time_lapsed = 0
        
        self.pockets_group = pygame.sprite.Group()
        self.cushions_group = pygame.sprite.Group()
        self.ball_group = pygame.sprite.Group()
        self.decals_group = pygame.sprite.Group()
        self.shadow_group = pygame.sprite.Group()

        self.pockets_by_shape: Dict[pymunk.Shape, PoolTablePocket] = dict()
        self.balls_by_shape: Dict[pymunk.Shape, PoolBall] = dict()

        self.relative_mouse_position = None
        
        self.cue_ball: PoolBall = None
        self.cue_ball_first_hit_ball = None
        self.balls_to_remove_from_table = []

        self.setup_visuals()
        self.setup_physical_space()
        self.redraw()
        
    def redraw(self):
        # Table
        self.image = pygame.transform.scale(self.orig_image, self.size)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

        # Decals
        for decal in self.decals_group:
            self.image.blit(decal.image, decal.rect)

        if self.draw_mode in DrawModeEnum.Physics:
            self.space_draw_options = pymunk.pygame_util.DrawOptions(self.surface)

    def setup_visuals(self):
        if self.draw_mode in DrawModeEnum.Wireframe | DrawModeEnum.Raw | DrawModeEnum.Physics:
            outline_width = 0
            if self.draw_mode in DrawModeEnum.Wireframe:
                outline_width = self.WIREFRAME_outline_width

            # Table
            table_image = self.surface.copy()
            table_rect = table_image.get_rect()
            pygame.draw.rect(table_image, self.raw_color, table_rect, outline_width)

            if self.draw_mode in DrawModeEnum.Wireframe:
                color = (0,0,0)
                draw_poly_points_around_rect(table_image, table_rect, color, self.WIREFRAME_poly_point_radius)

            # # Chalk lines
            # for _ in self.chalk_line_positions:
            #     pygame.draw.line(table_image, self.chalk_line_RAW_color, _[0], _[1], self.chalk_line_width)

            # # Chalk dots
            # for position in self.chalk_dots:
            #     position = (position[0], position[1])
            #     pygame.draw.circle(table_image, self.chalk_dot_RAW_color, position, self.chalk_dot_radius, outline_width)

            self.orig_image = table_image
        elif self.draw_mode in DrawModeEnum.Rich:
            # Table
            self.orig_image = media_manager.get(self.table_RICH_media, convert_alpha=True)
            if not self.orig_image:
                print('No table img', self.table_RICH_media)
                return
            
    def setup_physical_space(self):
        self.space = pymunk.Space()
        self.space.iterations = self.space_config.iterations
        self.space.gravity = self.space_config.gravity
        self.space.damping = self.space_config.damping
        self.space.sleep_time_threshold = self.space_config.sleep_time_threshold

        self.setup_physical_collision_handlers()

    def setup_physical_collision_handlers(self):
        handler = self.space.add_collision_handler(pool_balls_config.COLLISION_TYPE_POOL_BALL, pool_balls_config.COLLISION_TYPE_POOL_BALL)
        handler.post_solve = self.on_ball_post_solve_collide_with_ball
        self.handlers.append(handler)
        
        handler = self.space.add_collision_handler(pool_balls_config.COLLISION_TYPE_POOL_BALL, pool_balls_config.COLLISION_TYPE_POOL_TABLE_POCKET)
        handler.pre_solve = self.on_ball_collide_with_pocket
        handler.separate = self.on_ball_separate_from_pocket
        self.handlers.append(handler)

    def add_pocket(self, pocket: PoolTablePocket):
        self.pockets_by_shape[pocket.shape] = pocket
        self.pockets_group.add(pocket)
        self.space.add(pocket.body, pocket.shape)

    def add_cushion(self, cushion: PoolTableCushion):
        self.cushions_group.add(cushion)
        self.space.add(cushion.body, cushion.shape)

    def add_decals(self, decals: pygame.sprite.Group):
        for i, decal in enumerate(decals):
            decal: Decal
            self.decals_group.add(decal)

    def add_ball(self, ball: PoolBall, ball_is_in_play=False):
        self.space.add(ball.body, ball.shape)
        self.ball_group.add(ball)
        self.balls_by_shape[ball.shape] = ball
        
        ball.is_in_active_play = ball_is_in_play

        shadow = Shadow(ball)
        self.shadow_group.add(shadow)

    def update_ball(self, ball: PoolBall):
        orig_ball = None
        for _ in self.ball_group:
            #TODO: Make this better / Use a dict
            if _._identifier == ball._identifier:
                orig_ball = _
                break
        
        if orig_ball is None:
            return
    
        self.ball_group.remove(orig_ball)
        self.ball_group.add(ball)
        self.balls_by_shape[ball.shape] = ball

        orig_shadow = None
        #TODO: Make this better / Use a dict
        for _ in self.shadow_group:
            if _.parent_obj == orig_ball:
                orig_shadow = _
                break
        
        if orig_shadow is not None:
            self.shadow_group.remove(orig_shadow)
            shadow = Shadow(ball)
            self.shadow_group.add(shadow)

    def clear_balls(self):
        for ball in self.ball_group:
            self.space.remove(ball.shape.body, ball.shape)

        self.shadow_group.empty()
        self.balls_by_shape.clear()
        self.ball_group.empty()

    def on_ball_post_solve_collide_with_ball(self, arbiter: pymunk.Arbiter, space: pymunk.Space, data):
        ball_shape_0 = arbiter.shapes[0]
        ball_shape_1 = arbiter.shapes[1]

        if self.cue_ball_first_hit_ball is None and self.cue_ball.shape in arbiter.shapes:
            other_ball = ball_shape_0 if self.cue_ball.shape == ball_shape_0 else ball_shape_1
            self.cue_ball_first_hit_ball = self.balls_by_shape.get(other_ball)

        #TODO: Handle multi-step collision.. yes no?

        # Make collision sound        
        base_volume = 0.8
        volume = base_volume
        if arbiter.is_first_contact:
            ball_0_ke = ball_shape_0.body.kinetic_energy
            ball_1_ke = ball_shape_1.body.kinetic_energy
            total_ke = ball_0_ke + ball_1_ke
            total_ke_loss = arbiter.total_ke
            ke_remaining = total_ke - total_ke_loss
            max_volume_in_ke = 150000  #TODO: Get this from cue_power/somewhere else
            # volume_in_ke = max_volume_in_ke - ke_remaining
            # volume_by_ke = volume_in_ke / max_volume_in_ke
            # dampen_by = ke_remaining / total_ke #NOPE

            ke_scale = total_ke_loss / total_ke
            volume_in_ke = ke_remaining * ke_scale
            volume_scale = (volume_in_ke / max_volume_in_ke) % 1.0
            # volume = base_volume * ke_vol
            
            volume = base_volume * volume_scale

            if volume >= 0.01:
                # print('NOISE collide', volume)
                sound_length = sound_manager.play_sound(pool_balls_config.sound_ball_collide_with_ball, volume)
            else:
                # print('SILENT collide', volume)
                pass
        
        return True

    def on_ball_collide_with_pocket(self, arbiter: pymunk.Arbiter, space, data):
        ball_shape = arbiter.shapes[0]
        pocket_shape = arbiter.shapes[1]

        #This is to handle multiple space stepping before resolving any game changes made.
        # and its probably a bad way to do this.
        collision_handled = self.ball_collisions.get(arbiter.shapes)
        if collision_handled:
            return False

        self.ball_collisions[arbiter.shapes] = True

        distance = 0 - arbiter.contact_point_set.points[0].distance
        buffer = 2

        #TODO: Handle the velocity of the ball.. would it travel past or fall in?
        # ... could we make a real hole or is this too much? Likely, the simple calculations (hah) would be fine..

        ball = self.balls_by_shape.get(ball_shape)
        pocket = self.pockets_by_shape.get(pocket_shape)
        if ball and pocket:
            if pocket.radius > ball.radius: # Pocket is big enough to consume ball
                if distance > ball.radius + buffer: #ball has fallen 'enough' into the pocket
                    ball.stop_moving()
                    self.balls_to_remove_from_table.append(ball)
                    return False
        else:
            print('_!!_ UNHANDLED: PoolTable.on_ball_collide_with_pocket: NO BALL OR POCKET', ball, pocket)

        return True

    def on_ball_separate_from_pocket(self, arbiter: pymunk.Arbiter, space, data):
        return True
    
    def check_balls_are_moving(self):
        margin = 0.1
        for _ in self.ball_group:
            x_v = _.shape.body.velocity[0]
            y_v = _.shape.body.velocity[1]
            if not _.shape.body.is_sleeping and ((x_v < -margin or x_v > margin) or (y_v < -margin or y_v > margin)):
                return True
            
        return False

    def on_event(self, event: pygame.event.Event):
        if event.type not in [MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP]:
            return
        
        mouse_pos = event.pos
        self.relative_mouse_position = (mouse_pos[0] - self.rect.left, mouse_pos[1] - self.rect.top)
        
        if event.type == MOUSEBUTTONDOWN:
            buttons_pressed = pygame.mouse.get_pressed()

            if buttons_pressed[0] and self.cue_ball.is_picked_up:
                self.cue_ball.drop_ball()

    def free_place_cue_ball(self, ball: PoolBall):
        self.add_ball(ball)
        ball.is_in_active_play = True
        self.cue_ball.pick_up_ball()

    def remove_ball(self, ball: PoolBall):
        self.ball_group.remove(ball)
        del self.balls_by_shape[ball.shape]

        shadow = None
        #TODO: Make this better / Use a dict
        for _ in self.shadow_group:
            if _.parent_obj is ball:
                shadow = _
                break
        
        if shadow is not None:
            self.shadow_group.remove(shadow)

        self.space.remove(ball.shape.body, ball.shape)

    def set_cue_ball_in_play(self, ball: PoolBall):
        self.cue_ball = ball

    def ray_cast_ball_path_to_mouse_position(self):        
        ball = self.cue_ball

        # The plan here is to cast two paths from either side of the ball in the direction toward the angle of the mouse.
        # I don't think we'll need a center path but it might be a nice-to-have.

        ball_x = ball.position[0]
        ball_y = ball.position[1]

        # 1: Get the angle to the mouse position.
        dx = self.relative_mouse_position[0] - ball_x
        dy = self.relative_mouse_position[1] - ball_y
        angle_to_mouse_position = math.atan2(dy, dx)

        # 2: Find the points for the ray cast paths offset from the ball.
        perpendicular_angle = angle_to_mouse_position + math.pi/2
        offset_x = ball.radius * math.cos(perpendicular_angle)
        offset_y = ball.radius * math.sin(perpendicular_angle)
        
        center_point = ball.position
        left_point = (ball_x - offset_x, ball_y - offset_y)
        right_point = (ball_x + offset_x, ball_y + offset_y)
        
        # 3: Create the ray cast paths
        max_length = 2000
        ray_length = max_length
        end_x = math.cos(angle_to_mouse_position) * ray_length
        end_y = math.sin(angle_to_mouse_position) * ray_length
        
        self.rays = [
            (center_point, (center_point[0] + end_x, center_point[1] + end_y)),
            (left_point, (left_point[0] + end_x, left_point[1] + end_y)),
            (right_point, (right_point[0] + end_x, right_point[1] + end_y))
        ]

    # def get_ball_raycast(self):
    #     if not self.relative_mouse_position or not self.cue_ball:       #bit lame but better than no check
    #         return
        
    #     cue_x = self.cue_ball.position[0]
    #     cue_y = self.cue_ball.position[1]

    #     # Calculate the LOS start and end points
    #     dx = self.relative_mouse_position[0] - cue_x
    #     dy = self.relative_mouse_position[1] - cue_y
    #     mouse_distance = math.sqrt(dx*dx + dy*dy)
    #     mouse_angle = math.atan2(dy, dx)

    #     ray_length = 2000
    #     ray_dir_x = math.cos(mouse_angle)
    #     ray_dir_y = math.sin(mouse_angle)
    #     ray_end = (self.cue_ball.position[0] + ray_dir_x * ray_length,
    #             self.cue_ball.position[1] + ray_dir_y * ray_length)

    #     # Use segment_query_first for all collisions
    #     query = self.space.segment_query_first(self.cue_ball.position, ray_end, self.cue_ball.radius, pymunk.ShapeFilter())
        
    #     if query:
    #         # Calculate the hit normal
    #         if isinstance(query.shape, pymunk.Circle):
    #             # For balls, normal is from ball center to hit point
    #             normal_x = query.point.x - query.shape.body.position.x
    #             normal_y = query.point.y - query.shape.body.position.y
    #         else:
    #             # Use the segment normal provided by Pymunk
    #             normal_x = query.normal.x
    #             normal_y = query.normal.y
                
    #         # Normalize the normal vector
    #         normal_length = math.sqrt(normal_x * normal_x + normal_y * normal_y)
    #         if normal_length > 0:
    #             normal_x /= normal_length
    #             normal_y /= normal_length
                
    #             # Move the hit point back by ball_radius along the normal
    #             hit_point = pymunk.Vec2d(
    #                 query.point.x + normal_x * self.cue_ball.radius,
    #                 query.point.y + normal_y * self.cue_ball.radius
    #             )
                
    #             return hit_point, query.shape, [(self.cue_ball.position, ray_end)]

    #     return None, None, [(self.cue_ball.position, ray_end)]

    # def find_physical_line_of_sight_collision(self):
    #     if not self.relative_mouse_position or not self.cue_ball:       #bit lame but better than no check
    #         return

    #     # # Calculate the LOS start and end points
    #     # dx = self.relative_mouse_position[0] - self.cue_ball.position[0]
    #     # dy = self.relative_mouse_position[1] - self.cue_ball.position[1]
    #     # mouse_distance = math.sqrt(dx*dx + dy*dy)
    #     # mouse_angle = math.atan2(dy, dx)
        
    #     # starting_x = self.cue_ball.position[0] + math.cos(mouse_angle) * (self.cue_ball.radius + 2)
    #     # starting_y = self.cue_ball.position[1] + math.sin(mouse_angle) * (self.cue_ball.radius + 2)
    #     # start_point = (starting_x, starting_y)

    #     # max_length = self.size[0] if self.size[0] > self.size[1] else self.size[1]
    #     # ending_x = self.cue_ball.position[0] + math.cos(mouse_angle) * max_length
    #     # ending_y = self.cue_ball.position[1] + math.sin(mouse_angle) * max_length
    #     # end_point = (ending_x, ending_y)


    #     cue_x = self.cue_ball.position[0]
    #     cue_y = self.cue_ball.position[1]

    #     # Calculate the LOS start and end points
    #     dx = self.relative_mouse_position[0] - cue_x
    #     dy = self.relative_mouse_position[1] - cue_y
    #     mouse_distance = math.sqrt(dx*dx + dy*dy)
    #     mouse_angle = math.atan2(dy, dx)

    #     # print(mouse_angle)

    #     # cue_x = self.cue_ball.position[0] + math.cos(mouse_angle) * (self.cue_ball.radius + 5)
    #     # cue_y = self.cue_ball.position[1] + math.sin(mouse_angle) * (self.cue_ball.radius + 5)

    #     # # Calculate the LOS start and end points AGAIN!!?!?!
    #     # dx = self.relative_mouse_position[0] - cue_x
    #     # dy = self.relative_mouse_position[1] - cue_y
    #     # mouse_distance = math.sqrt(dx*dx + dy*dy)
    #     # mouse_angle = math.atan2(dy, dx)

    #     starting_x = self.cue_ball.position[0] + math.cos(mouse_angle) * (self.cue_ball.radius + 5)
    #     starting_y = self.cue_ball.position[1] + math.sin(mouse_angle) * (self.cue_ball.radius + 5)
    #     self.los_start_point = (starting_x, starting_y)
    #     # self.los_start_point = (cue_x, cue_y)

    #     max_length = self.size[0] if self.size[0] > self.size[1] else self.size[1]
    #     # max_length = mouse_distance
    #     ending_x = cue_x + math.cos(mouse_angle) * max_length
    #     ending_y = cue_y + math.sin(mouse_angle) * max_length
    #     self.los_end_point = (ending_x, ending_y)


    #     # This doesnt work as clear-cut as you'd expect using the radius..            
    #     # I think we'll need to check from the edges of the cue ball - not only the center.
    #     segment_radius = self.cue_ball.radius   #this makes sense - yes.no?!!! APPARENTLY NOT.
    #     segment_radius = 1
    #     self.physical_line_of_sight_hit = self.space.segment_query_first(self.los_start_point, self.los_end_point, segment_radius, pymunk.ShapeFilter(group=1))

    #     # Remove and recreate the LOS
    #     if self.physical_line_of_sight_hit:
    #         print(self.physical_line_of_sight_hit.point, self.physical_line_of_sight_hit.normal, self.physical_line_of_sight_hit.shape)
    #         if self.line_of_sight:
    #             self.space.remove(self.line_of_sight)

    #         body = self.space.static_body
    #         radius = 1
    #         self.line_of_sight = pymunk.Segment(body, self.los_start_point, self.los_end_point, radius)
    #         self.line_of_sight.sensor = True
    #         self.line_of_sight.collision_type = pool_balls_config.COLLISION_TYPE_LINE_OF_SIGHT
    #         self.space.add(self.line_of_sight)

    def update(self, time_lapsed, player: Player, light_source: LightSource, *args, **kwargs):
        self.ball_collisions.clear()
        self.time_lapsed = time_lapsed

        for _ in range(self.space_config.dt_steps):
            self.space.step(self.space_config.dt / self.space_config.dt_steps)
        
        self.shadow_group.update(self.rect.topleft, light_source)
        
        self.rays = []
        if player.can_take_shot:
            if self.relative_mouse_position and self.cue_ball and not self.cue_ball.is_picked_up:
                self.ray_cast_ball_path_to_mouse_position()
        
        # self.hit_point, self.hit_shape, self.rays = self.get_ball_raycast()
        # self.find_physical_line_of_sight_collision()

        self.pockets_group.update()
        self.cushions_group.update()

        if self.cue_ball and self.cue_ball.is_picked_up:
            x, y = self.relative_mouse_position
            min_x = 30
            min_y = 30
            if x < min_x:
                x = min_x
            elif x > self.rect.width-min_x:
                x = self.rect.width-min_x
            if y < min_y:
                y = min_y
            elif y > self.rect.height-min_y:
                y = self.rect.height-min_y
            position = (x, y)
            self.cue_ball.position = position

        self.ball_group.update()
        
        return super().update(*args, **kwargs)

    def draw(self, surface: pygame.Surface, light_source: LightSource):
        self.surface.fill((0,0,0,0))
        self.surface.blit(self.image, (0,0))

        self.decals_group.draw(self.surface)

        #TODO: Bake this and change only when needed
        self.light_source_overlap_mask = light_source.mask.overlap_mask(self.mask, (0,0))
        if self.light_source_overlap_mask:
            fade_steps = 6
            initial_lumens = light_source.lumens * 0.18
            for i in range(fade_steps):
                fade_step = fade_steps - i
                scale = fade_step * 1.1
                alpha = initial_lumens / fade_step
                light_surface = self.light_source_overlap_mask.to_surface(unsetcolor=None, setcolor=(255,255,190,alpha))
                rect = light_surface.get_rect()
                size = (rect.width*scale, rect.height*scale)
                light_surface = pygame.transform.scale(light_surface, size)
                position = (light_source.rect.left - self.rect.left + rect.width/2, light_source.rect.top - self.rect.top + rect.height/2)
                rect = light_surface.get_rect(center=position)
                self.surface.blit(light_surface, rect)

        # Cast shadows
        self.shadow_group.draw(self.surface)

        if not self.check_balls_are_moving() and self.cue_ball.is_in_active_play and not self.cue_ball.is_picked_up:
            # Cast rays from cue ball
            for ray_start, ray_end in self.rays:
                pygame.draw.line(self.surface, pygame.Color('blue'), ray_start, ray_end, 1)
        
        # # Draw hit point
        # if self.hit_point:
        #     pygame.draw.circle(self.surface, pygame.Color('red'), (int(self.hit_point.x), int(self.hit_point.y)), self.cue_ball.radius, 2)
        #     pygame.draw.line(self.surface, pygame.Color('white'), self.cue_ball.position, (self.hit_point.x, self.hit_point.y), 2)
        
        self.pockets_group.draw(self.surface)
        self.cushions_group.draw(self.surface)
        self.ball_group.draw(self.surface)

        if self.draw_mode in DrawModeEnum.Physics:
            self.space.debug_draw(self.space_draw_options)

        surface.blit(self.surface, self.rect)
