

from classes.common.sprite_sheet import SpriteSheet


class MergeObject(SpriteSheet):
    def __init__(self, sprite_sheet_image_path, animation_data, current_animation, color_key, animate):
        super(MergeObject, self).__init__(sprite_sheet_image_path, animation_data, current_animation, color_key, animate)

        