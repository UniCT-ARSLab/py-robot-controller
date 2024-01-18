import threading

import can

from models.can_packet import CAN_position
from robot.constants import CAN_IDS, CHANNEL, DEBUG_CAN, DEBUG_VIRTUAL
from robot.robot import Robot
from robot.virtual import get_v_bus, get_v_message
from webserver.webserver import start_webservices

robot = Robot()

# run webserver asynchronously in a separate thread
threading.Thread(target=start_webservices).start()

_bustype='socketcan' if not DEBUG_VIRTUAL else 'virtual'
bus = can.interface.Bus(channel=CHANNEL, bustype=_bustype)

if DEBUG_VIRTUAL:
    v_bus = get_v_bus(CHANNEL)

    v_message = get_v_message(CAN_IDS["ROBOT_POSITION"], "<hhh", CAN_position)
    v_messageUnk = get_v_message(0x333, "<hhh", CAN_position)

    v_bus.send(v_message)
    v_bus.send(v_messageUnk)

robot.init_lidar()

try:
    while True:
        robot.get_lidar_data()

        message = bus.recv()
        if DEBUG_CAN:
            print(message)

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
