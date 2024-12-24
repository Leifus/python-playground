from enum import Flag, auto

class GameModeEnum(Flag):
    CirclePool = auto()
    Billiards = auto()
    Snooker = auto()
    NONE = auto()
