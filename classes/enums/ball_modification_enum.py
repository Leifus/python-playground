from enum import Flag, auto

class BallModificationEnum(Flag):
    MassIncrease = auto()
    MassDecrease = auto()
    RadiusIncrease = auto()
    RadiusDecrease = auto()
