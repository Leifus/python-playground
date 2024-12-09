import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import random
import math

# ----------------------------
# :: MAIN CONFIG ::
# ----------------------------
# Physics Config
space_iterations = 10
space_gravity = (0, 0)
space_damping = 0.48
space_sleep_time_threshold = 0.1 #math.inf
space_debug_draw = False

# Time Config
time_fps = 60
time_dt = 1.0 / 30
time_dt_steps = 2

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
pool_table_pocket_radius = 30
pool_table_corner_pocket_radius = pool_table_pocket_radius * 1.5

pool_table_cushion_thickness = 20
pool_table_cushion_elasticity = 0.6
pool_table_cushion_friction = 0.8

pool_ball_radius = 12
pool_ball_mass = 10
pool_ball_elasticity = 0.9
pool_ball_friction = 0.8
pool_ball_max_force = 500000

pool_ball_cue_color = pygame.Color('white')
pool_ball_8_color = pygame.Color('black')
pool_ball_spot_color = pygame.Color('blue')
pool_ball_stripe_color = pygame.Color('green')