from typing import Any, TypedDict, Union


class VirtualMessages(TypedDict):
    packet_id: int
    format: str
    data: Any

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

class DistanceSensor(TypedDict):
    sensor: int
    distance: int
    alarm: int
    # char padding[4]


class StrategyCommand(TypedDict):
    cmd: int
    flags: int  # color
    elapsed_time: int
    stgy: int
    align: int
    # char padding[2]
