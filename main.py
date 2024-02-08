import threading

import can

from models.can_packet import CAN_FORMATS, CAN_IDS, CAN_position, CAN_velocity
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
    v_message = get_v_message(CAN_IDS["ROBOT_POSITION"], CAN_FORMATS["POSITION"], CAN_position)
    v_message_velocity = get_v_message(CAN_IDS["ROBOT_SPEED"], CAN_FORMATS["VELOCITY"], CAN_velocity)
    v_message_other_position = get_v_message(CAN_IDS["OTHER_ROBOT_POSITION"], CAN_FORMATS["POSITION"], CAN_position)
    v_messageUnk = get_v_message(0x333, "<hhhBB", { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5 })

if DEBUG_VIRTUAL:
    v_bus = get_v_bus(CHANNEL)
    v_bus.send(v_message)
    v_bus.send(v_message_velocity)
    v_bus.send(v_message_other_position)
    v_bus.send(v_messageUnk)

if DEBUG_VCAN:
    bus.send(v_message)
    bus.send(v_message_velocity)
    bus.send(v_message_other_position)
    bus.send(v_messageUnk)

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
