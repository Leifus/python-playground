from config import pygame, pymunk, pool_table_config, pool_balls_config, random
from pygame.locals import *

import config
from classes.pool_table_cushion import PoolTableCushion
from classes.pool_table_pocket import PoolTablePocket
from classes.pool_ball import PoolBall, POOL_BALL_TYPE_STRIPE, POOL_BALL_TYPE_SPOT, POOL_BALL_TYPE_8, POOL_BALL_TYPE_CUE
from classes.media_manager import MediaManager
from classes.draw_mode import DrawMode

class PoolTable:
    def __init__(self, position, media_manager: MediaManager):
        self.draw_mode = pool_table_config.pool_table_draw_mode
        self.raw_color = pool_table_config.pool_table_DM_RAW_color
        self.size = pool_table_config.pool_table_size
        self.width = self.size[0]
        self.height = self.size[1]
        self.position = position
        self.space = pymunk.Space()
        self.space.iterations = pool_table_config.pool_table_space_iterations
        self.space.gravity = pool_table_config.pool_table_space_gravity
        self.space.damping = pool_table_config.pool_table_space_damping
        self.space.sleep_time_threshold = pool_table_config.pool_table_space_sleep_time_threshold
        self.space_draw_options = None

        self.media_manager = media_manager
        
        self.pockets = []
        self.cushions = []
        self.balls = []
        self.cue_ball = None
        self.mouse_pos = None
        self.balls_to_remove_from_table = []
        
        self.raw_surface = None
        self.raw_rect = None
        self.rich_surface = None
        self.rich_rect = None
        
        self.hovered_ball = None
        self.selected_ball = None

        self.chalk_line_positions = []
        self.chalk_dot_positions = []
        
        self.setup_pockets()
        self.setup_cushions()
        self.setup_balls()
        self.setup_table_chalk_lines()
        self.setup_table_chalk_dots()
        
        self.handlers = []

    def draw_rich_media_layers(self):
        # table
        media_path = pool_table_config.pool_table_DM_RICH_media
        table_surface = self.media_manager.get(media_path, convert_alpha=True)
        if not table_surface:
            print('No table img')
            return
        
        self.rich_surface = pygame.transform.scale(table_surface, self.size)
        self.rich_rect = self.rich_surface.get_rect(center=self.position)

        # decals
        decals = [
            ['spr_Decal_Scratches3.png', 255], 
            ['spr_Decal_Scuff2.png', 200], 
            ['spr_Decal_Scratches1.png', 255], 
            ['spr_Decal_Scratches2.png', 255], 
            ['spr_Decal_Scratches3.png', 255], 
            ['spr_Decal_Scuff1.png', 200], 
            ['spr_Decal_Scratches2.png', 255], 
        ]

        for file_name, alpha in decals:
            media_path = f'table/decals/{file_name}'
            decal_surface = self.media_manager.get(media_path, convert_alpha=True)
            decal_surface.set_alpha(alpha)
            if not decal_surface:
                print('No decal_surface img', media_path)
            else:
                size = decal_surface.get_size()
                rand_x = random.uniform(size[0]/2, self.width-size[0]/2)
                rand_y = random.uniform(size[1]/2, self.height-size[1]/2)
                self.rich_surface.blit(decal_surface, (rand_x, rand_y))
        


    def on_init(self):
        self.raw_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.raw_rect = self.raw_surface.get_rect(center=self.position)

        # if self.draw_mode in DrawMode.RAW | DrawMode.WIREFRAME | DrawMode.PHYSICS:
        #     self.raw_surface.fill(self.raw_color)
        if self.draw_mode in DrawMode.RICH:
            # self.raw_surface.fill((0,0,0,0))

            self.draw_rich_media_layers()
        elif self.draw_mode in DrawMode.PHYSICS:
            self.space_draw_options = pymunk.pygame_util.DrawOptions(self.raw_surface)


        for i, _ in enumerate(self.cushions):
            _.on_init(self.space, i)

        for i, _ in enumerate(self.pockets):
            _.on_init(self.space, i)

        for i, ball in enumerate(self.balls):
            ball.on_init(self.space, i)

        for pocket in self.pockets:
            for ball in self.balls:
                handler = self.space.add_collision_handler(ball.shape.collision_type, pocket.shape.collision_type)
                handler.pre_solve = self.on_ball_collide_with_pocket
                handler.separate = self.on_ball_separate_from_pocket
                self.handlers.append(handler)

    def get_ball_by_shape(self, shape: pymunk.Shape):
        for ball in self.balls:
            if ball.shape == shape:
                return ball
        
        return None

    def on_ball_collide_with_pocket(self, arbiter: pymunk.Arbiter, space, data):
        ball_shape = arbiter.shapes[0]
        distance = 0 - arbiter.contact_point_set.points[0].distance
        buffer = 2

        ball = self.get_ball_by_shape(ball_shape)
        if ball.is_on_table and distance > ball.radius + buffer: #fallen into the pocket
            self.balls_to_remove_from_table.append(ball)
            ball.is_on_table = False

        return True

    def on_ball_separate_from_pocket(self, arbiter, space, data):
        return True
    
    def check_for_hovered_ball(self):
        hovered_ball = None
        max_distance = 3
        hit = self.space.point_query_nearest(self.mouse_pos, max_distance, pymunk.ShapeFilter())
        if hit is not None:
            if hit.shape.collision_type >= pool_balls_config.COLLISION_TYPE_POOL_BALL:
                idx = hit.shape.collision_type - pool_balls_config.COLLISION_TYPE_POOL_BALL
                ball = self.balls[idx]
                if not ball.is_moving:
                    hovered_ball = ball

        if hovered_ball is None:
            if self.hovered_ball is not None:
                self.hovered_ball.highlight_position(show=False)
                self.hovered_ball = None
            
            return
        
        if hovered_ball != self.hovered_ball:
            if self.hovered_ball is not None:
                self.hovered_ball.highlight_position(show=False)

            self.hovered_ball = hovered_ball
            self.hovered_ball.highlight_position(show=True)

    def check_for_moving_balls(self):
        margin = 0.1
        for _ in self.balls:
            x_v = _.shape.body.velocity[0]
            y_v = _.shape.body.velocity[1]
            if not _.shape.body.is_sleeping and ((x_v < -margin or x_v > margin) or (y_v < -margin or y_v > margin)):
                return True
            
        return False

    def on_event(self, event: pygame.event.Event):
        if event.type not in [MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP]:
            return
        
        mouse_pos = event.pos
        self.mouse_pos = (mouse_pos[0] - self.raw_rect.left, mouse_pos[1] - self.raw_rect.top)
        
        # check if we're hovering over a ball
        self.check_for_hovered_ball()

        # if event.type == MOUSEBUTTONDOWN: #and button checks
        #     if self.hovered_ball is not None:
        #         self.selected_ball = self.hovered_ball
            
        
    def setup_table_chalk_dots(self):
        position = (self.width - self.width/4, self.height/2)
        self.chalk_dot_positions.append(position)

        position = (self.width/4, self.height/2)
        self.chalk_dot_positions.append(position)

    def setup_table_chalk_lines(self):
        start_pos = (self.width/4, 0)
        end_pos = (self.width/4, self.height)
        table_third = (start_pos, end_pos)
        self.chalk_line_positions.append(table_third)

    def setup_balls(self):
        position = (120, self.height/2)
        cue_ball = PoolBall(POOL_BALL_TYPE_CUE, 16, position, self.media_manager)
        self.balls.append(cue_ball)
        self.cue_ball = cue_ball

        #triangle setup
        #      9
        #     1 10
        #    11 8 2
        #   3 12 4 13
        #  14 5 15 6 7

        #1
        position = ((self.width/2) + 150, self.height/2)
        ball1 = PoolBall(POOL_BALL_TYPE_STRIPE, 9, position, self.media_manager)
        self.balls.append(ball1)

        next_x_position_offset = pool_balls_config.pool_ball_radius * 2

        #2
        position = (position[0] + next_x_position_offset, position[1] + pool_balls_config.pool_ball_radius)
        ball2 = PoolBall(POOL_BALL_TYPE_SPOT, 1, position, self.media_manager)
        self.balls.append(ball2)
        position = (position[0], position[1] - (pool_balls_config.pool_ball_radius*2))
        ball3 = PoolBall(POOL_BALL_TYPE_STRIPE, 10, position, self.media_manager)
        self.balls.append(ball3)

        #3
        position = (position[0] + (pool_balls_config.pool_ball_radius*2), position[1] + pool_balls_config.pool_ball_radius*3)
        ball4 = PoolBall(POOL_BALL_TYPE_STRIPE, 11, position, self.media_manager)
        self.balls.append(ball4)
        position = (position[0], position[1] - pool_balls_config.pool_ball_radius*2)
        ball5 = PoolBall(POOL_BALL_TYPE_8, 8, position, self.media_manager)
        self.balls.append(ball5)
        position = (position[0], position[1] - pool_balls_config.pool_ball_radius*2)
        ball6 = PoolBall(POOL_BALL_TYPE_SPOT, 2, position, self.media_manager)
        self.balls.append(ball6)

        #4
        position = (position[0] + (pool_balls_config.pool_ball_radius*2), position[1] + pool_balls_config.pool_ball_radius*5)
        ball7 = PoolBall(POOL_BALL_TYPE_SPOT, 3, position, self.media_manager)
        self.balls.append(ball7)
        position = (position[0], position[1] - pool_balls_config.pool_ball_radius*2)
        ball8 = PoolBall(POOL_BALL_TYPE_STRIPE, 12, position, self.media_manager)
        self.balls.append(ball8)
        position = (position[0], position[1] - pool_balls_config.pool_ball_radius*2)
        ball9 = PoolBall(POOL_BALL_TYPE_SPOT, 4, position, self.media_manager)
        self.balls.append(ball9)
        position = (position[0], position[1] - pool_balls_config.pool_ball_radius*2)
        ball10 = PoolBall(POOL_BALL_TYPE_STRIPE, 13, position, self.media_manager)
        self.balls.append(ball10)

        #5
        position = (position[0] + (pool_balls_config.pool_ball_radius*2), position[1] + pool_balls_config.pool_ball_radius*7)
        ball11 = PoolBall(POOL_BALL_TYPE_STRIPE, 14, position, self.media_manager)
        self.balls.append(ball11)
        position = (position[0], position[1] - pool_balls_config.pool_ball_radius*2)
        ball12 = PoolBall(POOL_BALL_TYPE_SPOT, 5, position, self.media_manager)
        self.balls.append(ball12)
        position = (position[0], position[1] - pool_balls_config.pool_ball_radius*2)
        ball13 = PoolBall(POOL_BALL_TYPE_SPOT, 15, position, self.media_manager)
        self.balls.append(ball13)
        position = (position[0], position[1] - pool_balls_config.pool_ball_radius*2)
        ball14 = PoolBall(POOL_BALL_TYPE_SPOT, 6, position, self.media_manager)
        self.balls.append(ball14)
        position = (position[0], position[1] - pool_balls_config.pool_ball_radius*2)
        ball15 = PoolBall(POOL_BALL_TYPE_SPOT, 7, position, self.media_manager)
        self.balls.append(ball15)

    def setup_pockets(self):
        color = pool_table_config.pool_table_pocket_color
        radius = pool_table_config.pool_table_pocket_radius
        corner_radius = pool_table_config.pool_table_corner_pocket_radius

        #top left
        position = (0, 0)
        pocket = PoolTablePocket(corner_radius, color, position)
        self.pockets.append(pocket)

        #top mid
        position = (self.width/2, -radius/2)
        pocket = PoolTablePocket(radius, color, position)
        self.pockets.append(pocket)

        #top right
        position = (self.width, 0)
        pocket = PoolTablePocket(corner_radius, color, position)
        self.pockets.append(pocket)

        #bottom right
        position = (self.width, self.height)
        pocket = PoolTablePocket(corner_radius, color, position)
        self.pockets.append(pocket)

        #bottom mid
        position = (self.width/2, self.height + (radius/2))
        pocket = PoolTablePocket(radius, color, position)
        self.pockets.append(pocket)

        #bottom left
        position = (0, self.height)
        pocket = PoolTablePocket(corner_radius, color, position)
        self.pockets.append(pocket)

    def setup_cushions(self):
        corner_pocket_radius = pool_table_config.pool_table_corner_pocket_radius
        pocket_radius = pool_table_config.pool_table_pocket_radius
        cushion_gap = pool_table_config.pool_table_cushion_gap_to_pocket
        cushion_thickness = pool_table_config.pool_table_cushion_thickness
        bezel_short = pool_table_config.pool_table_cushion_bezel_short
        bezel_long = pool_table_config.pool_table_cushion_bezel_long
        
        #left
        offset = corner_pocket_radius*2 + cushion_gap*4
        width = cushion_thickness
        height = self.height - offset
        position = (width/2, self.height/2)
        poly_points = [
            (0, 0),
            (bezel_short, 0),
            (width - bezel_short/2, bezel_long/2),
            (width, bezel_long),
            (width, height - bezel_long),
            (width - bezel_short/2, height - bezel_long/2),
            (width - bezel_short, height),
            (0, height)
        ]
        cushion = PoolTableCushion((width, height), position, poly_points, self.media_manager)
        self.cushions.append(cushion)

        #right
        position = (self.width - (width/2), self.height/2)
        poly_points = [
            (width, 0), 
            (width, height),
            (bezel_short, height),
            (bezel_short/2, height - bezel_long/2),
            (0, height - bezel_long),
            (0, bezel_long),
            (bezel_short/2, bezel_long/2),
            (bezel_short, 0)
        ]
        cushion = PoolTableCushion((width, height), position, poly_points, self.media_manager)
        self.cushions.append(cushion)

        #top left
        offset = corner_pocket_radius + pocket_radius + cushion_gap*3
        height = cushion_thickness
        width = (self.width/2) - offset
        position = ((width/2) + corner_pocket_radius + cushion_gap*2, height/2)
        poly_points = [
            (0, 0), 
            (width, 0), 
            (width, height - bezel_short),
            (width - bezel_long/2, height - bezel_short/2),
            (width - bezel_long, height),
            (bezel_long, height),
            (bezel_long/2, height - bezel_short/2),
            (0, height - bezel_short)
        ]
        cushion = PoolTableCushion((width, height), position, poly_points, self.media_manager)
        self.cushions.append(cushion)

        #top right
        position = ((self.width/2) + (width/2) + corner_pocket_radius + cushion_gap, height/2)
        cushion = PoolTableCushion((width, height), position, poly_points, self.media_manager)
        self.cushions.append(cushion)

        #bottom left
        offset = corner_pocket_radius + pocket_radius + cushion_gap*3
        height = cushion_thickness
        width = (self.width/2) - offset
        position = ((width/2) + corner_pocket_radius + cushion_gap*2, self.height - (height/2))
        poly_points = [
            (bezel_long, 0),
            (width - bezel_long, 0),
            (width - bezel_long/2, bezel_short/2),
            (width, bezel_short),
            (width, height),
            (0, height),
            (0, bezel_short),
            (bezel_long/2, bezel_short/2),
        ]
        cushion = PoolTableCushion((width, height), position, poly_points, self.media_manager)
        self.cushions.append(cushion)

        #bottom right
        position = ((self.width/2) + (width/2) + corner_pocket_radius + cushion_gap, self.height - (height/2))
        cushion = PoolTableCushion((width, height), position, poly_points, self.media_manager)
        self.cushions.append(cushion)

    def remove_ball(self, ball: PoolBall):
        self.space.remove(ball.shape, ball.shape.body)

    def update(self):
        for _ in range(config.time_dt_steps):
            self.space.step(config.time_dt / config.time_dt_steps)
            
        for _ in self.pockets:
            _.update()

        for _ in self.cushions:
            _.update()

        for _ in self.balls:
            if _.is_on_table:
                _.update()

    def draw(self, surface: pygame.Surface):
        self.raw_surface.fill((0,0,0,0))
        wireframe_thickness = pool_table_config.pool_table_draw_mode_wireframe_thickness

        if self.draw_mode in DrawMode.WIREFRAME:
            # draw table
            rect = pygame.Rect(0, 0, self.raw_rect.width, self.raw_rect.height)
            pygame.draw.rect(self.raw_surface, self.raw_color, rect, wireframe_thickness)

            # draw poly points
            pygame.draw.circle(self.raw_surface, (0,0,0), (0, 0), 2)
            pygame.draw.circle(self.raw_surface, (0,0,0), (self.raw_rect.width, 0), 2)
            pygame.draw.circle(self.raw_surface, (0,0,0), (self.raw_rect.width, self.raw_rect.height), 2)
            pygame.draw.circle(self.raw_surface, (0,0,0), (0, self.raw_rect.height), 2)
        elif self.draw_mode in DrawMode.PHYSICS:
            self.space.debug_draw(self.space_draw_options)
                
        # elif self.draw_mode in DrawMode.RICH:


        # if self.draw_mode in DrawMode.WIREFRAME:
        #     wireframe_thickness = pool_table_config.pool_table_draw_mode_wireframe_thickness

        if self.draw_mode in DrawMode.RAW:
            # draw table
            self.raw_surface.fill(self.raw_color)

            # draw chalk lines
            color = pool_table_config.pool_table_chalk_line_color
            width = pool_table_config.pool_table_chalk_line_width
            for _ in self.chalk_line_positions:
                pygame.draw.line(self.raw_surface, color, _[0], _[1], width)

            # draw chalk dots
            color = pool_table_config.pool_table_chalk_dot_color
            radius = pool_table_config.pool_table_chalk_dot_radius
            outline = 0
            for position in self.chalk_dot_positions:
                position = (position[0] + radius/2, position[1] + radius/2)
                pygame.draw.circle(self.raw_surface, color, position, radius, outline)
            

        for _ in self.pockets:
            _.draw(self.raw_surface)
            
        for _ in self.cushions:
            _.draw(self.raw_surface)
            
        for _ in self.balls:
            if _.is_on_table:
                _.draw(self.raw_surface)


        if self.draw_mode in DrawMode.PHYSICS:
            self.space.debug_draw(self.space_draw_options)

        if self.draw_mode in DrawMode.RICH:
            surface.blit(self.rich_surface, self.rich_rect)

        surface.blit(self.raw_surface, self.raw_rect)
