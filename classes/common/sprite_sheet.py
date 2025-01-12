from classes.common.game_sprite import GameSprite
from classes.configs.sprite_animation_config import SpriteAnimationConfig
from config import pygame, Dict
from globals import media_manager

class SpriteSheet(GameSprite):
    def __init__(self, sprite_sheet_image_path, animation_data: Dict[str, SpriteAnimationConfig], current_animation: SpriteAnimationConfig, color_key, animate):
        super( SpriteSheet, self).__init__()
        self.sprite_sheet_image_path = sprite_sheet_image_path

        self.orig_image = media_manager.get(self.sprite_sheet_image_path, convert=True)
        self.animation_data = animation_data
        self.current_animation_step = 0
        self.current_animation: SpriteAnimationConfig = current_animation
        self.color_key = color_key
        self.time_to_step_animation = None
        self.animate = animate
        self.animate_reverse_order = False

    def redraw(self):
        x, y = self.current_animation.position
        width, height = self.current_animation.size
        self.image = self.get_sprite_by_data(x, y, width, height, self.current_animation_step)
        self.image.set_colorkey(self.color_key)
        self.rect = self.image.get_rect()
        # pygame.draw.rect(self.image, 'blue', pygame.Rect(0, 0, self.rect.width, self.rect.height), 1)

    def set_animation_speed(self, speed, reverse_animation):
        if self.time_to_step_animation is not None:
            current_speed = self.current_animation.animation_speed

            if speed < current_speed:   #speed up timers
                self.time_to_step_animation -= current_speed - speed
            else:   #slow down timers
                self.time_to_step_animation += speed - current_speed

        self.current_animation.animation_speed = speed
        self.animate_reverse_order = reverse_animation
            
    def step_animation(self):
        if self.animate_reverse_order:
            self.current_animation_step -= 1
            if self.current_animation_step < 0:
                self.current_animation_step = self.current_animation.steps-1
        else:
            self.current_animation_step += 1
            if self.current_animation_step >= self.current_animation.steps:
                self.current_animation_step = 0


        self.redraw()

    def update(self, time_lapsed, *args, **kwargs):
        if self.animate:
            pass
            # if self.time_to_step_animation is None:
            #     self.time_to_step_animation = self.current_animation.animation_speed
            # else:
            #     self.time_to_step_animation -= time_lapsed 
            # elif time_lapsed > self.time_to_step_animation:
            #     self.time_to_step_animation = time_lapsed + self.current_animation.animation_speed
            #     self.step_animation()

        return super().update(*args, **kwargs)

    def get_sprite_by_data(self, x, y, width, height, step):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.orig_image, (0, 0), area=(x + (width * step), y, width, height))

        return image
    