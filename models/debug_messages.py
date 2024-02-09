
from typing import List

from models.can_packet import (
    CAN_FORMATS,
    CAN_IDS,
    CAN_distance_sensor,
    CAN_position,
    CAN_robot_status,
    CAN_velocity,
)
from models.interfaces import VirtualMessages

virtual_messages: List[VirtualMessages] = [
    {
        "packet_id": CAN_IDS["ROBOT_POSITION"], "format": CAN_FORMATS["POSITION"], "data": CAN_position
    },
    {
        "packet_id": CAN_IDS["ROBOT_SPEED"], "format": CAN_FORMATS["VELOCITY"], "data": CAN_velocity
    },
    {
        "packet_id": CAN_IDS["OTHER_ROBOT_POSITION"], "format": CAN_FORMATS["POSITION"], "data": CAN_position
    },
    {
        "packet_id": CAN_IDS["ROBOT_STATUS"], "format": CAN_FORMATS["ROBOT_STATUS"], "data": CAN_robot_status
    },
    {
        "packet_id": CAN_IDS["DISTANCE_SENSOR"], "format": CAN_FORMATS["DISTANCE_SENSOR"], "data": CAN_distance_sensor
    },
    {
        "packet_id": 0x333, "format": "<hhhBB",  "data": { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5 },
    },

]
