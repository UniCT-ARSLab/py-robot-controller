import can

from robot.constants import CHANNEL, DEBUG_CAN
from robot.model import CAN_position
from robot.robot import Robot
from robot.virtual import get_v_bus, get_v_message

_bustype='socketcan' if not DEBUG_CAN else 'virtual'
bus = can.interface.Bus(channel=CHANNEL, bustype=_bustype)

if DEBUG_CAN:
    v_bus = get_v_bus(CHANNEL)
    v_message = get_v_message("<hhh", CAN_position)
    v_bus.send(v_message)

robot = Robot()

while True:
    message = bus.recv()
    print(message)

    if message is not None:
        try:
            robot.on_data_received(message)
        except Exception as e:
            print(str(e))
