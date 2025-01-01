from classes.common.game_sprite import GameSprite
from config import pygame, Dict
from globals import media_manager

class SpriteAnimationConfig():
    def __init__(self, label, position, size, steps, animation_speed):
        self.label = label
        self.position = position
        self.size = size
        self.steps = steps
        self.animation_speed = animation_speed

class SpriteSheet(GameSprite):
    def __init__(self, sprite_sheet_image_path, animation_data: Dict[str, SpriteAnimationConfig], current_animation: SpriteAnimationConfig, color_key, scale, animate):
        super( SpriteSheet, self).__init__()
        self.sprite_sheet_image_path = sprite_sheet_image_path

        self.orig_image = media_manager.get(self.sprite_sheet_image_path, convert=True)
        self.animation_data = animation_data
        self.current_animation_step = 0
        self.current_animation: SpriteAnimationConfig = current_animation
        self.color_key = color_key
        self.anim_update_ttl = 0
        self.scale = scale
        self.animate = animate

    def redraw(self):
        x, y = self.current_animation.position
        width, height = self.current_animation.size
        self.image = self.get_sprite(x, y, width, height, self.current_animation_step, self.scale)
        self.image.set_colorkey(self.color_key)
        self.rect = self.image.get_rect(center=self.position)

    def step_animation(self, time_lapsed):
        self.anim_update_ttl = time_lapsed + self.current_animation.animation_speed
        self.current_animation_step += 1
        if self.current_animation_step >= self.current_animation.steps:
            self.current_animation_step = 0

        self.redraw()

    def update(self, time_lapsed, *args, **kwargs):
        if self.animate and time_lapsed > self.anim_update_ttl:
            self.step_animation(time_lapsed)

        return super().update(*args, **kwargs)

    def get_sprite(self, x, y, width, height, step, scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.orig_image, (0, 0), area=(x + (width * step), y, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))

        return image
    

class GreenBlobCharacterSpriteSheet(SpriteSheet):
    def __init__(self, position):
        sprite_sheet_image_path = 'other/character_sprite_sheet_1.png'
        animation_data: Dict[str, SpriteAnimationConfig] = dict()

        anim_1 = SpriteAnimationConfig('green_blob_idle', (16,16), (16,16), 2, 100)
        animation_data[anim_1.label] = anim_1
        anim_2 = SpriteAnimationConfig('green_blob_move', (16,16), (16,16), 3, 100)
        animation_data[anim_2.label] = anim_2
        anim_3 = SpriteAnimationConfig('green_blob_jump', (64,16), (16,16), 3, 100)
        animation_data[anim_3.label] = anim_3
        
        scale = 4.0
        current_animation = anim_1
        color_key = (157, 142, 135)
        animate = True
        
        super( GreenBlobCharacterSpriteSheet, self).__init__(sprite_sheet_image_path, animation_data, current_animation, color_key, scale, animate)

        self.position = position

        self.redraw()