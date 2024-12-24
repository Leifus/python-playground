from config import pygame
from classes.draw_mode_enum import DrawModeEnum

# ----------------------------------------------------
# POOL BALLS CONFIG
# ----------------------------------------------------

# Collision Types
COLLISION_TYPE_LINE_OF_SIGHT = 5
COLLISION_TYPE_CUE_BALL = 1000      # NOT USED YET
COLLISION_TYPE_POOL_BALL = 100
COLLISION_TYPE_POOL_TABLE_POCKET = 10
COLLISION_TYPE_POOL_TABLE_CUSHION = 50
COLLISION_TYPE_FLOATING_BALL = 0
# Ball
# pool_ball_radius = 12
# pool_ball_mass = 15
# pool_ball_elasticity = 0.9
# pool_ball_friction = 0.6
pool_ball_max_force = 1000000

pool_ball_draw_mode = DrawModeEnum.Rich  # PHYSICS is treated as WIREFRAME due to space inherited from the parent
pool_ball_DM_WIREFRAME_outline_width = 2

snooker_ball_sets = [
    [
        'Standard', # title/Label
        12,  # ball radius
        'balls/coloured_balls', # media folder
        5.5,     # ball mass
        0.75,    # ball elasticity
        0.2,     # ball friction
    ]
]

billiard_ball_sets = [
    [
        'Colours', # title/Label
        12,  # ball radius
        False,    # use ball identifer as media file name
        'balls/coloured_balls', # media folder
        6,     # ball mass
        0.8,    # ball elasticity
        0.2,     # ball friction
        (pygame.Color('ivory'), 'white.png'),      # cue ball
        (pygame.Color('black'), 'black.png'),      # 8 ball
        (pygame.Color('yellow2'), 'yellow.png'), # spot ball
        (pygame.Color('firebrick2'), 'red.png'),    # stripe ball
    ],
    [
        'Numbers', # title/Label
        13,  # ball radius
        True,    # use ball identifer as media file name
        'balls/numbered_balls', # media folder
        6,     # ball mass
        0.8,    # ball elasticity
        0.2,     # ball friction
        (pygame.Color('ivory'), None),      # cue ball
        (pygame.Color('black'), None),      # 8 ball
        (pygame.Color('yellow2'), None), # spot ball
        (pygame.Color('firebrick2'), None),    # stripe ball
    ]
]

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


# Sounds
sound_ball_collide_with_ball = 'ball_collide.mp3'