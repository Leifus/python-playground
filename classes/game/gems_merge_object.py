from classes.configs.sprite_animation_config import SpriteAnimationConfig
from classes.enums.gems_merge_object_color_enum import GemsMergeObjectColorEnum
from classes.enums.merge_object_size_enum import MergeObjectSizeEnum
from classes.game.merge_object import MergeObject
from config import Dict

class GemsMergeObject(MergeObject):
    def __init__(self, color: GemsMergeObjectColorEnum, size: MergeObjectSizeEnum):
        sprite_sheet_image_path = 'gems.png'
        current_animation = None
        color_key = ((0,0,0))
        animate = False

        self.color = color
        self.object_size = size

        self.sprite_config: Dict[str, SpriteAnimationConfig] = dict()
        self.setup_sprite_config()

        super(GemsMergeObject, self).__init__(sprite_sheet_image_path, self.sprite_config, current_animation, color_key, animate)

    def setup_sprite_config(self):
        self.setup_blue_gem_sprite_config()

    def setup_blue_gem_sprite_config(self):
        animation_steps = 1
        animation_speed = -1
        
        sprite_label = 'blue_large'
        sprite_position = (0,0)
        sprite_size = (64,64)
        blue_large_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        self.sprite_config[blue_large_config.label] = blue_large_config
