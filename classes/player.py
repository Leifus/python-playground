from classes.pool_ball import PoolBall
from config import pygame
from classes.game_sprite import GameSprite

class Player(GameSprite):
    def __init__(self, identifier, name):
        super(GameSprite, self).__init__()
        
        self.identifier = identifier
        self.name = name
        self.is_playing = False
        self.can_take_shot = False
        self.has_taken_shot = False
        self.has_faulted_shot = False
        self.balls_potted_this_shot = pygame.sprite.Group()
        self.balls_potted = pygame.sprite.Group()

    def add_potted_ball(self, ball: PoolBall):
        self.balls_potted_this_shot.add(ball)
        self.balls_potted.add(ball)

    def end_turn(self):
        self.is_playing = False
        self.can_take_shot = False
        self.has_taken_shot = False
        self.has_faulted_shot = False
        self.balls_potted_this_shot.empty()
        # print(f'{self.name}: {len(self.balls_potted)} balls potted')
        self.balls_potted.empty()