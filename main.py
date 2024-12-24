from classes.decal import Decal
from classes.draw_mode_enum import DrawModeEnum
from classes.game_lobby import GameLobby
from classes.game_mode_enum import GameModeEnum
from classes.game_session import GameSession
from classes.game_tables.billiards_game_table import BilliardsGameTable
from classes.game_tables.circle_game_table import CircleGameTable
from classes.game_tables.game_table import GameTable
from classes.game_tables.snooker_game_table import SnookerGameTable
from classes.in_game_event_enum import InGameEventEnum
from classes.player import Player
from classes.players_gui import PlayersGui
from classes.pool_table_cushion import PoolTableCushion
from classes.pool_table_pocket import PoolTablePocket
from config import *
import config
from config import pool_table_config
import config.pool_ball_gutter_config as pool_ball_gutter_config
import config.cue_power_bar_config as cue_power_bar_config
from globals import media_manager
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
        self.pool_ball_gutter = None
        self.mouse_position = None
        self.balls_are_in_motion = False
        self.floor: Floor = None
        self.ui_layer: UILayer = None
        self.players_gui: PlayersGui = None
        self.active_ball_set_index = 0

        self.cue_power_bar = None
        self.balls = []
        self.cue_ball_out_of_play_time_to_reset = 2000
        self.cue_ball_reset_ttl = None

        self.game_lobby: GameLobby = None
        self.game_session: GameSession | None = None

        self.active_player: Player = None

        self.camera_screens = pygame.sprite.Group()
        self.general_light_dim_surface: pygame.Surface = None

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
        self.construct_game_table()

    def reset_table(self):
        self.game_session.game_table.clear_balls()
        if self.pool_ball_gutter:
            self.pool_ball_gutter.clear_balls()

    def construct_billiards_balls(self, table_rect: pygame.Rect):
        ball_group = pygame.sprite.Group()
        
        balls_config = pool_balls_config.billiard_ball_sets[self.active_ball_set_index]
        title, radius, use_ball_identifier_as_media, media_folder, mass, elasticity, friction, cue_ball_config, eight_ball_config, spot_ball_config, stripe_ball_config = balls_config
        
        color, media = cue_ball_config
        identifier = 'cue'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (120, table_rect.height/2)
        cue_ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(cue_ball)

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
        position = ((table_rect.width/2) + 150, table_rect.height/2)
        ball9 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball9)

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
        ball_group.add(ball1)

        color, media = stripe_ball_config
        identifier = '10'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball10 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball10)

        #3
        color, media = stripe_ball_config
        identifier = '11'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0] + (radius*2), position[1] + radius*3)
        ball11 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball11)

        color, media = eight_ball_config
        identifier = '8'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball8 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball8)

        color, media = spot_ball_config
        identifier = '2'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball2 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball2)

        #4
        color, media = spot_ball_config
        identifier = '3'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0] + (radius*2), position[1] + radius*5)
        ball3 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball3)

        color, media = stripe_ball_config
        identifier = '12'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball12 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball12)

        color, media = spot_ball_config
        identifier = '4'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball4 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball4)

        color, media = stripe_ball_config
        identifier = '13'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball13 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball13)

        #5
        color, media = stripe_ball_config
        identifier = '14'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0] + (radius*2), position[1] + radius*7)
        ball14 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball14)

        color, media = spot_ball_config
        identifier = '5'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball5 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball5)

        color, media = stripe_ball_config
        identifier = '15'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball15 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball15)

        color, media = spot_ball_config
        identifier = '6'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball6 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball6)

        color, media = spot_ball_config
        identifier = '7'
        if use_ball_identifier_as_media:
            media_path = f'{media_folder}/{identifier}.png'
        else:
            media_path = f'{media_folder}/{media}'
        position = (position[0], position[1] - radius*2)
        ball7 = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball7)
        
        return cue_ball, ball_group

    def construct_classic_table_cushions(self, table_rect: pygame.Rect):
        cushion_group = pygame.sprite.Group()
        pocket_radius = pool_table_config.pool_table_pocket_radius
        cushion_gap = pool_table_config.pool_table_cushion_gap_to_pocket
        cushion_thickness = pool_table_config.pool_table_cushion_thickness
        bezel_short = pool_table_config.pool_table_cushion_bezel_short
        bezel_long = pool_table_config.pool_table_cushion_bezel_long
        
        #left
        offset = pocket_radius*2 + cushion_gap*4
        width = cushion_thickness
        height = table_rect.height - offset
        position = (width/2, table_rect.height/2)
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
        cushion = PoolTableCushion((width, height), position, poly_points)
        cushion_group.add(cushion)

        #right
        position = (table_rect.width - (width/2), table_rect.height/2)
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
        cushion = PoolTableCushion((width, height), position, poly_points)
        cushion_group.add(cushion)

        #top left
        offset = pocket_radius*2 + cushion_gap*3
        height = cushion_thickness
        width = (table_rect.width/2) - offset
        position = ((width/2) + pocket_radius + cushion_gap*2, height/2)
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
        cushion = PoolTableCushion((width, height), position, poly_points)
        cushion_group.add(cushion)

        #top right
        position = ((table_rect.width/2) + (width/2) + pocket_radius + cushion_gap, height/2)
        cushion = PoolTableCushion((width, height), position, poly_points)
        cushion_group.add(cushion)

        #bottom left
        offset = pocket_radius*2 + cushion_gap*3
        height = cushion_thickness
        width = (table_rect.width/2) - offset
        position = ((width/2) + pocket_radius + cushion_gap*2, table_rect.height - (height/2))
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
        cushion = PoolTableCushion((width, height), position, poly_points)
        cushion_group.add(cushion)

        #bottom right
        position = ((table_rect.width/2) + (width/2) + pocket_radius + cushion_gap, table_rect.height - (height/2))
        cushion = PoolTableCushion((width, height), position, poly_points)
        cushion_group.add(cushion)

        return cushion_group

    def construct_classic_table_pockets(self, table_rect: pygame.Rect):
        pocket_group = pygame.sprite.Group()

        radius = pool_table_config.pool_table_pocket_radius
        
        #top left
        position = (0, 0)
        pocket = PoolTablePocket(position, radius)
        pocket_group.add(pocket)

        #top mid
        position = (table_rect.width/2, -radius/2)
        pocket = PoolTablePocket(position, radius)
        pocket_group.add(pocket)

        #top right
        position = (table_rect.width, 0)
        pocket = PoolTablePocket(position, radius)
        pocket_group.add(pocket)

        #bottom right
        position = (table_rect.width, table_rect.height)
        pocket = PoolTablePocket(position, radius)
        pocket_group.add(pocket)

        #bottom mid
        position = (table_rect.width/2, table_rect.height + (radius/2))
        pocket = PoolTablePocket(position, radius)
        pocket_group.add(pocket)

        #bottom left
        position = (0, table_rect.height)
        pocket = PoolTablePocket(position, radius)
        pocket_group.add(pocket)

        return pocket_group

    def construct_billiards_decals(self, table_rect: pygame.Rect):
        decals = pygame.sprite.Group()

        media = pool_table_config.pool_table_chalk_line_DM_RICH_media
        chalk_line_orig_image = media_manager.get(media, convert_alpha=True)
        chalk_line_orig_rect = chalk_line_orig_image.get_rect()
        if not chalk_line_orig_image:
            print('No chalk line img', media)
        else:
            size = (chalk_line_orig_rect.width, table_rect.height)
            position = (table_rect.width/5, table_rect.height/2)
            decal = Decal(chalk_line_orig_image, size, position, use_aspect_scale=True)
            decals.add(decal)

        # Chalk Dots
        media = pool_table_config.pool_table_chalk_dot_DM_RICH_media
        chalk_dot_orig_image = media_manager.get(media, convert_alpha=True)
        if not chalk_dot_orig_image:
            print('No chalk dot img', media)
        else:
            position = (table_rect.width - table_rect.width/4, table_rect.height/2)
            decal = Decal(chalk_dot_orig_image, size, position, use_aspect_scale=True)
            decals.add(decal)
        
            position = (table_rect.width/5, table_rect.height/2)
            decal = Decal(chalk_dot_orig_image, size, position, use_aspect_scale=True)
            decals.add(decal)

        return decals
    
    def construct_scuff_and_scratch_decals(self, table_rect: pygame.Rect):
        decals = pygame.sprite.Group()

        decal_media_list = [
            ['spr_Decal_Scratches3.png', 255], 
            ['spr_Decal_Scuff2.png', 200], 
            ['spr_Decal_Scratches1.png', 255], 
            ['spr_Decal_Scratches1.png', 255], 
            ['spr_Decal_Scratches2.png', 255], 
            ['spr_Decal_Scratches2.png', 255], 
            ['spr_Decal_Scratches3.png', 255], 
            ['spr_Decal_Scuff1.png', 200], 
            ['spr_Decal_Scratches2.png', 255], 
        ]

        bleed = 10
        for file_name, alpha in decal_media_list:
            media_path = f'table/decals/{file_name}'
            decal_image = media_manager.get(media_path, convert_alpha=True)
            decal_image.set_alpha(alpha)
            if not decal_image:
                print('No scuff decal img', media_path)
                continue

            rand_x = random.randint(bleed, table_rect.width - bleed)
            rand_y = random.randint(bleed, table_rect.height - bleed)
            position = (rand_x, rand_y)
            decal_rect = decal_image.get_rect(center=position)
            decal = Decal(decal_image, decal_rect.size, position, use_aspect_scale=True)
            decals.add(decal)

        return decals

    def construct_snooker_decals(self, table_rect: pygame.Rect):
        decals = pygame.sprite.Group()

        # start_pos = (table_rect.width/5, 0)
        # end_pos = (table_rect.width/5, table_rect.height)
        # table_third = (start_pos, end_pos)
        
        # Chalk Line
        media = pool_table_config.pool_table_chalk_line_DM_RICH_media
        chalk_line_image = media_manager.get(media, convert_alpha=True)
        chalk_line_rect = chalk_line_image.get_rect()
        if not chalk_line_image:
            print('No chalk line img', media)
        
        first_chalk_line_size = (chalk_line_rect.width, table_rect.height)
        first_chalk_line_position = (table_rect.width/5, table_rect.height/2)
        decal = Decal(chalk_line_image, first_chalk_line_size, first_chalk_line_position, use_aspect_scale=True)
        decals.add(decal)

        # Chalk D Line
        media = pool_table_config.pool_table_chalk_d_line_DM_RICH_media
        chalk_d_line_image = media_manager.get(media, convert_alpha=True)
        if not chalk_d_line_image:
            print('No chalk d line img', media)
        
        d_line_size = (100, table_rect.height/3 + 4)
        x_offset = 20
        d_line_position = (x_offset + first_chalk_line_position[0] - d_line_size[0]/2 + first_chalk_line_size[0]/2, table_rect.height/2)
        decal = Decal(chalk_d_line_image, d_line_size, d_line_position, use_aspect_scale=False)
        decals.add(decal)

        # Chalk Dots
        media = pool_table_config.pool_table_chalk_dot_DM_RICH_media
        chalk_dot_orig_image = media_manager.get(media, convert_alpha=True)
        if not chalk_dot_orig_image:
            print('No chalk dot img', media)
        else:
            radius = pool_table_config.pool_table_chalk_dot_radius
            chalk_dot_size = (radius*2, radius*2)
            center_y = table_rect.height/2
            first_line_x = first_chalk_line_position[0]

            # Green
            position = (first_line_x, table_rect.height/3)
            decal = Decal(chalk_dot_orig_image, chalk_dot_size, position, use_aspect_scale=True)
            decals.add(decal)

            # Brown
            position = (first_line_x, center_y)
            decal = Decal(chalk_dot_orig_image, chalk_dot_size, position, use_aspect_scale=True)
            decals.add(decal)

            # Yellow
            position = (first_line_x, table_rect.height - table_rect.height/3)
            decal = Decal(chalk_dot_orig_image, chalk_dot_size, position, use_aspect_scale=True)
            decals.add(decal)

            # Blue
            position = (table_rect.width/2, center_y)
            decal = Decal(chalk_dot_orig_image, chalk_dot_size, position, use_aspect_scale=True)
            decals.add(decal)

            # Pink
            position = (table_rect.width/2 + 120, center_y)
            decal = Decal(chalk_dot_orig_image, chalk_dot_size, position, use_aspect_scale=True)
            decals.add(decal)

            # Black
            position = (table_rect.width - 112, center_y)
            decal = Decal(chalk_dot_orig_image, chalk_dot_size, position, use_aspect_scale=True)
            decals.add(decal)

        return decals

    def construct_snooker_balls(self, table_rect: pygame.Rect):
        ball_group = pygame.sprite.Group()
        balls_config = pool_balls_config.snooker_ball_sets[self.active_ball_set_index]
        title, radius, media_folder, mass, elasticity, friction = balls_config

        color = pygame.Color('ivory')
        identifier = 'white'
        media_path = f'{media_folder}/{identifier}.png'
        position = (100, 170)
        cue_ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(cue_ball)

        color = pygame.Color('yellow')
        identifier = 'yellow'
        media_path = f'{media_folder}/{identifier}.png'
        position = (160, table_rect.height - table_rect.height/3)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)

        color = pygame.Color('brown')
        identifier = 'brown'
        media_path = f'{media_folder}/{identifier}.png'
        position = (160, table_rect.height/2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)

        color = pygame.Color('green')
        identifier = 'green'
        media_path = f'{media_folder}/{identifier}.png'
        position = (160, table_rect.height/3)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)

        color = pygame.Color('blue')
        identifier = 'blue'
        media_path = f'{media_folder}/{identifier}.png'
        position = (table_rect.width/2, table_rect.height/2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)

        color = pygame.Color('pink')
        identifier = 'pink'
        media_path = f'{media_folder}/{identifier}.png'
        position = ((table_rect.width/2) + 146 - radius*2, table_rect.height/2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)

        color = pygame.Color('red')
        identifier = 'red'
        media_path = f'{media_folder}/{identifier}.png'
        x_offset_from_pink = 6
        x_pos = position[0] + radius*2 + x_offset_from_pink
        y_pos = position[1]
        position = (x_pos, y_pos)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        x_pos += radius*2
        position = (x_pos, y_pos - radius)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        position = (x_pos, y_pos + radius)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        x_pos += radius*2
        position = (x_pos, y_pos)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        position = (x_pos, y_pos - radius*2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        position = (x_pos, y_pos + radius*2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        x_pos += radius*2
        position = (x_pos, y_pos - radius)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        position = (x_pos, y_pos - radius*3)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        position = (x_pos, y_pos + radius)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        position = (x_pos, y_pos + radius*3)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        x_pos += radius*2
        position = (x_pos, y_pos)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        position = (x_pos, y_pos - radius*2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        position = (x_pos, y_pos - radius*4)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        position = (x_pos, y_pos + radius*2)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)
        position = (x_pos, y_pos + radius*4)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)

        color = pygame.Color('black')
        identifier = 'black'
        media_path = f'{media_folder}/{identifier}.png'
        x_offset_from_reds = 6
        x_pos += radius*2 + x_offset_from_reds
        position = (x_pos, y_pos)
        ball = PoolBall(identifier, radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(ball)

        return cue_ball, ball_group

    def construct_snooker_game_table(self) -> SnookerGameTable:
        # Table
        size = pool_table_config.pool_table_size
        position = (self.rect.width/2, self.rect.height/2)
        space_config = self.game_session.game_mode_config.space_config
        draw_mode = DrawModeEnum.Rich
        game_table = SnookerGameTable(size, position, space_config, draw_mode)

        # Pockets
        pockets_group = self.construct_classic_table_pockets(game_table.rect)
        for i, pocket in enumerate(pockets_group):
            game_table.add_pocket(pocket)
        
        # Cushions
        cushions_group = self.construct_classic_table_cushions(game_table.rect)
        for i, cushion in enumerate(cushions_group):
            game_table.add_cushion(cushion)

        # Decals
        decal_group = self.construct_snooker_decals(game_table.rect)
        game_table.add_decals(decal_group)

        # Random Scuff Mark Decals
        decal_group = self.construct_scuff_and_scratch_decals(game_table.rect)
        game_table.add_decals(decal_group)
        

        # Balls
        cue_ball, ball_group = self.construct_snooker_balls(game_table.rect)

        game_table.clear_balls()
        for i, ball in enumerate(ball_group):
            game_table.add_ball(ball, ball_is_in_play=True)
            
        game_table.set_cue_ball_in_play(cue_ball)

        return game_table

    def construct_custom_circle_game_table(self) -> CircleGameTable:
        # Table
        radius = 300
        position = (self.rect.width/2, self.rect.height/2)
        space_config = self.game_session.game_mode_config.space_config
        draw_mode = DrawModeEnum.Rich
        game_table = CircleGameTable(radius, position, space_config, draw_mode)

        # Random Scuff Mark Decals
        decal_group = self.construct_scuff_and_scratch_decals(game_table.rect)
        game_table.add_decals(decal_group)

        # Pockets
        pocket_group = pygame.sprite.Group()
        radius = 32

        # center
        center_position = (game_table.rect.width/2, game_table.rect.height/2)
        center_pocket = PoolTablePocket(center_position, radius)
        pocket_group.add(center_pocket)
        
        for i, pocket in enumerate(pocket_group):
            game_table.add_pocket(pocket)
                
        # Balls
        ball_group = pygame.sprite.Group()
        balls_config = pool_balls_config.snooker_ball_sets[0]
        ball_set_title, ball_radius, media_folder, mass, elasticity, friction = balls_config

        color = pygame.Color('ivory')
        identifier = 'white'
        media_path = f'{media_folder}/{identifier}.png'
        position = (game_table.rect.width/2, 100)
        cue_ball = PoolBall(identifier, ball_radius, mass, elasticity, friction, position, color, media_path)
        ball_group.add(cue_ball)

        # Black balls
        color = pygame.Color('black')
        identifier = 'black'
        media_path = f'{media_folder}/{identifier}.png'
        positions = [
            (center_position[0], center_position[1] + center_pocket.rect.height),
            (center_position[0], center_position[1] - center_pocket.rect.height),
            (center_position[0] + center_pocket.rect.width, center_position[1]),
            (center_position[0] - center_pocket.rect.width, center_position[1]),
            (center_position[0] + center_pocket.rect.width - ball_radius*2, center_position[1] - center_pocket.rect.height + ball_radius*2),
            (center_position[0] + center_pocket.rect.width - ball_radius*2, center_position[1] + center_pocket.rect.height - ball_radius*2),
            (center_position[0] - center_pocket.rect.width + ball_radius*2, center_position[1] - center_pocket.rect.height + ball_radius*2),
            (center_position[0] - center_pocket.rect.width + ball_radius*2, center_position[1] + center_pocket.rect.height - ball_radius*2),
        ]

        for position in positions:
            ball = PoolBall(identifier, ball_radius, mass, elasticity, friction, position, color, media_path)
            ball_group.add(ball)

        # Red balls
        color = pygame.Color('red')
        identifier = 'red'
        media_path = f'{media_folder}/{identifier}.png'
        base_position = (center_position[0], game_table.rect.height - 60)
        positions = [
            base_position,
            (base_position[0] - ball_radius*2, base_position[1] - ball_radius),
            (base_position[0] - ball_radius*4, base_position[1] - ball_radius*2),
            (base_position[0] - ball_radius*6, base_position[1] - ball_radius*3),
            (base_position[0] - ball_radius*8, base_position[1] - ball_radius*4),
            (base_position[0] - ball_radius*10, base_position[1] - ball_radius*5),
            (base_position[0] + ball_radius*2, base_position[1] - ball_radius),
            (base_position[0] + ball_radius*4, base_position[1] - ball_radius*2),
            (base_position[0] + ball_radius*6, base_position[1] - ball_radius*3),
            (base_position[0] + ball_radius*8, base_position[1] - ball_radius*4),
            (base_position[0] + ball_radius*10, base_position[1] - ball_radius*5),
        ]

        for position in positions:
            ball = PoolBall(identifier, ball_radius, mass, elasticity, friction, position, color, media_path)
            ball_group.add(ball)


        game_table.clear_balls()
        for i, ball in enumerate(ball_group):
            game_table.add_ball(ball, ball_is_in_play=True)

        game_table.set_cue_ball_in_play(cue_ball)
        
        return game_table

    def construct_billiards_game_table(self) -> BilliardsGameTable:
        # size = pool_table_config.pool_table_size
        size =  (820, 400)
        position = (self.rect.width/2, self.rect.height/2)
        space_config = self.game_session.game_mode_config.space_config
        draw_mode = DrawModeEnum.Rich
        game_table = BilliardsGameTable(size, position, space_config, draw_mode)

        # Pockets
        pockets_group = self.construct_classic_table_pockets(game_table.rect)
        for i, pocket in enumerate(pockets_group):
            game_table.add_pocket(pocket)
        
        # Cushions
        cushions_group = self.construct_classic_table_cushions(game_table.rect)
        for i, cushion in enumerate(cushions_group):
            game_table.add_cushion(cushion)

        # Decals
        decals_group = self.construct_billiards_decals(game_table.rect)
        game_table.add_decals(decals_group)

        # Random Scuff Mark Decals
        decal_group = self.construct_scuff_and_scratch_decals(game_table.rect)
        game_table.add_decals(decal_group)

        # Balls
        cue_ball, ball_group = self.construct_billiards_balls(game_table.rect)
        
        game_table.clear_balls()
        for i, ball in enumerate(ball_group):
            game_table.add_ball(ball, ball_is_in_play=True)

        game_table.set_cue_ball_in_play(cue_ball)

        return game_table

    def construct_game_table(self):
        if self.game_session is None or self.game_session.game_mode is GameModeEnum.NONE:
            print('CANT SETUP POOL TABLE: NO GAMESESSION SET')
            return

        if self.game_session.game_table is not None:
            self.game_session.game_table = self.game_session.game_table.kill()

        game_table: GameTable = None
        if self.game_session.game_mode == GameModeEnum.Billiards:
            game_table = self.construct_billiards_game_table()
        elif self.game_session.game_mode == GameModeEnum.Snooker:
            game_table = self.construct_snooker_game_table()
        elif self.game_session.game_mode == GameModeEnum.CirclePool:
            game_table = self.construct_custom_circle_game_table()

        if game_table:
            game_table.add_light_source(self.light_source)
            self.game_session.game_table = game_table

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
        
        self.general_light_dim_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

    def setup_floor(self):
        self.floor = Floor(self.rect.size, self.rect.center)
        self.floor.on_init()

    def setup_ball_gutter(self):
        if self.game_session is None or self.game_session.game_mode in GameModeEnum.NONE:
            print('CANT SETUP POOL BALL GUTTER: NO GAMESESSION SET')
            return
        
        if self.pool_ball_gutter is not None:
            self.pool_ball_gutter = self.pool_ball_gutter.kill()

        size = pool_ball_gutter_config.pool_ball_gutter_size
        x_buffer = 0
        y_buffer = 40

        rect = self.rect
        if self.game_session and self.game_session.game_table:
            rect = self.game_session.game_table.rect
        position = (rect.right - size[0]/2 - x_buffer, rect.bottom + size[1]/2 + y_buffer)
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

        # TODO: Move to Game Session
        # Player takes a shot
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if not self.ui_layer.is_hovered and not self.cue_power_bar.is_hovered:
                if self.game_session.game_table.check_cue_ball_is_available() and not self.balls_are_in_motion:
                    self.take_player_shot()

        self.game_session.game_table.on_event(event)

    def take_player_shot(self):
        self.apply_force_to_ball(self.game_session.game_table.cue_ball)
        self.balls_are_in_motion = True
        self.active_player.is_taking_shot = True

    def apply_force_to_ball(self, ball: PoolBall):
        dx = self.mouse_position[0] - (self.game_session.game_table.rect.x + ball.position[0])
        dy = self.mouse_position[1] - (self.game_session.game_table.rect.y + ball.position[1])
        # distance = math.sqrt(dx*dx + dy*dy)
        angle = math.atan2(dy, dx)
        
        force_magnitude = self.cue_power_bar.power
        force_x = force_magnitude * math.cos(angle - ball.angle)
        force_y = force_magnitude * math.sin(angle - ball.angle)
        force = (force_x, force_y)

        max_volume = 0.3    #HACK: For quietening my cheap sounds
        volume = self.cue_power_bar.power_percent * max_volume
        ball.on_cue_hit(force, volume)

    def change_random_ball_size(self):
        balls = []
        for ball in self.game_session.game_table.ball_group:
            ball: PoolBall
            if ball.is_in_active_play:
                balls.append(ball)

        radius = random.randint(0, 50)
        ball_idx = random.randint(0, len(balls)-1)
        ball = balls[ball_idx]
        ball.set_radius(radius)
        self.game_session.game_table.update_ball(ball)

        print('changing ball size', ball.identifier, radius)

    # TODO: PLACE GAME EVENT SENSORS ON TABLE
    # TODO: DISPLAY UPCOMING QUEUED GAME EVENTS

    def change_random_ball_mass(self):
        balls = []
        for ball in self.game_session.game_table.ball_group:
            ball: PoolBall
            if ball.is_in_active_play:
                balls.append(ball)

        mass = random.uniform(0, 50)
        ball_idx = random.randint(0, len(balls)-1)
        ball = balls[ball_idx]
        ball.set_mass(mass)
        self.game_session.game_table.update_ball(ball)

        print('changing ball mass', ball.identifier, mass)

    def spawn_random_hole(self):
        radius = random.uniform(10, 60)
        rand_x = random.uniform(radius/2, self.game_session.game_table.rect.width - radius/2)
        rand_y = random.uniform(radius/2, self.game_session.game_table.rect.height - radius/2)
        position = (rand_x, rand_y)
        hole = PoolTablePocket(position, radius)
        self.game_session.game_table.add_pocket(hole)

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

        game_table = self.game_session.game_table

        if len(self.game_session.game_events_to_action) > 0:
            self.action_game_events()

        self.players_gui.update()
        self.ui_layer.update(self.game_session.game_mode)
        self.cue_power_bar.update()
        self.light_source.update(self.ui_layer.light_options, self.mouse_position)
        
        if not game_table:
            return
        
        game_table.update(self.game_session.time_lapsed, self.active_player.can_take_shot, self.light_source)
        
        # for camera_screen in self.camera_screens:
        #     camera_screen.update(self.surface)

        self.balls_are_in_motion = game_table.check_balls_are_moving()

        if game_table.cue_ball_first_hit_ball is not None and self.active_player.is_taking_shot:
            self.active_player.first_contact = game_table.cue_ball_first_hit_ball

        if len(game_table.balls_potted) > 0: # Balls potted
            for ball in game_table.balls_potted:
                ball: PoolBall
                ball.stop_moving()

                self.active_player.add_potted_ball(ball)
                game_table.remove_ball(ball)
                self.pool_ball_gutter.add_ball(ball)
            
            game_table.balls_potted = []

        self.pool_ball_gutter.update()
        
        cue_ball = game_table.cue_ball
        if not self.balls_are_in_motion and cue_ball:
            if not cue_ball.is_in_active_play and not cue_ball.is_picked_up and self.cue_ball_reset_ttl is None:
                self.cue_ball_reset_ttl = time_lapsed + self.cue_ball_out_of_play_time_to_reset

        if self.cue_ball_reset_ttl is not None and time_lapsed > self.cue_ball_reset_ttl:
            self.pool_ball_gutter.remove_ball(cue_ball)
            game_table.free_place_cue_ball(cue_ball)
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
                    game_table.cue_ball_first_hit_ball = None

        if self.ui_layer.queued_game_event is not InGameEventEnum.NONE:
            time_to_activate = 2 * 1000
            self.game_session.queue_game_event(self.ui_layer.queued_game_event, time_to_activate)
            self.ui_layer.queued_game_event = InGameEventEnum.NONE

    def check_potted_balls_are_player_friendly(self):
        disallowed_balls = [
            self.game_session.game_table.cue_ball
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
        self.cue_ball_reset_ttl = None

        self.construct_game_table()
        self.setup_ball_gutter()

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

        current_mouse_cursor = pygame.mouse.get_cursor()
        new_mouse_cursor = pygame.SYSTEM_CURSOR_ARROW

        mouse_cursor_checks = [
            self.game_lobby.hovered_component is not None,
            self.ui_layer.hovered_component is not None,
            self.cue_power_bar.is_hovered and not self.ui_layer.is_active,
            self.game_session is not None and self.game_session.has_picked_up_cue_ball()
        ]

        for check in mouse_cursor_checks:
            if check:
                new_mouse_cursor = pygame.SYSTEM_CURSOR_HAND
                break

        if new_mouse_cursor != current_mouse_cursor:
            pygame.mouse.set_cursor(new_mouse_cursor)

    def draw_running_game(self):
        self.floor.draw(self.surface)
        #TODO: Make this a game_sesson.draw
        self.game_session.game_table.draw(self.surface, self.light_source)
        self.pool_ball_gutter.draw(self.surface)
        self.cue_power_bar.draw(self.surface)

        self.general_light_dim_surface.fill((0,0,0,self.light_source.lumens))
        self.surface.blit(self.general_light_dim_surface, (0,0))

        self.light_source.draw(self.surface)
        # for camera_screen in self.camera_screens:
        #     camera_screen.draw(self.surface)
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
