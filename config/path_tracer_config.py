from config import pygame
from classes.draw_mode import DrawMode

# ----------------------------------------------------
# PATH TRACER CONFIG
# ----------------------------------------------------

path_tracer_point_radius = 4
path_tracer_draw_mode = DrawMode.RICH

path_tracer_DM_WIREFRAME_outline_width = 2
path_tracer_line_DM_RAW_width = 2

path_tracer_point_a_DM_RICH_media = 'UI/spr_UI_Ball_Spin_Circle.png'
path_tracer_point_b_DM_RICH_media = 'UI/spr_UI_Ball_Spin_Circle.png'

path_tracer_point_a_DM_RAW_color = pygame.Color('red')
path_tracer_point_b_DM_RAW_color = pygame.Color('red')
path_tracer_line_DM_RAW_color = pygame.Color('black')