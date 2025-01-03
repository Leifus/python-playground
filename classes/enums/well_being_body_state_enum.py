from enum import Flag, auto

class WellBeingBodyStateEnum(Flag):
    Alive = auto()
    Wounded = auto()
    Deceased = auto()
    Decayed = auto()
    Bones = auto()
    Spirit = auto()
