from config import pygame, pool_balls_config
from classes.draw_mode_enum import DrawModeEnum

# ----------------------------------------------------
# POOL BALL GUTTER CONFIG
# ----------------------------------------------------

pool_ball_gutter_edge_barrier_elasticity = 0.4
pool_ball_gutter_edge_barrier_friction = 0.99
pool_ball_gutter_edge_barrier_width = 8
pool_ball_gutter_size = (400,( 15*2) + (pool_ball_gutter_edge_barrier_width*2) + 2)
pool_ball_gutter_space_iterations = 10
pool_ball_gutter_space_gravity = (780, 980)
pool_ball_gutter_space_damping = 0.98
pool_ball_gutter_space_sleep_time_threshold = 0.1 #math.inf

pool_ball_gutter_draw_mode = DrawModeEnum.Rich
pool_ball_gutter_DM_WIREFRAME_outline_width = 3
pool_ball_gutter_DM_WIREFRAME_poly_point_radius = 2

# Rich Drawing
# pool_ball_gutter_DM_RICH_media = 'UI/spr_UI_Powerbar_Overlay.png'
pool_ball_gutter_DM_RICH_media = 'SBS - Tiny Texture Pack 2 - 512x512/512x512/Metal/Metal_06-512x512.png'


# Raw & Wireframe Drawing
pool_ball_gutter_DM_RAW_color = pygame.Color('tan')
pool_ball_gutter_edge_barrier_DM_RAW_color = pygame.Color('tan4')
