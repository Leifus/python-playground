from config import pygame
from classes.draw_mode import DrawMode


# ----------------------------------------------------
# POOL TABLE CONFIG
# ----------------------------------------------------

# Main Table
pool_table_size = (800, 400)
pool_table_space_iterations = 10
pool_table_space_gravity = (0, 0)
pool_table_space_damping = 0.55
pool_table_space_sleep_time_threshold = 0.1 #math.inf
pool_table_draw_mode = DrawMode.RICH
pool_table_draw_mode_wireframe_thickness = 2
pool_table_DM_RICH_media = 'table/green_fabric.jpg'
pool_table_DM_RAW_color = pygame.Color('darkgreen')


# Pockets
pool_table_pocket_color = pygame.Color('gray20')
pool_table_pocket_radius = 25
pool_table_corner_pocket_radius = pool_table_pocket_radius


# Cushions
pool_table_cushion_thickness = 10
pool_table_cushion_gap_to_pocket = 4
pool_table_cushion_bezel_short = pool_table_cushion_thickness - 5
pool_table_cushion_bezel_long = pool_table_cushion_thickness + 5
pool_table_cushion_elasticity = 0.9
pool_table_cushion_friction = 0.8
pool_table_cushion_draw_mode = DrawMode.RAW
pool_table_cushion_draw_mode_wireframe_thickness = 3
pool_table_cushion_DM_RICH_media = 'floor/floor_wood.png'
pool_table_cushion_DM_RAW_color = pygame.Color('chartreuse4')


# Chalk Lines
pool_table_chalk_line_color = pygame.Color('green4')
pool_table_chalk_line_width = 2


# Chalk Dots
pool_table_chalk_dot_color = pygame.Color('grey25')
pool_table_chalk_dot_radius = 3

