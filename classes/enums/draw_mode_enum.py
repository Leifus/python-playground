from enum import Flag, auto

class DrawModeEnum(Flag):
    Wireframe = auto()
    Raw = auto()
    Rich = auto()
    Physics = auto()
    NONE = auto()
