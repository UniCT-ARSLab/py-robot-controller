import threading

from can.interface import Bus

from models.debug_messages import init_debug
from robot.config import (
    CAN_BAUD,
    CHANNEL,
    DEBUG_CAN,
    DEBUG_VCAN,
    DEBUG_VIRTUAL,
    VCHANNEL,
)
from robot.robot import robot
from webserver.webserver import start_rest_api, start_socket

# run webserver asynchronously in a separate thread
threading.Thread(target=start_socket).start()
threading.Thread(target=start_rest_api).start()

_bustype = "virtual" if DEBUG_VIRTUAL or DEBUG_VCAN else "socketcan"
_channel = VCHANNEL if DEBUG_VCAN else CHANNEL
bus = Bus(channel=_channel, bustype=_bustype, bitrate=CAN_BAUD)

if DEBUG_CAN or DEBUG_VIRTUAL or DEBUG_VCAN:
    v_bus = init_debug(bus, _bustype, _channel)

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
