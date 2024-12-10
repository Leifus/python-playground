from config import pygame, pool_balls_config

# ----------------------------------------------------
# POOL BALL GUTTER CONFIG
# ----------------------------------------------------

pool_ball_gutter_color = pygame.Color('tan')
pool_ball_gutter_border_color = pygame.Color('tan4')
pool_ball_gutter_border_elasticity = 0.4
pool_ball_gutter_border_friction = 0.7
pool_ball_gutter_border_width = 6
pool_ball_gutter_border_width = 6
pool_ball_gutter_size = (( pool_balls_config.pool_ball_radius*2) + (pool_ball_gutter_border_width*2) + 4, 400)
pool_ball_gutter_space_iterations = 10
pool_ball_gutter_space_gravity = (0, 980)
pool_ball_gutter_space_damping = 0.55
pool_ball_gutter_space_sleep_time_threshold = 0.1 #math.inf
pool_ball_gutter_space_debug_draw = False
