from config import pygame, pool_balls_config
from classes.draw_mode import DrawMode

# ----------------------------------------------------
# POOL BALL GUTTER CONFIG
# ----------------------------------------------------

pool_ball_gutter_border_elasticity = 0.4
pool_ball_gutter_border_friction = 0.7
pool_ball_gutter_border_width = 8
pool_ball_gutter_size = (( pool_balls_config.pool_ball_radius*2) + (pool_ball_gutter_border_width*2) + 4, 400)
pool_ball_gutter_space_iterations = 10
pool_ball_gutter_space_gravity = (0, 980)
pool_ball_gutter_space_damping = 0.55
pool_ball_gutter_space_sleep_time_threshold = 0.1 #math.inf

pool_ball_gutter_draw_mode = DrawMode.RICH
pool_ball_gutter_DM_WIREFRAME_thickness = 2

# Rich Drawing
pool_ball_gutter_DM_RICH_media = 'UI/spr_UI_Powerbar_Overlay.png'
# pool_ball_gutter_DM_RICH_media = 'pool_ball_gutter/green_pipe.png'


# Raw & Wireframe Drawing
pool_ball_gutter_DM_RAW_color = pygame.Color('tan')
pool_ball_gutter_DM_RAW_border_color = pygame.Color('tan4')
