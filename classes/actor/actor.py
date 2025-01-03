from classes.actor.actor_well_being import ActorWellBeing
from classes.common.sprite_sheet import SpriteSheet
from config import pymunk, math

class Actor(SpriteSheet):
    def __init__(self, birth_date, sprite_sheet_image_path, animation_data, current_animation, color_key, animate):
        super(Actor, self).__init__(sprite_sheet_image_path, animation_data, current_animation, color_key, animate)

        self.body: pymunk.Body = None
        self.shape: pymunk.Shape = None
        self.is_active = False

        self.well_being = ActorWellBeing(birth_date)

    def update(self, time_lapsed, *args, **kwargs):
        self.well_being.update(time_lapsed)
        return super().update(time_lapsed, *args, **kwargs)
        
    def update_position(self, position):
        if self.body:
            self.body.position = position
        self.position = position
        self.redraw()

    def update_angle(self, degrees):
        if self.body:
            self.body.angle = math.radians(degrees)

        self.angle = degrees
        self.redraw()

        