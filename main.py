from classes import ui_layer
from config import *
import config
import config.pool_ball_gutter_config as pool_ball_gutter_config
import config.cue_power_bar_config as cue_power_bar_config
from classes.pool_table import PoolTable
from classes.pool_ball import PoolBall
from classes.pool_ball_gutter import PoolBallGutter
from classes.media_manager import MediaManager
from classes.floor import Floor
from classes.ui_layer import UILayer
from classes.sound_manager import SoundManager
from classes.cue_power_bar import CuePowerBar
from classes.draw_mode import DrawMode

class App:
    def __init__(self):
        self.surface = None
        self.rect = None
        self.clock = None
        self.is_running = False
        self.pool_table = None
        self.pool_ball_gutter = None
        self.mouse_position = None
        self.balls_are_in_motion = False
        self.media_manager = None
        self.floor = None
        self.ui_layer = None
        self.active_game_type_index = active_game_type_index
        self.game_types = game_types
        self.active_ball_set_index = active_ball_set_index

        self.cue_power_bar = None
        self.balls = []

    def on_init(self):
        pygame.init()

        self.media_manager = MediaManager()
        self.sound_manager = SoundManager()

        self.surface = pygame.display.set_mode(config.display_size, config.display_flags, config.display_depth)
        self.rect = self.surface.get_rect()
        self.clock = pygame.time.Clock()

        self.setup_ui_menu()
        self.setup_floor()
        self.setup_pool_table()
        self.setup_ball_gutter()
        self.setup_cue_power_bar()
        self.set_table_layout()

        self.is_running = True

    def on_change_floor(self, selected_floor_idx=None):
        if selected_floor_idx < len(self.floor.floor_options):
            self.floor.change_floor(selected_floor_idx)

    def on_change_ball_set(self, selected_ball_set_idx=None):
        if self.active_ball_set_index == selected_ball_set_idx:
            return
        
        self.active_ball_set_index = selected_ball_set_idx
        
        self.reset_table()   
        self.set_table_layout()     

    def reset_table(self):
        self.pool_table.clear_balls()
        self.pool_ball_gutter.clear_balls()
        

    def set_table_layout_as_snooker(self):
        self.balls = []
        
        balls_config = pool_balls_config.snooker_ball_sets[self.active_ball_set_index]
        title, radius, media_folder, mass, elasticity, friction = balls_config

        color = pygame.Color('ivory')
        identifier = 'white'
        media_path = f'{media_folder}/{identifier}.png'
        position = (100, 170)
        cue_ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(cue_ball)
        self.pool_table.set_cue_ball(cue_ball)

        color = pygame.Color('yellow')
        identifier = 'yellow'
        media_path = f'{media_folder}/{identifier}.png'
        position = (160, self.pool_table.height - self.pool_table.height/3)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)

        color = pygame.Color('brown')
        identifier = 'brown'
        media_path = f'{media_folder}/{identifier}.png'
        position = (160, self.pool_table.height/2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)

        color = pygame.Color('green')
        identifier = 'green'
        media_path = f'{media_folder}/{identifier}.png'
        position = (160, self.pool_table.height/3)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)

        color = pygame.Color('blue')
        identifier = 'blue'
        media_path = f'{media_folder}/{identifier}.png'
        position = (self.pool_table.width/2, self.pool_table.height/2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)

        color = pygame.Color('pink')
        identifier = 'pink'
        media_path = f'{media_folder}/{identifier}.png'
        position = ((self.pool_table.width/2) + 146 - radius*2, self.pool_table.height/2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)

        color = pygame.Color('red')
        identifier = 'red'
        media_path = f'{media_folder}/{identifier}.png'
        x_pos = position[0] + radius*2 + 6
        y_pos = position[1]
        position = (x_pos, y_pos)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        x_pos += radius*2
        position = (x_pos, y_pos - radius)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        position = (x_pos, y_pos + radius)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        x_pos += radius*2
        position = (x_pos, y_pos)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        position = (x_pos, y_pos - radius*2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        position = (x_pos, y_pos + radius*2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        x_pos += radius*2
        position = (x_pos, y_pos - radius)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        position = (x_pos, y_pos - radius*3)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        position = (x_pos, y_pos + radius)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        position = (x_pos, y_pos + radius*3)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        x_pos += radius*2
        position = (x_pos, y_pos)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        position = (x_pos, y_pos - radius*2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        position = (x_pos, y_pos - radius*4)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        position = (x_pos, y_pos + radius*2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)
        position = (x_pos, y_pos + radius*4)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)

        color = pygame.Color('black')
        identifier = 'black'
        media_path = f'{media_folder}/{identifier}.png'
        x_pos += radius*2 + 6
        position = (x_pos, y_pos)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball)

        self.pool_table.clear_balls()
        for i, ball in enumerate(self.balls):
            ball.on_init(i)
            self.pool_table.add_ball(ball)

    def set_table_layout_as_billiards(self):
        self.balls = []
        
        balls_config = pool_balls_config.billiard_ball_sets[self.active_ball_set_index]
        title, radius, use_ball_identifier_as_media, media_folder, mass, elasticity, friction, cue_ball_config, eight_ball_config, spot_ball_config, stripe_ball_config = balls_config
        
        color, media = cue_ball_config
        identifier = 'cue'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (120, self.pool_table.height/2)
        cue_ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(cue_ball)
        self.pool_table.set_cue_ball(cue_ball)

        #triangle setup
        #      9
        #     1 10
        #    11 8 2
        #   3 12 4 13
        #  14 5 15 6 7

        #1
        color, media = stripe_ball_config
        identifier = '9'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = ((self.pool_table.width/2) + 150, self.pool_table.height/2)
        ball9 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball9)

        next_x_position_offset = radius * 2

        #2
        color, media = spot_ball_config
        identifier = '1'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0] + next_x_position_offset, position[1] + radius)
        ball1 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball1)

        color, media = stripe_ball_config
        identifier = '10'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball10 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball10)

        #3
        color, media = stripe_ball_config
        identifier = '11'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0] + (radius*2), position[1] + radius*3)
        ball11 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball11)

        color, media = eight_ball_config
        identifier = '8'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball8 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball8)

        color, media = spot_ball_config
        identifier = '2'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball2 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball2)

        #4
        color, media = spot_ball_config
        identifier = '3'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0] + (radius*2), position[1] + radius*5)
        ball3 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball3)

        color, media = stripe_ball_config
        identifier = '12'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball12 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball12)

        color, media = spot_ball_config
        identifier = '4'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball4 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball4)

        color, media = stripe_ball_config
        identifier = '13'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball13 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball13)

        #5
        color, media = stripe_ball_config
        identifier = '14'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0] + (radius*2), position[1] + radius*7)
        ball14 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball14)

        color, media = spot_ball_config
        identifier = '5'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball5 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball5)

        color, media = stripe_ball_config
        identifier = '15'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball15 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball15)

        color, media = spot_ball_config
        identifier = '6'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball6 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball6)

        color, media = spot_ball_config
        identifier = '7'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball7 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path, self.media_manager)
        self.balls.append(ball7)

        self.pool_table.clear_balls()
        for i, ball in enumerate(self.balls):
            ball.on_init(i)
            self.pool_table.add_ball(ball)

    def set_table_layout(self):
        game_type = self.game_types[self.active_game_type_index]
        if game_type == 'Billiards':
            self.set_table_layout_as_billiards()
        elif game_type == 'Snooker':
            self.set_table_layout_as_snooker()

    def setup_ui_menu(self):
        display_size = self.surface.get_size()
        size = (250, display_size[1])
        position = (size[0]/2, size[1]/2)
        on_change_floor = self.on_change_floor
        on_change_ball_set = self.on_change_ball_set
        self.ui_layer = UILayer(size, position, on_change_floor, on_change_ball_set, self.media_manager)
        self.ui_layer.on_init()

    def setup_floor(self):
        self.floor = Floor(self.rect.size, self.rect.center, self.media_manager)
        self.floor.on_init()

    def setup_pool_table(self):
        surface_size = self.surface.get_size()
        position = (surface_size[0]/2, surface_size[1]/2)
        self.pool_table = PoolTable(position, self.media_manager, self.sound_manager)
        self.pool_table.on_init()

    def setup_ball_gutter(self):
        size = pool_ball_gutter_config.pool_ball_gutter_size
        x_buffer = 0
        y_buffer = 40

        position = (self.pool_table.rect.right - size[0]/2 - x_buffer, self.pool_table.rect.bottom + size[1]/2 + y_buffer)
        self.pool_ball_gutter = PoolBallGutter(position, self.media_manager)
        self.pool_ball_gutter.on_init()

    def setup_cue_power_bar(self):
        size = cue_power_bar_config.cue_power_bar_size
        position = (100, self.rect.height/2)
        draw_mode = cue_power_bar_config.cue_power_bar_draw_mode
        self.cue_power_bar = CuePowerBar(draw_mode, size, position, self.media_manager)
        self.cue_power_bar.on_init()

    def on_event(self, event: pygame.event.Event):
        if event.type == QUIT:
            self.is_running = False
            return
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.is_running = False
            return
        
        if event.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]:
            self.mouse_position = event.pos
        
        self.cue_power_bar.on_event(event)
        self.ui_layer.on_event(event)
        self.pool_table.on_event(event)

        # Hit the cue ball

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.pool_table.cue_ball.is_in_active_play and not self.balls_are_in_motion:
                if not self.ui_layer.is_hovered and not self.cue_power_bar.is_hovered:
                    self.apply_force_to_ball(self.pool_table.cue_ball)
                    self.balls_are_in_motion = True

    def apply_force_to_ball(self, ball: PoolBall):
        dx = self.mouse_position[0] - (self.pool_table.rect.x + ball.position[0])
        dy = self.mouse_position[1] - (self.pool_table.rect.y + ball.position[1])
        # distance = math.sqrt(dx*dx + dy*dy)
        angle = math.atan2(dy, dx)
        
        force_magnitude = self.cue_power_bar.power
        force_x = force_magnitude * math.cos(angle - ball.angle)
        force_y = force_magnitude * math.sin(angle - ball.angle)
        
        ball.set_force_at_point((force_x, force_y))

    def update(self, time_lapsed):
        self.ui_layer.update()

        self.cue_power_bar.update()
        self.pool_table.update(time_lapsed)

        if len(self.pool_table.balls_to_remove_from_table) > 0:
            for ball in self.pool_table.balls_to_remove_from_table:
                self.pool_table.remove_ball(ball)
                self.pool_ball_gutter.add_ball(ball)
            
            self.pool_table.balls_to_remove_from_table = []

        self.pool_ball_gutter.update()

        self.balls_are_in_motion = self.pool_table.check_balls_are_moving()

        if self.ui_layer.hovered_component is not None or (self.cue_power_bar.is_hovered and not self.ui_layer.is_active):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


    def draw(self):
        bg_fill = config.display_bg_color
        self.surface.fill(bg_fill)
        
        self.floor.draw(self.surface)
        self.pool_table.draw(self.surface)
        self.pool_ball_gutter.draw(self.surface)
        self.cue_power_bar.draw(self.surface)

        self.ui_layer.draw(self.surface)

        pygame.display.update()
 
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.is_running = False
 
        while( self.is_running ):
            for event in pygame.event.get():
                self.on_event(event)

            time_lapsed = pygame.time.get_ticks()
            self.update(time_lapsed)
            self.draw()
            
            self.clock.tick(config.time_fps)
            pygame.display.set_caption(f"Pool Table: {round(self.clock.get_fps(),3)} fps | {round(time_lapsed / 1000)} secs")

        self.on_cleanup()

 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
    pygame.quit()
