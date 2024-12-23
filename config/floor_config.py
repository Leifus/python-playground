from config import pygame
from classes.draw_mode_enum import DrawModeEnum

# ----------------------------------------------------
# FLOOR CONFIG
# ----------------------------------------------------

floor_draw_mode = DrawModeEnum.Rich
floor_DM_WIREFRAME_thickness = 5
floor_DM_WIREFRAME_poly_point_radius = 5
floor_DM_active_idx = 0
floor_DM_RICH_medias = [    #path, scale
    ['floor/floor_carpet.png', 0.4],
    ['floor/floor_tile.png', 0.5],
    ['floor/floor_wood.png', 0.6],
    ['floor/space_bg.jpg', 0.3]
]
floor_DM_RAW_colors = [
    pygame.Color('black'),
    pygame.Color('blue'),
    pygame.Color('pink'),
    pygame.Color('brown'),
    pygame.Color('turquoise'),
    pygame.Color('violetred'),
    pygame.Color('wheat'),
    pygame.Color('yellow2'),
    pygame.Color('salmon'),
    pygame.Color('seagreen1'),
    pygame.Color('mediumpurple2'),
    pygame.Color('indigo'),
]
