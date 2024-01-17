from typing import TypedDict, Union


class Position(TypedDict):
    X: int
    Y: int
    angle: Union[float, int]

CAN_position: Position = {
    "X": 10,
    "Y": 20,
    "angle": 300,
}
