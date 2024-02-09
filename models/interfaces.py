from typing import TypedDict, Union


class Position(TypedDict):
    X: int
    Y: int
    Angle: Union[float, int]
    Flags: int
    Bumpers: int

class Velocity(TypedDict):
    linear_speed: int

class RobotStatus(TypedDict):
    robot_selected: int
    status_display: int
