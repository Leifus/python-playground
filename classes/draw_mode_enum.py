from enum import Flag, auto

class DrawModeEnum(Flag):
    WIREFRAME = auto()
    RAW = auto()
    RICH = auto()
    PHYSICS = auto()
    NONE = auto()
