import struct

from can import Message
from can.interface import Bus, BusABC

from robot.config import CAN_BAUD


def get_v_bus(_channel: str) -> BusABC:
    return Bus(channel=_channel, interface='virtual', preserve_timestamps=True, bitrate=CAN_BAUD)

def get_v_message(packet_id: int, format: str, data: dict) -> Message:
    values = data.values()
    message_data = struct.pack(format, *values)
    msg = Message(arbitration_id=packet_id, data=message_data, is_extended_id=False, is_rx=False)
    return msg
