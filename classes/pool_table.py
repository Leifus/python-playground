from config import *
import config
from classes.pool_table_cushion import PoolTableCushion
from classes.pool_table_pocket import PoolTablePocket
from classes.pool_ball import PoolBall, POOL_BALL_TYPE_STRIPE, POOL_BALL_TYPE_SPOT, POOL_BALL_TYPE_8, POOL_BALL_TYPE_CUE

class PoolTable:
    def __init__(self, size, color, position):
        self.surface = pygame.Surface(size)
        self.surface.fill(color)
        self.rect = self.surface.get_rect(center=position)
        self.color = color
        self.width = size[0]
        self.height = size[1]
        
        self.space = pymunk.Space()
        self.space.iterations = config.pool_table_space_iterations
        self.space.gravity = config.pool_table_space_gravity
        self.space.damping = config.pool_table_space_damping
        self.space.sleep_time_threshold = config.pool_table_space_sleep_time_threshold
        
        if config.pool_table_space_debug_draw:
            self.space_draw_options = pymunk.pygame_util.DrawOptions(self.surface)

        self.pockets = []
        self.cushions = []
        self.balls = []
        self.cue_ball = None
        self.mouse_pos = None
        self.cue_point_start = None
        self.cue_point_end = None
        self.balls_to_remove_from_table = []
        
        self.hovered_ball = None
        self.selected_ball = None
        
        self.setup_pockets()
        self.setup_cushions()
        self.setup_balls()
        
        self.handlers = []

    def on_init(self):
        self.surface.fill(self.color)

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
            if hit.shape.collision_type >= COLLISION_TYPE_POOL_BALL:
                idx = hit.shape.collision_type - COLLISION_TYPE_POOL_BALL
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
        self.mouse_pos = (mouse_pos[0] - self.rect.left, mouse_pos[1] - self.rect.top)
        
        # check if we're hovering over a ball
        self.check_for_hovered_ball()

        # if event.type == MOUSEBUTTONDOWN: #and button checks
        #     if self.hovered_ball is not None:
        #         self.selected_ball = self.hovered_ball
            
        self.set_cue_points()

    def set_cue_points(self):
        pass
        # if self.hovered_ball is not None and self.hovered_ball.type == POOL_BALL_TYPE_CUE:
        #     self.cue_point_end = None
        #     self.cue_point_start = self.mouse_pos
        # else:
        #     if self.cue_point_start is not None:
        #         self.cue_point_end = self.mouse_pos

        

    def setup_balls(self):
        position = (120, self.height/2)
        cue_ball = PoolBall(POOL_BALL_TYPE_CUE, position)
        self.balls.append(cue_ball)
        self.cue_ball = cue_ball

        #triangle setup
        #      1
        #     1 2
        #    2 8 1
        #   1 2 2 1
        #  2 1 2 1 2

        #1
        position = ((self.width/2) + 150, self.height/2)
        ball1 = PoolBall(POOL_BALL_TYPE_SPOT, position)
        self.balls.append(ball1)

        next_x_position_offset = config.pool_ball_radius * 2

        #2
        position = (position[0] + next_x_position_offset, position[1] + config.pool_ball_radius)
        ball2 = PoolBall(POOL_BALL_TYPE_STRIPE, position)
        self.balls.append(ball2)
        position = (position[0], position[1] - (config.pool_ball_radius*2))
        ball3 = PoolBall(POOL_BALL_TYPE_SPOT, position)
        self.balls.append(ball3)

        #3
        position = (position[0] + (config.pool_ball_radius*2), position[1] + config.pool_ball_radius*3)
        ball4 = PoolBall(POOL_BALL_TYPE_STRIPE, position)
        self.balls.append(ball4)
        position = (position[0], position[1] - config.pool_ball_radius*2)
        ball5 = PoolBall(POOL_BALL_TYPE_8, position)
        self.balls.append(ball5)
        position = (position[0], position[1] - config.pool_ball_radius*2)
        ball6 = PoolBall(POOL_BALL_TYPE_STRIPE, position)
        self.balls.append(ball6)

        #4
        position = (position[0] + (config.pool_ball_radius*2), position[1] + config.pool_ball_radius*5)
        ball7 = PoolBall(POOL_BALL_TYPE_SPOT, position)
        self.balls.append(ball7)
        position = (position[0], position[1] - config.pool_ball_radius*2)
        ball8 = PoolBall(POOL_BALL_TYPE_STRIPE, position)
        self.balls.append(ball8)
        position = (position[0], position[1] - config.pool_ball_radius*2)
        ball9 = PoolBall(POOL_BALL_TYPE_SPOT, position)
        self.balls.append(ball9)
        position = (position[0], position[1] - config.pool_ball_radius*2)
        ball10 = PoolBall(POOL_BALL_TYPE_SPOT, position)
        self.balls.append(ball10)

        #5
        position = (position[0] + (config.pool_ball_radius*2), position[1] + config.pool_ball_radius*7)
        ball11 = PoolBall(POOL_BALL_TYPE_STRIPE, position)
        self.balls.append(ball11)
        position = (position[0], position[1] - config.pool_ball_radius*2)
        ball12 = PoolBall(POOL_BALL_TYPE_SPOT, position)
        self.balls.append(ball12)
        position = (position[0], position[1] - config.pool_ball_radius*2)
        ball13 = PoolBall(POOL_BALL_TYPE_STRIPE, position)
        self.balls.append(ball13)
        position = (position[0], position[1] - config.pool_ball_radius*2)
        ball14 = PoolBall(POOL_BALL_TYPE_SPOT, position)
        self.balls.append(ball14)
        position = (position[0], position[1] - config.pool_ball_radius*2)
        ball15 = PoolBall(POOL_BALL_TYPE_STRIPE, position)
        self.balls.append(ball15)

    def setup_pockets(self):
        color = config.pool_table_pocket_color
        radius = config.pool_table_pocket_radius
        corner_radius = config.pool_table_corner_pocket_radius

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
        elasticity = 0.7
        friction = 0.9
        color = config.pool_table_cushion_color
        corner_pocket_radius = config.pool_table_corner_pocket_radius
        cushion_gap = config.pool_table_cushion_gap_to_pocket
        cushion_thickness = config.pool_table_cushion_thickness
        bezel_short = config.pool_table_cushion_bezel_short
        bezel_long = config.pool_table_cushion_bezel_long
        
        #left
        offset = corner_pocket_radius*2 + cushion_gap*2
        width = cushion_thickness
        height = self.height - offset
        position = (width/2, self.height/2)
        poly_points = [
            (0, 0), 
            (width - bezel_short, 0), 
            (width, bezel_long), 
            (width, height - bezel_long),
            (width-bezel_short, height),
            (0, height)
        ]
        cushion = PoolTableCushion((width, height), color, elasticity, friction, position, poly_points)
        self.cushions.append(cushion)

        #top left
        offset = corner_pocket_radius + config.pool_table_pocket_radius + cushion_gap*2
        height = cushion_thickness
        width = (self.width/2) - offset
        position = ((width/2) + corner_pocket_radius + cushion_gap, height/2)
        poly_points = [
            (0, 0), 
            (width, 0), 
            (width, height - bezel_short),
            (width - bezel_long, height),
            (bezel_long, height),
            (0, height - bezel_short),
        ]
        cushion = PoolTableCushion((width, height), color, elasticity, friction, position, poly_points)
        self.cushions.append(cushion)

        #top right
        position = ((self.width/2) + (width/2) + corner_pocket_radius + cushion_gap, height/2)
        cushion = PoolTableCushion((width, height), color, elasticity, friction, position, poly_points)
        self.cushions.append(cushion)

        #right
        offset = corner_pocket_radius*2 + cushion_gap*2
        width = config.pool_table_cushion_thickness
        height = self.height - offset
        position = (self.width - (width/2), self.height/2)
        poly_points = [
            (bezel_short, 0), 
            (width, 0),
            (width, height),
            (bezel_short, height),
            (0, height - bezel_long),
            (0, bezel_long)
        ]
        cushion = PoolTableCushion((width, height), color, elasticity, friction, position, poly_points)
        self.cushions.append(cushion)

        #bottom left
        offset = corner_pocket_radius + config.pool_table_pocket_radius + cushion_gap*2
        height = config.pool_table_cushion_thickness
        width = (self.width/2) - offset
        position = ((width/2) + corner_pocket_radius + cushion_gap, self.height - (height/2))
        poly_points = [
            (bezel_long, 0),
            (width - bezel_long, 0),
            (width, bezel_short),
            (width, height),
            (0, height),
            (0, bezel_short)
        ]
        cushion = PoolTableCushion((width, height), color, elasticity, friction, position, poly_points)
        self.cushions.append(cushion)

        #bottom right
        position = ((self.width/2) + (width/2) + corner_pocket_radius + cushion_gap, self.height - (height/2))
        cushion = PoolTableCushion((width, height), color, elasticity, friction, position, poly_points)
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

    def draw_cue_points(self):
        start_color = pygame.Color('red')
        end_color = pygame.Color('black')
        line_color = pygame.Color('blue')
        start_radius = 3
        end_radius = 4
        line_width = 2
        if self.cue_point_start is not None:
            pygame.draw.circle(self.surface, start_color, self.cue_point_start, start_radius)
            pygame.draw.circle(self.surface, end_color, self.mouse_pos, end_radius)
            pygame.draw.line(self.surface, line_color, self.cue_point_start, self.mouse_pos, line_width)
    
    def draw(self, surface: pygame.Surface):
        self.surface.fill(self.color)

        for _ in self.pockets:
            _.draw(self.surface)
            
        for _ in self.cushions:
            _.draw(self.surface)
            
        for _ in self.balls:
            if _.is_on_table:
                _.draw(self.surface)

        self.draw_cue_points()


        if config.pool_table_space_debug_draw:
            self.space.debug_draw(self.space_draw_options)

        surface.blit(self.surface, self.rect)
