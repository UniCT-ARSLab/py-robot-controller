# not working

import can
from robot.constants import CHANNEL, DEBUG_CAN, CAN_IDS
from robot.virtual import get_v_bus, get_v_message
from robot.model import CAN_position

v_bus = get_v_bus(CHANNEL)
v_msg = get_v_message(0x3E3, "<hhh", CAN_position)
v_bus.send(v_msg)
v_bus.shutdown()