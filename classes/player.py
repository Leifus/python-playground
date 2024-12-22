from classes.game_sprite import GameSprite

class Player(GameSprite):
    def __init__(self, name):
        super(GameSprite, self).__init__()
        
        self.name = name
        
    