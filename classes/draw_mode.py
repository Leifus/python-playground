from enum import Flag, auto

class DrawMode(Flag):
    WIREFRAME = auto()
    RAW = auto()
    RICH = auto()
    PHYSICS = auto()
    NONE = auto()
