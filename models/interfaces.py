from typing import TypedDict, Union


class Position(TypedDict):
    X: int
    Y: int
    Angle: Union[float, int]
    Flags: int
    Bumpers: int

class Velocity(TypedDict):
    linear_speed: int
    padding: bytearray
