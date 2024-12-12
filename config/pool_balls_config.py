from config import pygame
from classes.draw_mode import DrawMode

# ----------------------------------------------------
# POOL BALLS CONFIG
# ----------------------------------------------------

# Collision Types
COLLISION_TYPE_POOL_BALL = 100
COLLISION_TYPE_POOL_TABLE_POCKET = 10
COLLISION_TYPE_POOL_TABLE_CUSHION = 50

# Ball
pool_ball_radius = 12
pool_ball_mass = 15
pool_ball_elasticity = 0.9
pool_ball_friction = 0.6
pool_ball_max_force = 1000000

pool_ball_draw_mode = DrawMode.RICH  # PHYSICS is treated as WIREFRAME due to space inherited from the parent
pool_ball_DM_WIREFRAME_outline_width = 2

# Rich Drawing
pool_ball_DM_RICH_use_identifer_as_media = True
pool_ball_DM_RICH_media_path = 'balls/Numbered_balls'
# pool_ball_DM_RICH_use_identifer_as_media = False
# pool_ball_DM_RICH_media_path = 'balls/Billiard_Balls_01'

# When pool_ball_DM_RICH_use_identifer_as_media = False
pool_ball_DM_RICH_cue_media_path = 'white.png'
pool_ball_DM_RICH_8_media_path = 'black.png'
pool_ball_DM_RICH_spot_media_path = 'yellow.png'
pool_ball_DM_RICH_stripe_media_path = 'red.png'

# Raw & Wireframe Drawing
pool_ball_DM_RAW_cue_color = pygame.Color('ivory')
pool_ball_DM_RAW_8_color = pygame.Color('black')
pool_ball_DM_RAW_spot_color = pygame.Color('orangered3')
pool_ball_DM_RAW_stripe_color = pygame.Color('yellow2')
