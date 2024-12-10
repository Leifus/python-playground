import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import random
import math

# ----------------------------
# :: MAIN CONFIG ::
# ----------------------------

# Time Config
time_fps = 60
time_dt = 1.0 / 60
time_dt_steps = 1

# Display Config
display_size = (1400, 800)
display_flags = DOUBLEBUF
display_depth = 32
display_bg_color = pygame.Color('gray75')


# Collision Types
COLLISION_TYPE_POOL_BALL = 100
COLLISION_TYPE_POOL_TABLE_POCKET = 10
COLLISION_TYPE_POOL_TABLE_CUSHION = 50


# ----------------------------
# :: GAME CONFIG ::
# ----------------------------

pool_table_size = (800, 400)
pool_table_color = pygame.Color('darkgreen')
pool_table_space_iterations = 10
pool_table_space_gravity = (0, 0)
pool_table_space_damping = 0.55
pool_table_space_sleep_time_threshold = 0.1 #math.inf
pool_table_space_debug_draw = False

pool_ball_radius = 12
pool_ball_mass = 15
pool_ball_elasticity = 0.9
pool_ball_friction = 0.6
pool_ball_max_force = 1000000
pool_ball_cue_color = pygame.Color('ivory')
pool_ball_8_color = pygame.Color('black')
pool_ball_spot_color = pygame.Color('orangered3')
pool_ball_stripe_color = pygame.Color('yellow2')

pool_ball_gutter_color = pygame.Color('tan')
pool_ball_gutter_border_color = pygame.Color('tan4')
pool_ball_gutter_border_elasticity = 0.4
pool_ball_gutter_border_friction = 0.7
pool_ball_gutter_border_width = 6
pool_ball_gutter_border_width = 6
pool_ball_gutter_size = ((pool_ball_radius*2) + (pool_ball_gutter_border_width*2) + 4, pool_table_size[1])
pool_ball_gutter_space_iterations = 10
pool_ball_gutter_space_gravity = (0, 980)
pool_ball_gutter_space_damping = 0.55
pool_ball_gutter_space_sleep_time_threshold = 0.1 #math.inf
pool_ball_gutter_space_debug_draw = False

pool_table_pocket_color = pygame.Color('gray20')
pool_table_pocket_radius = 25
pool_table_corner_pocket_radius = pool_table_pocket_radius

pool_table_cushion_color = pygame.Color('chartreuse4')
pool_table_cushion_thickness = 10
pool_table_cushion_gap_to_pocket = 8
pool_table_cushion_bezel_short = pool_table_cushion_thickness/2
pool_table_cushion_bezel_long = pool_table_cushion_thickness
pool_table_cushion_elasticity = 0.7
pool_table_cushion_friction = 0.8