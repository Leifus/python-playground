from classes.configs.sprite_animation_config import SpriteAnimationConfig
from classes.enums.gems_merge_object_color_enum import GemsMergeObjectColorEnum
from classes.enums.merge_object_size_enum import MergeObjectSizeEnum
from classes.game.merge_object import MergeObject
from config import Dict

class GemsMergeObject(MergeObject):
    def __init__(self, color: GemsMergeObjectColorEnum, size: MergeObjectSizeEnum):
        sprite_sheet_image_path = 'gems.png'
        color_key = ((0,0,0))

        self.color = color
        self.sprite_config: Dict[str, SpriteAnimationConfig] = dict()
        self.setup_sprite_config()

        current_animation = self.sprite_config.get(f'{color.name}_{size.name}')
        collision_type = (color.value * 100) + size.value
        super(GemsMergeObject, self).__init__(collision_type, size, sprite_sheet_image_path, self.sprite_config, current_animation, color_key)
    
        self.label = f'{self.color.name}_{self.object_size.name}'

    def setup_sprite_config(self):
        self.setup_blue_gem_sprite_config()
        self.setup_yellow_green_gem_sprite_config()
        self.setup_black_gem_sprite_config()
        self.setup_red_gem_sprite_config()
        self.setup_green_gem_sprite_config()
        self.setup_white_gem_sprite_config()
        self.setup_violet_gem_sprite_config()

    def setup_blue_gem_sprite_config(self):
        animation_steps = 1
        animation_speed = -1
        
        # Large
        sprite_label = f'{GemsMergeObjectColorEnum.Blue.name}_{MergeObjectSizeEnum.Large.name}'
        sprite_position = (11,11)
        sprite_size = (46,43)
        blue_large_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [-6.5,-20.5],
            [2.5,-16.5],
            [9.5,-13.5],
            [18.5,-10.5],
            [21.5,-0.5],
            [21.5,9.5],
            [13.5,17.5],
            [4.5,21.5],
            [-3.5,17.5],
            [-13.5,16.5],
            [-21.5,9.5],
            [-20.5,0.5],
            [-14.5,-9.5],
            [-10.5,-17.5]
        ]
        blue_large_config.poly_points = poly_points
        self.sprite_config[blue_large_config.label] = blue_large_config

        # Medium
        sprite_label = f'{GemsMergeObjectColorEnum.Blue.name}_{MergeObjectSizeEnum.Medium.name}'
        sprite_position = (7,73)
        sprite_size = (33,30)
        blue_md_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [-5.0,-15.0],
            [4.0,-16.0],
            [10.0,-7.0],
            [14.0,2.0],
            [13.0,11.0],
            [5.0,13.0],
            [-4.0,14.0],
            [-12.0,10.0],
            [-16.0,1.0],
            [-13.0,-8.0],
            [-7.0,-14.0]
        ]
        blue_md_config.poly_points = poly_points
        self.sprite_config[blue_md_config.label] = blue_md_config

        # Small
        sprite_label = f'{GemsMergeObjectColorEnum.Blue.name}_{MergeObjectSizeEnum.Small.name}'
        sprite_position = (484,68)
        sprite_size = (23,21)
        blue_sm_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [-3.0,-11.0],
            [7.0,-5.0],
            [7.0,5.0],
            [0.0,9.0],
            [-10.0,6.0],
            [-10.0,-4.0],
            [-3.0,-11.0]
        ]
        blue_sm_config.poly_points = poly_points
        self.sprite_config[blue_sm_config.label] = blue_sm_config

    def setup_yellow_green_gem_sprite_config(self):
        animation_steps = 1
        animation_speed = -1
        
        # Large
        sprite_label = f'{GemsMergeObjectColorEnum.YellowGreen.name}_{MergeObjectSizeEnum.Large.name}'
        sprite_position = (71,7)
        sprite_size = (49,46)
        green_large_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [-3.0,-25.0],
            [9.0,-17.0],
            [20.0,-8.0],
            [22.0,4.0],
            [14.0,14.0],
            [2.0,19.0],
            [-10.0,17.0],
            [-21.0,9.0],
            [-20.0,-3.0],
            [-13.0,-15.0]
        ]
        green_large_config.poly_points = poly_points
        self.sprite_config[green_large_config.label] = green_large_config

        # Medium
        sprite_label = f'{GemsMergeObjectColorEnum.YellowGreen.name}_{MergeObjectSizeEnum.Medium.name}'
        sprite_position = (52,68)
        sprite_size = (38,36)
        green_md_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [4.0,-20.0],
            [16.0,-9.0],
            [19.0,2.0],
            [15.0,14.0],
            [3.0,16.0],
            [-8.0,15.0],
            [-20.0,10.0],
            [-15.0,-2.0],
            [-10.0,-13.0],
            [2.0,-18.0]
        ]
        green_md_config.poly_points = poly_points
        self.sprite_config[green_md_config.label] = green_md_config

        # Small
        sprite_label = f'{GemsMergeObjectColorEnum.YellowGreen.name}_{MergeObjectSizeEnum.Small.name}'
        sprite_position = (514,66)
        sprite_size = (26,25)
        green_sm_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [1.0,-14.0],
            [11.0,-4.0],
            [11.0,5.0],
            [4.0,12.0],
            [-6.0,11.0],
            [-14.0,6.0],
            [-11.0,-4.0],
            [-1.0,-12.0]
        ]
        green_sm_config.poly_points = poly_points
        self.sprite_config[green_sm_config.label] = green_sm_config
    
    def setup_black_gem_sprite_config(self):
        animation_steps = 1
        animation_speed = -1
        
        # Large
        sprite_label = f'{GemsMergeObjectColorEnum.Black.name}_{MergeObjectSizeEnum.Large.name}'
        sprite_position = (141,9)
        sprite_size = (32,47)
        black_large_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [10.0,-23.0],
            [16.0,-8.0],
            [14.0,7.0],
            [12.0,20.0],
            [1.0,18.0],
            [-14.0,21.0],
            [-18.0,7.0],
            [-19.0,-8.0],
            [-8.0,-16.0],
            [4.0,-17.0]
        ]
        black_large_config.poly_points = poly_points
        self.sprite_config[black_large_config.label] = black_large_config

        # Medium
        sprite_label = f'{GemsMergeObjectColorEnum.Black.name}_{MergeObjectSizeEnum.Medium.name}'
        sprite_position = (106,69)
        sprite_size = (27,36)
        black_md_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [-8.0,-19.0],
            [3.0,-16.0],
            [13.0,-9.0],
            [12.0,3.0],
            [3.0,11.0],
            [-7.0,18.0],
            [-12.0,6.0],
            [-14.0,-6.0],
            [-9.0,-18.0]
        ]
        black_md_config.poly_points = poly_points
        self.sprite_config[black_md_config.label] = black_md_config

        # Small
        sprite_label = f'{GemsMergeObjectColorEnum.Black.name}_{MergeObjectSizeEnum.Small.name}'
        sprite_position = (550,66)
        sprite_size = (17,24)
        black_sm_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [3.0,-13.0],
            [7.0,-4.0],
            [4.0,5.0],
            [-2.0,9.0],
            [-10.0,3.0],
            [-8.0,-7.0],
            [1.0,-12.0]
        ]
        black_sm_config.poly_points = poly_points
        self.sprite_config[black_sm_config.label] = black_sm_config

    def setup_red_gem_sprite_config(self):
        animation_steps = 1
        animation_speed = -1
        
        # Large
        sprite_label = f'{GemsMergeObjectColorEnum.Red.name}_{MergeObjectSizeEnum.Large.name}'
        sprite_position = (204,8)
        sprite_size = (39,44)
        red_large_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [-13.0,-24.0],
            [1.0,-15.0],
            [14.0,-21.0],
            [17.0,-6.0],
            [19.0,9.0],
            [10.0,21.0],
            [-3.0,18.0],
            [-18.0,18.0],
            [-17.0,3.0],
            [-20.0,-12.0]
        ]
        red_large_config.poly_points = poly_points
        self.sprite_config[red_large_config.label] = red_large_config

        # Medium
        sprite_label = f'{GemsMergeObjectColorEnum.Red.name}_{MergeObjectSizeEnum.Medium.name}'
        sprite_position = (151,69)
        sprite_size = (32,35)
        red_md_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [-5.0,-19.0],
            [5.0,-16.0],
            [15.0,-10.0],
            [15.0,0.0],
            [11.0,10.0],
            [6.0,19.0],
            [-3.0,14.0],
            [-13.0,11.0],
            [-17.0,2.0],
            [-14.0,-8.0],
            [-6.0,-18.0]
        ]
        red_md_config.poly_points = poly_points
        self.sprite_config[red_md_config.label] = red_md_config

        # Small
        sprite_label = f'{GemsMergeObjectColorEnum.Red.name}_{MergeObjectSizeEnum.Small.name}'
        sprite_position = (583,67)
        sprite_size = (16,24)
        red_sm_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [2.0,-13.0],
            [11.0,-8.0],
            [8.0,2.0],
            [2.0,10.0],
            [-9.0,10.0],
            [-8.0,0.0],
            [-3.0,-10.0]
        ]
        red_sm_config.poly_points = poly_points
        self.sprite_config[red_sm_config.label] = red_sm_config

    def setup_green_gem_sprite_config(self):
        animation_steps = 1
        animation_speed = -1
        
        # Large
        sprite_label = f'{GemsMergeObjectColorEnum.Green.name}_{MergeObjectSizeEnum.Large.name}'
        sprite_position = (270,12)
        sprite_size = (36,38)
        green_large_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [7.0,-20.0],
            [18.0,-9.0],
            [13.0,6.0],
            [6.0,13.0],
            [-8.0,18.0],
            [-16.0,7.0],
            [-16.0,-8.0],
            [-1.0,-17.0]
        ]
        green_large_config.poly_points = poly_points
        self.sprite_config[green_large_config.label] = green_large_config

        # Medium
        sprite_label = f'{GemsMergeObjectColorEnum.Green.name}_{MergeObjectSizeEnum.Medium.name}'
        sprite_position = (200,72)
        sprite_size = (28,29)
        green_md_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [1.0,-16.0],
            [10.0,-9.0],
            [13.0,1.0],
            [9.0,11.0],
            [-1.0,12.0],
            [-10.0,10.0],
            [-15.0,1.0],
            [-13.0,-9.0],
            [-3.0,-13.0]
        ]
        green_md_config.poly_points = poly_points
        self.sprite_config[green_md_config.label] = green_md_config

        # Small
        sprite_label = f'{GemsMergeObjectColorEnum.Green.name}_{MergeObjectSizeEnum.Small.name}'
        sprite_position = (616,72)
        sprite_size = (15,18)
        green_sm_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [-3.0,-8.0],
            [7.0,-6.0],
            [6.0,3.0],
            [1.0,10.0],
            [-8.0,3.0],
            [-4.0,-7.0]
        ]
        green_sm_config.poly_points = poly_points
        self.sprite_config[green_sm_config.label] = green_sm_config

    def setup_white_gem_sprite_config(self):
        animation_steps = 1
        animation_speed = -1
        
        # Large
        sprite_label = f'{GemsMergeObjectColorEnum.White.name}_{MergeObjectSizeEnum.Large.name}'
        sprite_position = (325,7)
        sprite_size = (53,49)
        white_large_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [16.0,-25.0],
            [17.0,-15.0],
            [11.0,-5.0],
            [12.0,1.0],
            [22.0,1.0],
            [20.0,9.0],
            [10.0,9.0],
            [13.0,17.0],
            [10.0,23.0],
            [2.0,16.0],
            [-3.0,14.0],
            [-12.0,20.0],
            [-16.0,14.0],
            [-18.0,6.0],
            [-13.0,2.0],
            [-23.0,-3.0],
            [-26.0,-11.0],
            [-16.0,-9.0],
            [-10.0,-10.0],
            [-7.0,-15.0],
            [-2.0,-19.0],
            [1.0,-9.0],
            [4.0,-9.0],
            [7.0,-19.0],
            [16.0,-25.0]
        ]
        white_large_config.poly_points = poly_points
        self.sprite_config[white_large_config.label] = white_large_config

        # Medium
        sprite_label = f'{GemsMergeObjectColorEnum.White.name}_{MergeObjectSizeEnum.Medium.name}'
        sprite_position = (244,70)
        sprite_size = (37,32)
        white_md_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [-11.0,-18.0],
            [-4.0,-9.0],
            [0.0,-5.0],
            [7.0,-13.0],
            [5.0,-3.0],
            [15.0,-7.0],
            [14.0,0.0],
            [9.0,7.0],
            [3.0,11.0],
            [-6.0,12.0],
            [-15.0,10.0],
            [-15.0,3.0],
            [-9.0,-4.0],
            [-11.0,-14.0]
        ]
        white_md_config.poly_points = poly_points
        self.sprite_config[white_md_config.label] = white_md_config

        # Small
        sprite_label = f'{GemsMergeObjectColorEnum.White.name}_{MergeObjectSizeEnum.Small.name}'
        sprite_position = (6,118)
        sprite_size = (20,20)
        white_sm_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [3.0,-10.0],
            [3.0,-2.0],
            [10.0,4.0],
            [3.0,7.0],
            [-5.0,9.0],
            [-7.0,0.0],
            [-6.0,-5.0],
            [0.0,-8.0]
        ]
        white_sm_config.poly_points = poly_points
        self.sprite_config[white_sm_config.label] = white_sm_config

    def setup_violet_gem_sprite_config(self):
        animation_steps = 1
        animation_speed = -1
        
        # Large
        sprite_label = f'{GemsMergeObjectColorEnum.Violet.name}_{MergeObjectSizeEnum.Large.name}'
        sprite_position = (396,10)
        sprite_size = (41,41)
        violet_large_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [-11.0,-22.0],
            [4.0,-16.0],
            [18.0,-16.0],
            [20.0,-2.0],
            [14.0,13.0],
            [-1.0,19.0],
            [-14.0,9.0],
            [-17.0,-3.0],
            [-13.0,-18.0]
        ]
        violet_large_config.poly_points = poly_points
        self.sprite_config[violet_large_config.label] = violet_large_config

        # Medium
        sprite_label = f'{GemsMergeObjectColorEnum.Violet.name}_{MergeObjectSizeEnum.Medium.name}'
        sprite_position = (293,68)
        sprite_size = (36,36)
        violet_md_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [3.0,-20.0],
            [11.0,-8.0],
            [18.0,-1.0],
            [10.0,8.0],
            [-1.0,17.0],
            [-11.0,9.0],
            [-18.0,-3.0],
            [-15.0,-11.0],
            [-3.0,-16.0]
        ]
        violet_md_config.poly_points = poly_points
        self.sprite_config[violet_md_config.label] = violet_md_config

        # Small
        sprite_label = f'{GemsMergeObjectColorEnum.Violet.name}_{MergeObjectSizeEnum.Small.name}'
        sprite_position = (36,115)
        sprite_size = (22,22)
        violet_sm_config = SpriteAnimationConfig(sprite_label, sprite_position, sprite_size, animation_steps, animation_speed)
        poly_points = [
            [4.0,-13.0],
            [11.0,-6.0],
            [6.0,5.0],
            [-6.0,9.0],
            [-12.0,-3.0],
            [-7.0,-10.0]
        ]
        violet_sm_config.poly_points = poly_points
        self.sprite_config[violet_sm_config.label] = violet_sm_config