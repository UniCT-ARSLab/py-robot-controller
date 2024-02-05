# not working

from models.can_packet import CAN_IDS, CAN_position
from robot.config import CHANNEL
from robot.virtual import get_v_bus, get_v_message

v_bus = get_v_bus(CHANNEL)
v_msg = get_v_message(CAN_IDS['ROBOT_POSITION'], "<hhh", CAN_position)
v_bus.send(v_msg)
v_bus.shutdown()
