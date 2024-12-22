import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import random
import math
import os
from typing import Dict

from config import pool_balls_config


# ----------------------------
# :: MAIN CONFIG ::
# ----------------------------


# Display Config
display_size = (1400, 800)
display_flags = DOUBLEBUF
display_depth = 32
display_bg_color = pygame.Color('gray75')

media_root_path = 'media'
sounds_root_path = 'sounds'
