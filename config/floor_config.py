from config import pygame
from classes.draw_mode import DrawMode

# ----------------------------------------------------
# FLOOR CONFIG
# ----------------------------------------------------

floor_draw_mode = DrawMode.RICH
floor_DM_RAW_color = pygame.Color('lightblue')
floor_DM_WIREFRAME_thickness = 5
floor_DM_WIREFRAME_poly_point_radius = 5
# floor_tile_DM_RICH_media = 'floor/floor_carpet.png'
# floor_tile_DM_RICH_scale = 0.2

floor_active_idx = 0
floor_DM_RICH_medias = [    #path, scale
    ['floor/floor_carpet.png', 0.4],
    ['floor/floor_tile.png', 0.5],
    ['floor/floor_wood.png', 0.6],
    ['floor/space_bg.jpg', 0.3]
]
