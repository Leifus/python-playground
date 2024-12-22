from classes.game_sprite import GameSprite

class Player(GameSprite):
    def __init__(self, identifier, name):
        super(GameSprite, self).__init__()
        
        self.identifier = identifier
        self.name = name
        self.is_playing = False
        self.can_take_shot = False
        self.has_taken_shot = False
    