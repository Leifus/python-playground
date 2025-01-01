from classes.common.sprite_sheet import SpriteSheet
from classes.configs.sprite_animation_config import SpriteAnimationConfig
from config import Dict

class RedBlobCharacterSpriteSheet(SpriteSheet):
    def __init__(self, position):
        sprite_sheet_image_path = 'other/character_sprite_sheet_1.png'
        animation_data: Dict[str, SpriteAnimationConfig] = dict()

        anim_1 = SpriteAnimationConfig('red_blob_blobbing', (16,80), (16,16), 5, 80)
        animation_data[anim_1.label] = anim_1
        
        current_animation = anim_1
        color_key = (157, 142, 135)
        animate = True
        
        super( RedBlobCharacterSpriteSheet, self).__init__(sprite_sheet_image_path, animation_data, current_animation, color_key, animate)

        self.position = position

        self.redraw()