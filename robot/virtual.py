import struct

import can


def get_v_bus(_channel: str) -> can.interface.BusABC:
    return can.interface.Bus(channel=_channel, interface='virtual', preserve_timestamps=True)

def get_v_message(packet_id: int, format: str, data: dict) -> can.Message:
    message_data = struct.pack(format, *data.values())
    msg = can.Message(arbitration_id=packet_id, data=message_data)
    return msg
