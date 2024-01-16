import struct

import can

from robot.constants import ID_ROBOT_POSITION


def get_v_bus(_channel: str) -> can.interface.Bus:
    return can.interface.Bus(channel=_channel, interface='virtual', preserve_timestamps=True)

def get_v_message(format: str, data: dict) -> can.Message:
    message_data = struct.pack(format, *data.values())
    msg = can.Message(arbitration_id=ID_ROBOT_POSITION, data=message_data)
    return msg

