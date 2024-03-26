from typing import List, Union

from can import BusABC, Message

from models.can_packet import (
    CAN_FORMATS,
    CAN_IDS,
    CAN_align,
    CAN_distance_sensor,
    CAN_position,
    CAN_robot_status,
    CAN_velocity,
)
from models.interfaces import VirtualMessages
from robot.config import CHANNEL, DEBUG_CAN, DEBUG_VCAN, DEBUG_VIRTUAL
from robot.virtual import get_v_bus, get_v_message

virtual_messages: List[VirtualMessages] = [
    {
        "packet_id": CAN_IDS["ROBOT_POSITION"],
        "format": CAN_FORMATS["POSITION"],
        "data": CAN_position,
    },
    {
        "packet_id": CAN_IDS["ROBOT_SPEED"],
        "format": CAN_FORMATS["VELOCITY"],
        "data": CAN_velocity,
    },
    {
        "packet_id": CAN_IDS["OTHER_ROBOT_POSITION"],
        "format": CAN_FORMATS["POSITION"],
        "data": CAN_position,
    },
    {
        "packet_id": CAN_IDS["ROBOT_STATUS"],
        "format": CAN_FORMATS["ROBOT_STATUS"],
        "data": CAN_robot_status,
    },
    {
        "packet_id": CAN_IDS["DISTANCE_SENSOR"],
        "format": CAN_FORMATS["DISTANCE_SENSOR"],
        "data": CAN_distance_sensor,
    },
    {
        "packet_id": CAN_IDS["STRATEGY_COMMAND"],
        "format": CAN_FORMATS["ALIGN"],
        "data": CAN_align,
    },
    {
        "packet_id": 0x333,
        "format": "<hhhBB",
        "data": {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5},
    },
]


def init_debug(bus: BusABC, _bustype: str, _channel: str) -> Union[BusABC, None]:
    if DEBUG_CAN:
        print(f"ℹ️  Bus type: {_bustype}")
        print(f"ℹ️  Channel: {_channel}")

    if DEBUG_VIRTUAL or DEBUG_VCAN:
        v_messages: List[Message] = []
        for v_message in virtual_messages:
            v_messages.append(
                get_v_message(
                    v_message["packet_id"], v_message["format"], v_message["data"]
                )
            )

    v_bus = None
    if DEBUG_VIRTUAL:
        v_bus = get_v_bus(CHANNEL)
        for virtual_message in v_messages:
            v_bus.send(virtual_message)

    if DEBUG_VCAN:
        for virtual_message in v_messages:
            bus.send(virtual_message)

    return v_bus
