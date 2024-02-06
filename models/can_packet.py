import struct
from typing import TypedDict, Union


class Position(TypedDict):
    X: int
    Y: int
    Angle: Union[float, int]

CAN_position: Position = {
    "X": 10,
    "Y": 20,
    "Angle": 300,
}

class MotionCommand:
    # pylint: disable=too-many-arguments
    def __init__(self, CMD: int, PARAM_1: int, PARAM_2: int, PARAM_3: Union[float, int], flags: int) -> None:
        self.CMD = CMD
        self.PARAM_1 = PARAM_1
        self.PARAM_2 = PARAM_2
        self.PARAM_3 = PARAM_3
        self.flags = flags

    def get_struct(self) -> bytes:
        return struct.pack("<BhhhB", self.CMD, self.PARAM_1, self.PARAM_2, self.PARAM_3, self.flags)
