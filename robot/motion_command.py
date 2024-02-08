import struct
from typing import Union

from models.can_packet import CAN_FORMATS


class MotionCommand:
    # pylint: disable=too-many-arguments
    def __init__(self, cmd: int, param_1: int, param_2: int, param_3: Union[float, int], flags: int, bumpers: int) -> None:
        self.cmd = cmd
        self.param_1 = param_1
        self.param_2 = param_2
        self.param_3 = param_3
        self.flags = flags
        self.bumpers = bumpers

    def get_struct(self) -> bytes:
        return struct.pack(CAN_FORMATS["POSITION"], self.cmd, self.param_1, self.param_2, self.param_3, self.flags, self.bumpers)
