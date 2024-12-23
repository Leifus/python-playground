from classes.game_lobby import GameLobby
from classes.game_mode_enum import GameModeEnum
from classes.game_session import GameSession
from classes.in_game_event_enum import InGameEventEnum
from classes.player import Player
from classes.players_gui import PlayersGui
from classes.pool_table_pocket import PoolTablePocket
from config import *
import config
import config.pool_ball_gutter_config as pool_ball_gutter_config
import config.cue_power_bar_config as cue_power_bar_config
from globals import media_manager, sound_manager
from classes.pool_table import PoolTable
from classes.pool_ball import PoolBall
from classes.pool_ball_gutter import PoolBallGutter
from classes.floor import Floor
from classes.ui_layer import UILayer
from classes.cue_power_bar import CuePowerBar
from classes.light_source import LightSource


class App:
    def __init__(self):
        self.surface = None
        self.rect = None
        self.app_is_running = False
        self.pool_table: PoolTable = None
        self.pool_ball_gutter = None
        self.mouse_position = None
        self.balls_are_in_motion = False
        self.floor: Floor = None
        self.ui_layer: UILayer = None
        self.players_gui: PlayersGui = None
        self.active_ball_set_index = 0

        self.cue_power_bar = None
        self.balls = []
        self.cue_hitting_ball_sound = 'cue_hit_ball_1.wav'
        self.cue_ball_out_of_play_time_to_reset = 2000
        self.cue_ball_reset_ttl = None

        self.game_lobby: GameLobby = None
        self.game_session: GameSession = None

        self.active_player: Player = None

        self.camera_screens = pygame.sprite.Group()

    def on_init(self):
        pygame.init()

        self.surface = pygame.display.set_mode(config.display_size, config.display_flags, config.display_depth)
        self.rect = self.surface.get_rect()

        self.setup_game_lobby()
        self.setup_players_gui()
        self.setup_ui_menu()
        self.setup_floor()
        self.setup_lighting()
        self.setup_cue_power_bar()
        self.setup_camera_screen() # TODO: MOVE THIS FIX THIS

        self.app_is_running = True

    def on_change_floor(self, selected_floor_idx=None):
        if selected_floor_idx < len(self.floor.floor_options):
            self.floor.update(selected_floor_idx)

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
        cue_ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(cue_ball)
        self.pool_table.set_cue_ball_in_play(cue_ball)

        color = pygame.Color('yellow')
        identifier = 'yellow'
        media_path = f'{media_folder}/{identifier}.png'
        position = (160, self.pool_table.height - self.pool_table.height/3)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)

        color = pygame.Color('brown')
        identifier = 'brown'
        media_path = f'{media_folder}/{identifier}.png'
        position = (160, self.pool_table.height/2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)

        color = pygame.Color('green')
        identifier = 'green'
        media_path = f'{media_folder}/{identifier}.png'
        position = (160, self.pool_table.height/3)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)

        color = pygame.Color('blue')
        identifier = 'blue'
        media_path = f'{media_folder}/{identifier}.png'
        position = (self.pool_table.width/2, self.pool_table.height/2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)

        color = pygame.Color('pink')
        identifier = 'pink'
        media_path = f'{media_folder}/{identifier}.png'
        position = ((self.pool_table.width/2) + 146 - radius*2, self.pool_table.height/2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)

        color = pygame.Color('red')
        identifier = 'red'
        media_path = f'{media_folder}/{identifier}.png'
        x_offset_from_pink = 6
        x_pos = position[0] + radius*2 + x_offset_from_pink
        y_pos = position[1]
        position = (x_pos, y_pos)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        x_pos += radius*2
        position = (x_pos, y_pos - radius)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        position = (x_pos, y_pos + radius)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        x_pos += radius*2
        position = (x_pos, y_pos)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        position = (x_pos, y_pos - radius*2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        position = (x_pos, y_pos + radius*2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        x_pos += radius*2
        position = (x_pos, y_pos - radius)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        position = (x_pos, y_pos - radius*3)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        position = (x_pos, y_pos + radius)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        position = (x_pos, y_pos + radius*3)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        x_pos += radius*2
        position = (x_pos, y_pos)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        position = (x_pos, y_pos - radius*2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        position = (x_pos, y_pos - radius*4)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        position = (x_pos, y_pos + radius*2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)
        position = (x_pos, y_pos + radius*4)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)

        color = pygame.Color('black')
        identifier = 'black'
        media_path = f'{media_folder}/{identifier}.png'
        x_offset_from_reds = 6
        x_pos += radius*2 + x_offset_from_reds
        position = (x_pos, y_pos)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball)

        self.pool_table.clear_balls()
        for i, ball in enumerate(self.balls):
            self.pool_table.add_ball(ball, ball_is_in_play=True)

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
        cue_ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(cue_ball)
        self.pool_table.set_cue_ball_in_play(cue_ball)

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
        ball9 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
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
        ball1 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball1)

        color, media = stripe_ball_config
        identifier = '10'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball10 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball10)

        #3
        color, media = stripe_ball_config
        identifier = '11'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0] + (radius*2), position[1] + radius*3)
        ball11 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball11)

        color, media = eight_ball_config
        identifier = '8'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball8 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball8)

        color, media = spot_ball_config
        identifier = '2'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball2 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball2)

        #4
        color, media = spot_ball_config
        identifier = '3'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0] + (radius*2), position[1] + radius*5)
        ball3 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball3)

        color, media = stripe_ball_config
        identifier = '12'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball12 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball12)

        color, media = spot_ball_config
        identifier = '4'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball4 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball4)

        color, media = stripe_ball_config
        identifier = '13'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball13 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball13)

        #5
        color, media = stripe_ball_config
        identifier = '14'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0] + (radius*2), position[1] + radius*7)
        ball14 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball14)

        color, media = spot_ball_config
        identifier = '5'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball5 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball5)

        color, media = stripe_ball_config
        identifier = '15'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball15 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball15)

        color, media = spot_ball_config
        identifier = '6'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball6 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball6)

        color, media = spot_ball_config
        identifier = '7'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball7 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        self.balls.append(ball7)

        self.pool_table.clear_balls()
        for i, ball in enumerate(self.balls):
            self.pool_table.add_ball(ball, ball_is_in_play=True)

    def set_table_layout(self):
        if self.game_session is None:
            return
        
        if self.game_session.game_mode == GameModeEnum.Billiards:
            self.set_table_layout_as_billiards()
        elif self.game_session.game_mode == GameModeEnum.Snooker:
            self.set_table_layout_as_snooker()

    def setup_game_lobby(self):
        size = (self.rect.width*0.9, self.rect.height*0.9)
        position = self.rect.center
        self.game_lobby = GameLobby(size, position)
        self.game_lobby.is_active = True

    def setup_players_gui(self):
        size = (self.rect.width/2, 200)
        position = (self.rect.centerx, self.rect.top)
        self.players_gui = PlayersGui(size, position)

    def setup_ui_menu(self):
        display_size = self.surface.get_size()
        size = (250, display_size[1])
        position = (size[0]/2, size[1]/2)
        on_change_floor = self.on_change_floor
        on_change_ball_set = self.on_change_ball_set
        self.ui_layer = UILayer(size, position, on_change_floor, on_change_ball_set)

    def setup_lighting(self):
        radius = 40
        position = (self.rect.centerx, self.rect.centery)
        z_position = 300    #distance from table in cm (ish)
        lumens = 32  #255 max at the moment.
        show_light = False
        self.light_source = LightSource(lumens, radius, position, z_position, show_light)

    def setup_floor(self):
        self.floor = Floor(self.rect.size, self.rect.center)
        self.floor.on_init()

    def setup_pool_table(self):
        if self.game_session is None or self.game_session.game_mode is GameModeEnum.NONE:
            print('CANT SETUP POOL TABLE: NO GAMESESSION SET')
            return
        
        self.cue_ball_reset_ttl = None
        
        if self.pool_table is not None:
            self.pool_table = self.pool_table.kill()
        
        surface_size = self.surface.get_size()
        position = (surface_size[0]/2, surface_size[1]/2)
        self.pool_table = PoolTable(position, self.game_session.game_mode_config.space_config)
        self.pool_table.on_init()

    def setup_ball_gutter(self):
        if self.game_session is None or self.game_session.game_mode is GameModeEnum.NONE:
            print('CANT SETUP POOL BALL GUTTER: NO GAMESESSION SET')
            return
        
        if self.pool_ball_gutter is not None:
            self.pool_ball_gutter = self.pool_ball_gutter.kill()

        size = pool_ball_gutter_config.pool_ball_gutter_size
        x_buffer = 0
        y_buffer = 40

        position = (self.pool_table.rect.right - size[0]/2 - x_buffer, self.pool_table.rect.bottom + size[1]/2 + y_buffer)
        self.pool_ball_gutter = PoolBallGutter(position, self.game_session.game_mode_config.space_config)
        self.pool_ball_gutter.on_init()

    def setup_cue_power_bar(self):
        size = cue_power_bar_config.cue_power_bar_size
        position = (100, self.rect.height/2)
        draw_mode = cue_power_bar_config.cue_power_bar_draw_mode
        self.cue_power_bar = CuePowerBar(draw_mode, size, position)
        self.cue_power_bar.on_init()

    def setup_camera_screen(self):
        # size = (200, 200)
        # position = self.rect.center
        # camera = Camera(size, position)

        # size = (200, 200)
        # position = (size[0]/2 + 20, self.rect.height - size[1]/2 - 20)
        # camera_screen = CameraScreen(size, position, camera)
        # self.camera_screens.add(camera_screen)
        pass

    def quit_to_menu(self):
        if self.game_session is not None:
            self.game_session.is_running = False
            #TODO: Gentle tear down (and reporting/logging)
        
        self.game_session = None
        self.game_lobby.is_active = True


    def on_event(self, event: pygame.event.Event):
        if event.type == QUIT:
            self.app_is_running = False
            return
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            if not self.game_lobby.is_active:
                self.quit_to_menu()
            else:
                self.app_is_running = False
                return
        
        if event.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]:
            self.mouse_position = event.pos
        
        if self.game_lobby.is_active:
            self.game_lobby.on_event(self.mouse_position, event)

        if self.game_session is None or not self.game_session.is_running:
            return
        
        self.game_session.on_event(event)
        self.ui_layer.on_event(event)
        
        if not self.ui_layer.is_active:
            self.cue_power_bar.on_event(event)

        self.pool_table.on_event(event)

        # Player takes a shot
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if not self.ui_layer.is_hovered and not self.cue_power_bar.is_hovered:
                if self.pool_table.cue_ball.is_in_active_play and not self.balls_are_in_motion:
                    self.take_player_shot()

    def take_player_shot(self):
        self.apply_force_to_ball(self.pool_table.cue_ball)
        self.balls_are_in_motion = True
        self.active_player.is_taking_shot = True

    def apply_force_to_ball(self, ball: PoolBall):
        dx = self.mouse_position[0] - (self.pool_table.rect.x + ball.position[0])
        dy = self.mouse_position[1] - (self.pool_table.rect.y + ball.position[1])
        # distance = math.sqrt(dx*dx + dy*dy)
        angle = math.atan2(dy, dx)
        
        force_magnitude = self.cue_power_bar.power
        force_x = force_magnitude * math.cos(angle - ball.angle)
        force_y = force_magnitude * math.sin(angle - ball.angle)
        
        ball.set_force_at_point((force_x, force_y))
        max_volume = 0.3    #hack for my cheap sounds
        volume = self.cue_power_bar.power_percent * max_volume
        sound_manager.play_sound(self.cue_hitting_ball_sound, volume)

    def change_random_ball_size(self):
        balls = []
        for ball in self.pool_table.ball_group:
            if ball.is_in_active_play:
                balls.append(ball)

        radius = random.randint(0, 50)
        ball_idx = random.randint(0, len(balls)-1)
        ball = balls[ball_idx]
        ball.set_radius(radius)
        self.pool_table.update_ball(ball)

        print('changing ball size', ball.identifier, radius)

    def change_random_ball_mass(self):
        balls = []
        for ball in self.pool_table.ball_group:
            if ball.is_in_active_play:
                balls.append(ball)

        mass = random.uniform(0, 50)
        ball_idx = random.randint(0, len(balls)-1)
        ball = balls[ball_idx]
        ball.set_mass(mass)
        self.pool_table.update_ball(ball)

        print('changing ball mass', ball.identifier, mass)

    def spawn_random_hole(self):
        radius = random.uniform(10, 30)
        rand_x = random.uniform(radius/2, self.pool_table.rect.width - radius/2)
        rand_y = random.uniform(radius/2, self.pool_table.rect.height - radius/2)
        position = (rand_x, rand_y)
        hole = PoolTablePocket(position, radius)
        self.pool_table.add_pocket(hole)

    def action_game_events(self):
        for kvp in self.game_session.game_events_to_action.items():
            event_time, game_event = kvp
            print('action_game_event', game_event.name, event_time)
            if game_event is InGameEventEnum.Spawn_Hole:
                self.spawn_random_hole()
            elif game_event is InGameEventEnum.Ball_Size:
                self.change_random_ball_size()
            elif game_event is InGameEventEnum.Ball_Mass:
                self.change_random_ball_mass()

        self.game_session.game_events_to_action.clear()

    def update_active_game_session(self):
        self.game_session.update()
        time_lapsed = self.game_session.time_lapsed

        if len(self.game_session.game_events_to_action) > 0:
            self.action_game_events()

        self.players_gui.update()
        self.ui_layer.update(self.game_session.game_mode)
        self.cue_power_bar.update()
        self.light_source.update(self.ui_layer.light_options, self.mouse_position)
        
        self.pool_table.update(self.game_session.time_lapsed, self.active_player, self.light_source)
        for camera_screen in self.camera_screens:
            camera_screen.update(self.surface)

        self.balls_are_in_motion = self.pool_table.check_balls_are_moving()

        if self.pool_table.cue_ball_first_hit_ball is not None and self.active_player.is_taking_shot:
            self.active_player.first_contact = self.pool_table.cue_ball_first_hit_ball

        if len(self.pool_table.balls_to_remove_from_table) > 0: # Balls potted
            for ball in self.pool_table.balls_to_remove_from_table:
                ball.stop_moving()

                self.active_player.add_potted_ball(ball)
                self.pool_table.remove_ball(ball)
                self.pool_ball_gutter.add_ball(ball)
            
            self.pool_table.balls_to_remove_from_table = []

        self.pool_ball_gutter.update()
        
        cue_ball = self.pool_table.cue_ball
        if not self.balls_are_in_motion and not cue_ball.is_in_active_play and not cue_ball.is_picked_up and self.cue_ball_reset_ttl is None:
            self.cue_ball_reset_ttl = time_lapsed + self.cue_ball_out_of_play_time_to_reset

        if self.cue_ball_reset_ttl is not None and time_lapsed > self.cue_ball_reset_ttl:
            self.pool_ball_gutter.remove_ball(cue_ball)
            self.pool_table.free_place_cue_ball(cue_ball)
            self.cue_ball_reset_ttl = None
        
        if self.cue_ball_reset_ttl is None: # No wait timer
            if not self.balls_are_in_motion: # No moving balls
                if self.active_player.is_taking_shot: # Player has taken shot
                    if self.active_player.first_contact is None: # No cue ball hit
                        self.active_player.has_faulted_shot = True
                    
                    if not self.check_potted_balls_are_player_friendly():
                        self.active_player.has_faulted_shot = True

                    if self.active_player.has_faulted_shot or len(self.active_player.balls_potted_this_shot) == 0:
                        self.active_player.end_turn()
                        next_player = self.game_session.move_to_next_player()
                        self.active_player = next_player
                        self.active_player.can_take_shot = True
                        self.players_gui.redraw()

                    self.active_player.end_shot()
                    self.pool_table.cue_ball_first_hit_ball = None

        if self.ui_layer.queued_game_event is not InGameEventEnum.NONE:
            time_to_activate = 2 * 1000
            self.game_session.queue_game_event(self.ui_layer.queued_game_event, time_to_activate)
            self.ui_layer.queued_game_event = InGameEventEnum.NONE

    def check_potted_balls_are_player_friendly(self):
        disallowed_balls = [
            self.pool_table.cue_ball
        ]

        for ball in self.active_player.balls_potted:
            if ball in disallowed_balls:
                return False
            
        return True

    def create_new_game_session(self, game_mode: str):
        # TODO: End existing game session (if exists)

        # Create new game and session
        game_mode_enum = GameModeEnum[game_mode]
        game_id = f'{game_mode} Game'
        self.game_session = GameSession(game_id, game_mode_enum)
        self.active_ball_set_index = 0
        self.active_player = self.game_session.get_first_player()
        self.game_session.set_active_player(self.active_player)
        self.players_gui.setup_players(self.game_session.players)
        self.active_player.can_take_shot = True

        self.setup_pool_table()
        self.setup_ball_gutter()
        self.set_table_layout()

    def update(self):
        self.game_lobby.update()
        if self.game_lobby.is_active:
            if self.game_session is not None:
                self.game_session.is_running = False    #Force this for now

            if self.game_lobby.start_new_game:
                self.game_lobby.start_new_game = False
                self.create_new_game_session(self.game_lobby.selected_game_mode)
                self.game_lobby.is_active = False
                self.game_lobby.hovered_component = None
                self.game_session.is_running = True

        if self.game_session is not None and self.game_session.is_running:
            self.update_active_game_session()

        if self.game_lobby.hovered_component is not None or self.ui_layer.hovered_component is not None or (self.cue_power_bar.is_hovered and not self.ui_layer.is_active):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw_running_game(self):
        self.floor.draw(self.surface)
        self.pool_table.draw(self.surface, self.light_source)
        self.pool_ball_gutter.draw(self.surface)
        self.cue_power_bar.draw(self.surface)
        self.light_source.draw(self.surface)
        for camera_screen in self.camera_screens:
            camera_screen.draw(self.surface)
        self.ui_layer.draw(self.surface)
        self.players_gui.draw(self.surface)

    def draw(self):
        bg_fill = config.display_bg_color
        self.surface.fill(bg_fill)

        if self.game_lobby.is_active:
            self.game_lobby.draw(self.surface)
                    
        if self.game_session is not None and self.game_session.is_running:
            self.draw_running_game()

        pygame.display.update()
 
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.app_is_running = False
 
        pygame.display.set_caption("Pwl Arcade")

        while( self.app_is_running ):
            for event in pygame.event.get():
                self.on_event(event)

            self.update()
            self.draw()

            # if self.game_session is not None:
            #     self.game_session.update()

            # time_lapsed = pygame.time.get_ticks()
            # self.update(time_lapsed)
            
            # self.clock.tick(config.time_fps)
            # pygame.display.set_caption(f"Pool Table: {round(self.clock.get_fps(),3)} fps | {round(time_lapsed / 1000)} secs")

        self.on_cleanup()

 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
    pygame.quit()
