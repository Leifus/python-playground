from enum import Flag, auto

class InGameEventEnum(Flag):
    Spawn_Hole = auto()
    Ball_Mass = auto()
    Ball_Size = auto()
    NONE = auto()