import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import random
import math

COLLISION_TYPE_BALLOON_STRING = 4
COLLISION_TYPE_BALLOON = 3
COLLISION_TYPE_WIND = 2

class BalloonConfig():
    def __init__(self):
        self.base_gravity = -5
        self.base_gravity_radius_multiplier = 1.3
        self.base_mass = 2
        self.base_mass_radius_multiplier = 0.3
        self.elasticity = 0.6
        self.friction = 0.2
        self.alpha = 180

class BalloonStringConfig():
    def __init__(self):
        pass

class BoxWithLidConfig():
    def __init__(self):
        self.box_width = 350
        self.box_height = 300
        self.box_edge_thickness = 5
        self.box_alpha = 155
        self.lid_width = self.box_width + 10
        self.lid_height = 20
        self.lid_mass = 10

class WindSourceConfig():
    def __init__(self):
        # desk fan config
        # self.strength = 500
        # self.cone_length = 600
        # self.cone_angle = math.pi/4
        # self.height = 150
        # self.width = 150
        # self.position = (80, 290)
        # self.angle = 0

        # ceiling fan config
        self.strength = 50000
        self.cone_length = 350
        self.cone_angle = 2.5
        self.height = 70
        self.width = 70
        self.position = (500, 20)
        self.angle = 90

class PhysicsConfig():
    def __init__(self):
        self.space_iterations = 10
        self.space_gravity = (0, 981)
        self.space_damping = 0.7
        self.space_sleep_time_threshold = math.inf

class AppConfig():
    def __init__(self):
        self.debug_draw_pymunk_space = False
        self.fps = 60
        self.dt = 1.0 / self.fps
        self.dt_steps = 1
        self.window_size = (1080, 800)

        self.wall_thickness = 5
        self.wall_elasticity = 1
        self.wall_friction = 0.5

        self.balloon_count = 50
        self.balloon_min_radius = 8
        self.balloon_max_radius = 40


app_cfg = AppConfig()
phys_cfg = PhysicsConfig()
wind_cfg = WindSourceConfig()
box_cfg = BoxWithLidConfig()
balloonstring_cfg = BalloonStringConfig()
balloon_cfg = BalloonConfig()