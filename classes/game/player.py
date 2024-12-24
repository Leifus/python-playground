from classes.game.pool_ball import PoolBall
from config import pygame
from classes.common.game_sprite import GameSprite

class Player(GameSprite):
    def __init__(self, identifier, name):
        super(Player, self).__init__()
        
        self.identifier = identifier
        self.name = name
        self.is_playing = False
        self.can_take_shot = False
        self.is_taking_shot = False
        self.has_faulted_shot = False
        self.balls_potted_this_shot = pygame.sprite.Group()
        self.balls_potted = pygame.sprite.Group()
        self.disallowed_balls = pygame.sprite.Group()
        self.first_contact = None

    def add_potted_ball(self, ball: PoolBall):
        self.balls_potted_this_shot.add(ball)
        self.balls_potted.add(ball)

    def end_shot(self):
        self.first_contact = None
        self.balls_potted_this_shot.empty()
        self.is_taking_shot = False
    
    def end_turn(self):
        print(f'{self.name}: {len(self.balls_potted)} balls potted, faulted={self.has_faulted_shot}')
        
        self.is_playing = False
        self.can_take_shot = False
        self.is_taking_shot = False
        self.has_faulted_shot = False
        self.first_contact = None
        self.balls_potted_this_shot.empty()
        self.balls_potted.empty()