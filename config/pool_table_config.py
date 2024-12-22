from config import pygame, math
from classes.draw_mode_enum import DrawModeEnum


# ----------------------------------------------------
# POOL TABLE CONFIG
# ----------------------------------------------------

# Main Table
pool_table_size = (800, 400)
pool_table_draw_mode = DrawModeEnum.RICH
pool_table_DM_WIREFRAME_outline_width = 2
pool_table_DM_WIREFRAME_poly_point_radius = 3
pool_table_DM_RICH_media = 'table/green_fabric.jpg'
pool_table_DM_RAW_color = pygame.Color('darkgreen')


# Pockets
pool_table_pocket_radius = 32
pool_table_pocket_draw_mode = DrawModeEnum.RICH
pool_table_pocket_DM_RICH_media = 'UI/spr_UI_Ball_Slot.png'
pool_table_pocket_DM_RAW_color = pygame.Color('gray2')
pool_table_pocket_DM_WIREFRAME_outline_width = 2


# Cushions
pool_table_cushion_thickness = 10
pool_table_cushion_gap_to_pocket = 3
pool_table_cushion_bezel_short = 3
pool_table_cushion_bezel_long = 10
pool_table_cushion_elasticity = 0.7
pool_table_cushion_friction = 0.8
pool_table_cushion_draw_mode = DrawModeEnum.RICH
pool_table_cushion_DM_WIREFRAME_outline_width = 3
pool_table_cushion_DM_WIREFRAME_poly_point_radius = 2
pool_table_cushion_DM_RICH_media = 'SBS - Tiny Texture Pack 2 - 512x512/512x512/Plaster/Plaster_12-512x512.png'
pool_table_cushion_DM_RAW_color = pygame.Color('chartreuse3')


# Chalk Lines
pool_table_chalk_line_DM_RICH_media = 'table/decals/spr_Decal_Line.png'
pool_table_chalk_line_DM_RAW_color = pygame.Color('green4')
pool_table_chalk_line_width = 2


# Chalk Dots
pool_table_chalk_dot_DM_RICH_media = 'table/decals/spr_Decal_Blackspot.png'
pool_table_chalk_dot_DM_RAW_color = pygame.Color('gray25')
pool_table_chalk_dot_radius = 4

