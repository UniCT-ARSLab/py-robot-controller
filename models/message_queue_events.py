from enum import Enum


class MessageQueueEvents(Enum):
    NEW_CAN_PACKET = "NEW_CAN_PACKET"
    ROBOT_DATA = "ROBOT_DATA"
    LIDAR_DATA = "LIDAR_DATA"
    SEND_ALIGN = "SEND_ALIGN"
    END_CYCLE = "END_CYCLE"
