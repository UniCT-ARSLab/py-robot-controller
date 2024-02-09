import threading
from typing import List

import can

from models.debug_messages import virtual_messages
from robot.config import (
    CAN_BAUD,
    CHANNEL,
    DEBUG_CAN,
    DEBUG_VCAN,
    DEBUG_VIRTUAL,
    VCHANNEL,
)
from robot.robot import robot
from robot.virtual import get_v_bus, get_v_message
from webserver.webserver import start_rest_api, start_socket

# run webserver asynchronously in a separate thread
threading.Thread(target=start_socket).start()
threading.Thread(target=start_rest_api).start()

_bustype = "virtual" if DEBUG_VIRTUAL or DEBUG_VCAN else "socketcan"
_channel = VCHANNEL if DEBUG_VCAN else CHANNEL
bus = can.interface.Bus(channel=_channel, bustype=_bustype, bitrate=CAN_BAUD)

if DEBUG_CAN:
    print(f"Bus type: {_bustype}")
    print(f"Channel: {_channel}")

if DEBUG_VIRTUAL or DEBUG_VCAN:
    v_messages: List[can.Message] = []
    for v_message in virtual_messages:
        v_messages.append(get_v_message(v_message["packet_id"], v_message["format"], v_message["data"]))

if DEBUG_VIRTUAL:
    v_bus = get_v_bus(CHANNEL)
    for virtual_message in v_messages:
        v_bus.send(virtual_message)

if DEBUG_VCAN:
    for virtual_message in v_messages:
        bus.send(virtual_message)

robot.init_lidar()

try:
    while True:
        robot.get_lidar_data()

        message = bus.recv()
        if DEBUG_CAN:
            print("\n", message)

        if message is not None:
            try:
                robot.on_data_received(message)
            except Exception as e:
                print(str(e))
except KeyboardInterrupt:
    print("KeyboardInterrupt")
except Exception as e:
    print(str(e))
finally:
    bus.shutdown()
    if DEBUG_VIRTUAL:
        v_bus.shutdown()
