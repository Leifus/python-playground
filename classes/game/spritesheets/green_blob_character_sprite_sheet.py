from classes.common.sprite_sheet import SpriteSheet
from classes.configs.sprite_animation_config import SpriteAnimationConfig
from config import Dict

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
        
        current_animation = anim_3
        color_key = (157, 142, 135)
        animate = True
        
        super( GreenBlobCharacterSpriteSheet, self).__init__(sprite_sheet_image_path, animation_data, current_animation, color_key, animate)

        self.position = position

        self.redraw()
