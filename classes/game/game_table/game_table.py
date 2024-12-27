from operator import delitem
from classes.enums.collision_type_enum import CollisionTypeEnum
from classes.game.decal import Decal
from classes.enums.draw_mode_enum import DrawModeEnum
from classes.configs.game_space_config import GameSpaceConfig
from classes.common.game_sprite import GameSprite
from classes.game.game_table_objects.game_table_object import GameTableObject
from classes.light_source import LightSource
from classes.game.pool_ball import PoolBall
from classes.game.pool_table_cushion import PoolTableCushion
from classes.game.pool_table_pocket import PoolTablePocket
from classes.shadow import Shadow
from config import pool_balls_config, pygame, pymunk, Dict, math
from globals import sound_manager

class GameTable(GameSprite):
    def __init__(self, size, position, space_config: GameSpaceConfig, draw_mode: DrawModeEnum):
        super(GameTable, self).__init__()

        self.draw_mode: DrawModeEnum = draw_mode

        self.position = position
        self.space_config: GameSpaceConfig = space_config

        self.surface: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.position)
        
        self.cue_ball: PoolBall | None = None
        self.cue_ball_first_hit_ball: PoolBall | None = None

        self.game_table_objects = pygame.sprite.Group()
        self.ball_group = pygame.sprite.Group()
        self.shadow_group = pygame.sprite.Group()
        self.pockets_group = pygame.sprite.Group()
        self.cushions_group = pygame.sprite.Group()
        self.decals_group = pygame.sprite.Group()

        self.balls_by_shape: Dict[pymunk.Shape, PoolBall] = dict()
        self.pockets_by_shape: Dict[pymunk.Shape, PoolTablePocket] = dict()

        self.space: pymunk.Space = None
        self.space_draw_options: pymunk.pygame_util.DrawOptions | None = None
        if self.draw_mode in DrawModeEnum.Physics:
            self.space_draw_options = pymunk.pygame_util.DrawOptions(self.surface)
        
        self.ball_collisions = dict()
        self.handlers = []
        self.balls_potted = []
        self.rays = []

        self.relative_mouse_position = None

        self.light_sources = []

        self.setup_physical_space()
        self.setup_physical_collision_handlers()
   
    def setup_physical_space(self):
        self.space = pymunk.Space()
        self.space.iterations = self.space_config.iterations
        self.space.gravity = self.space_config.gravity
        self.space.damping = self.space_config.damping
        self.space.sleep_time_threshold = self.space_config.sleep_time_threshold

    def setup_physical_collision_handlers(self):
        # Ball on Ball
        handler = self.space.add_collision_handler(CollisionTypeEnum.COLLISION_TYPE_POOL_BALL.value, CollisionTypeEnum.COLLISION_TYPE_POOL_BALL.value)
        handler.post_solve = self.on_ball_post_solve_collide_with_ball
        self.handlers.append(handler)
        
        # Ball on Pocket
        handler = self.space.add_collision_handler(CollisionTypeEnum.COLLISION_TYPE_POOL_BALL.value, CollisionTypeEnum.COLLISION_TYPE_POOL_TABLE_POCKET.value)
        handler.pre_solve = self.on_ball_collide_with_pocket
        handler.separate = self.on_ball_separate_from_pocket
        self.handlers.append(handler)

        # Ball on TABLE
        handler = self.space.add_collision_handler(CollisionTypeEnum.COLLISION_TYPE_POOL_BALL.value, CollisionTypeEnum.COLLISION_TYPE_GAME_TABLE.value)
        handler.separate = self.on_ball_separate_with_table
        self.handlers.append(handler)
        
        # Ball on Flat Game Object
        handler = self.space.add_collision_handler(CollisionTypeEnum.COLLISION_TYPE_POOL_BALL.value, CollisionTypeEnum.COLLISION_TYPE_FLAT_GAME_OBJECT.value)
        handler.begin = self.on_ball_collide_begin_with_flat_game_object
        handler.pre_solve = self.on_ball_collide_pre_solve_with_flat_game_object
        handler.post_solve = self.on_ball_seperate_post_solve_with_flat_game_object
        handler.separate = self.on_ball_seperate_with_flat_game_object
        self.handlers.append(handler)

    def on_ball_collide_begin_with_flat_game_object(self, arbiter: pymunk.Arbiter, space, data):
        shape = arbiter.shapes[1]

        # Get object by shape: Badly
        game_object = None
        for _game_object in self.game_table_objects:
            _game_object: GameTableObject
            if _game_object.shape == shape:
                game_object = _game_object
                break

        # TODO: This is where we reslve lookup up the ball and then pass it onwards to whomever cares..
        if game_object and game_object.on_collide_begin_func is not None:
            return game_object.on_collide_begin_func(self.time_lapsed, arbiter, space, data)

        return True

    def on_ball_collide_pre_solve_with_flat_game_object(self, arbiter: pymunk.Arbiter, space, data):
        ball_shape = arbiter.shapes[0]
        game_table_object_shape = arbiter.shapes[1]

        # Get object by shape: Badly
        game_object = None
        for _game_object in self.game_table_objects:
            _game_object: GameTableObject
            if _game_object.shape == game_table_object_shape:
                game_object = _game_object
                break

        if game_object and game_object.on_collide_pre_solve_func is not None:
            ball = self.balls_by_shape.get(ball_shape)
            return game_object.on_collide_pre_solve_func(ball, arbiter, space, data)

        return True

    def on_ball_seperate_post_solve_with_flat_game_object(self, arbiter: pymunk.Arbiter, space, data):
        shape = arbiter.shapes[1]

        # Get object by shape: Badly
        game_object = None
        for _game_object in self.game_table_objects:
            _game_object: GameTableObject
            if _game_object.shape == shape:
                game_object = _game_object
                break

        if game_object and game_object.on_collide_post_solve_func is not None:
            return game_object.on_collide_post_solve_func(arbiter, space, data)

        return True

    def on_ball_seperate_with_flat_game_object(self, arbiter: pymunk.Arbiter, space, data):
        shape = arbiter.shapes[1]

        # Get object by shape: Badly
        game_object = None
        for _game_object in self.game_table_objects:
            _game_object: GameTableObject
            if _game_object.shape == shape:
                game_object = _game_object
                break

        if game_object and game_object.on_collide_seperate_func is not None:
            return game_object.on_collide_seperate_func(arbiter, space, data)

        return True

    def on_ball_separate_with_table(self, arbiter: pymunk.Arbiter, space, data):
        print('on_ball_separate_with_table')
        return True

    def check_cue_ball_is_available(self) -> bool:
        if not self.cue_ball:
            return False
        
        return self.cue_ball.is_in_active_play and not self.cue_ball.is_picked_up

    def check_balls_are_moving(self) -> bool:
        margin = 0.1
        for ball in self.ball_group:
            ball: PoolBall
            x_v = ball.shape.body.velocity[0]
            y_v = ball.shape.body.velocity[1]
            if not ball.shape.body.is_sleeping and ((x_v < -margin or x_v > margin) or (y_v < -margin or y_v > margin)):
                return True
            
        return False

    def remove_ball(self, ball: PoolBall):
        ball.stop_moving()
        self.ball_group.remove(ball)
        del self.balls_by_shape[ball.shape]

        existing_shadow = None
        #TODO: Make this better / Use a dict
        for shadow in self.shadow_group:
            shadow: Shadow
            if shadow.parent_obj is ball:
                existing_shadow = shadow
                break
        
        if existing_shadow is not None:
            self.shadow_group.remove(existing_shadow)

        self.space.remove(ball.shape.body, ball.shape)

    def free_place_cue_ball(self, ball: PoolBall):
        self.add_ball(ball)
        ball.is_in_active_play = True
        self.cue_ball.pick_up_ball()

    def add_ball(self, ball: PoolBall, ball_is_in_play=False):
        self.space.add(ball.body, ball.shape)
        self.ball_group.add(ball)
        self.balls_by_shape[ball.shape] = ball
        
        ball.is_in_active_play = ball_is_in_play

        shadow = Shadow(ball)
        self.shadow_group.add(shadow)

    def add_cushion(self, cushion: PoolTableCushion):
        self.cushions_group.add(cushion)
        self.space.add(cushion.body, cushion.shape)
        self.redraw()

    def add_game_table_object(self, game_table_object: GameTableObject):
        self.game_table_objects.add(game_table_object)
        self.space.add(game_table_object.body, game_table_object.shape)

        # shadow = Shadow(game_table_object)
        # self.shadow_group.add(shadow)

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
        # HOW ABOUT A SIMPLE TIMER (HAS THE BALL BEEN IN THE HOLE FOR X?!)

        ball = self.balls_by_shape.get(ball_shape)
        pocket = self.pockets_by_shape.get(pocket_shape)
        if ball and not ball.is_picked_up and pocket:
            if pocket.radius > ball.radius: # Pocket is big enough to consume ball
                if distance > ball.radius + buffer: #ball has fallen 'enough' into the pocket
                    self.balls_potted.append(ball)

        return True

    def on_ball_separate_from_pocket(self, arbiter: pymunk.Arbiter, space, data):
        return True
    
    def clear_balls(self):
        for ball in self.ball_group:
            ball: PoolBall
            self.space.remove(ball.shape.body, ball.shape)

        self.shadow_group.empty()
        self.balls_by_shape.clear()
        self.ball_group.empty()

    def on_event(self, event: pygame.event.Event):
        if event.type not in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            return
        
        mouse_pos = event.pos
        self.relative_mouse_position = (mouse_pos[0] - self.rect.left, mouse_pos[1] - self.rect.top)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            buttons_pressed = pygame.mouse.get_pressed()

            if buttons_pressed[0] and self.cue_ball and self.cue_ball.is_picked_up:
                self.cue_ball.drop_ball()

    def update_ball(self, ball: PoolBall):
        orig_ball = None
        for _ball in self.ball_group:
            _ball: PoolBall
            #TODO: Make this better / Use a dict
            if _ball._identifier == ball._identifier:
                orig_ball = _ball
                break
        
        if orig_ball is None:
            return
    
        self.ball_group.remove(orig_ball)
        self.ball_group.add(ball)
        self.balls_by_shape[ball.shape] = ball

        orig_shadow = None
        #TODO: Make this better / Use a dict
        for _shadow in self.shadow_group:
            _shadow: Shadow
            if _shadow.parent_obj == orig_ball:
                orig_shadow = _shadow
                break
        
        if orig_shadow is not None:
            self.shadow_group.remove(orig_shadow)
            shadow = Shadow(ball)
            self.shadow_group.add(shadow)

    def add_pocket(self, pocket: PoolTablePocket):
        self.pockets_by_shape[pocket.shape] = pocket
        self.pockets_group.add(pocket)
        self.space.add(pocket.body, pocket.shape)

        self.redraw()

    def add_decals(self, decals: pygame.sprite.Group):
        for i, decal in enumerate(decals):
            decal: Decal
            self.decals_group.add(decal)

        self.redraw()

    def add_light_source(self, light_source: LightSource):
        self.light_sources.append(light_source)
        self.redraw()

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

    def update(self, time_lapsed, player_can_take_shot: bool, light_source: LightSource, *args, **kwargs):
        self.ball_collisions.clear()
        self.time_lapsed = time_lapsed

        # THIS IS SHIT AND DOEASNT WORK.. GOT NO EFFECT TYPE OR VALUE.. 
        # THIS SHOULD ALL BE WHERE ITS RELEVEANT....
        # STOP AND THINK ABOUT THE APPROACH

        # Pass the ball_group for now...?
        self.game_table_objects.update(time_lapsed)

        #TODO: Move and recode this away from here.. LAME:
        # Temp place to test
        # if ball_shapes_to_effect:


        for _ in range(self.space_config.dt_steps):
            self.space.step(self.space_config.dt / self.space_config.dt_steps)
        
        self.shadow_group.update(self.rect.topleft, light_source)
        
        self.rays = []
        if player_can_take_shot:
            if self.relative_mouse_position and self.check_cue_ball_is_available():
                self.ray_cast_ball_path_to_mouse_position()

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
        
        #Bit lame check here to keep dictionaries and such in check...
        updated_balls = []
        for ball in self.ball_group:
            ball: PoolBall
            if ball.shape_before_updated is None:
                continue
            updated_balls.append(ball)

        for ball in updated_balls:
            self.balls_by_shape[ball.shape] = ball
            self.balls_by_shape.__delitem__(ball.shape_before_updated)
            ball.shape_before_updated = None

        return super().update(*args, **kwargs)

    def draw(self, surface: pygame.Surface, light_source: LightSource):
        self.surface.fill((0,0,0,0))
        self.surface.blit(self.image, (0,0))

        self.game_table_objects.draw(self.surface)

        # TODO: Bake this and change only when needed
        for light_source in self.light_sources:
            light_source: LightSource
            overlap_mask = light_source.mask.overlap_mask(self.mask, (0,0))
            if overlap_mask:
                fade_steps = 6
                initial_lumens = light_source.lumens * 0.18
                for i in range(fade_steps):
                    fade_step = fade_steps - i
                    scale = fade_step * 1.1
                    alpha = initial_lumens / fade_step
                    light_surface = overlap_mask.to_surface(unsetcolor=None, setcolor=(255,255,190,alpha))
                    rect = light_surface.get_rect()
                    size = (rect.width*scale, rect.height*scale)
                    light_surface = pygame.transform.scale(light_surface, size)
                    position = (light_source.rect.left - self.rect.left + rect.width/2, light_source.rect.top - self.rect.top + rect.height/2)
                    rect = light_surface.get_rect(center=position)
                    self.surface.blit(light_surface, rect)

        # Cast shadows
        self.shadow_group.draw(self.surface)

        if not self.check_balls_are_moving() and self.check_cue_ball_is_available:
            # Cast rays from cue ball
            for ray_start, ray_end in self.rays:
                pygame.draw.line(self.surface, pygame.Color('blue'), ray_start, ray_end, 1)
        
        self.ball_group.draw(self.surface)

        if self.draw_mode in DrawModeEnum.Physics:
            self.space.debug_draw(self.space_draw_options)

        surface.blit(self.surface, self.rect)

    def redraw(self, mask_surface: pygame.Surface = None):
        self.image = pygame.transform.scale(self.orig_image, self.rect.size)

        if not mask_surface:
            mask_surface = self.image
        self.mask = pygame.mask.from_surface(mask_surface)

        self.decals_group.draw(self.image)
        self.pockets_group.draw(self.image)
        self.cushions_group.draw(self.image)
