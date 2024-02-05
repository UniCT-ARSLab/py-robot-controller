import struct
from random import randrange
from typing import Any, List

import can
from breezylidar import URG04LX

from models.can_packet import CAN_FORMATS, CAN_IDS, MOTION_CMDS
from models.interfaces import Position
from models.lidar_mock import SCANDATA_MOCKS
from robot.config import (
    CAN_BAUD,
    CHANNEL,
    DEBUG_CAN,
    DEBUG_LIDAR,
    DEBUG_VCAN,
    DEBUG_VIRTUAL,
    LIDAR_DEVICE,
    VCHANNEL,
)
from robot.motion_command import MotionCommand


class Robot:
    def __init__(self):
        # Initialize the CAN bus
        _channel = VCHANNEL if DEBUG_VCAN else CHANNEL
        _bustype = "virtual" if DEBUG_VIRTUAL or DEBUG_VCAN else "socketcan"
        self.bus = can.interface.Bus(channel=_channel, bustype=_bustype, bitrate=CAN_BAUD)

        # Initialize the lidar
        self.laser_data = []
        self.laser: Any = None

        # Initialize the starting and current positions of the robot
        self.StartPosition: Position = { "X": -1000, "Y": -1000, "Angle": 0, "Flags": 0, "Bumpers": 0 }
        self.Position: Position = { "X": 0, "Y": 0, "Angle": 0, "Flags": 0, "Bumpers": 0 }

    def on_data_received(self, frm: can.Message) -> None:
        """
        Handle the data received from the CAN bus depending on the CAN ID.
        this has to be called in a loop at the moment, but it should be changed to a callback somehow
        :param frm: The CAN message received.
        :type frm: can.Message
        :return: None
        """
        # Extract data from the CAN message
        data = frm.data

        if frm.arbitration_id not in CAN_IDS.values():
            print(f"Unknown CAN ID: {frm.arbitration_id}")
            return

        if frm.arbitration_id == CAN_IDS["ROBOT_POSITION"]:
            self.__handle_position(data)
        elif frm.arbitration_id == CAN_IDS["ROBOT_SPEED"]:
            self.__handle_speed(data)

    def __handle_position(self, data: bytearray) -> None:
        posX, posY, angle, flags, bumpers = struct.unpack(CAN_FORMATS["POSITION"], data)

        # Convert the angle to a float by dividing by 100
        angle /= 100.0

        # Update the robot's position information
        if self.StartPosition["X"] < -999:
            self.StartPosition["X"] = posX
            self.StartPosition["Y"] = posY
            self.StartPosition["Angle"] = angle

        self.Position["X"] = posX
        self.Position["Y"] = posY
        self.Position["Angle"] = angle
        self.Position["Flags"] = flags
        self.Position["Bumpers"] = bumpers

        if DEBUG_CAN: # debug can viene usata per scopi diversi (switch da virtual a socket / logging), forse serve un altro flag
            print(f"Position: [X: {posX}, Y: {posY}, A: {angle}]")


    def __handle_speed(self, data: bytearray) -> None:
        linear_speed, padding = struct.unpack(CAN_FORMATS["VELOCITY"], data)
        print('linear_speed', linear_speed)
        print('padding')
        print(padding)



    def get_position(self) -> Position:
        return self.Position

    def set_position(self, position: Position) -> None:
        """
        Set the position of the robot using a Position object.

        :param position: A Position object containing X, Y, and Angle values.
        :type position: dict
        :key position["X"]: X-coordinate of the robot.
        :key position["Y"]: Y-coordinate of the robot.
        :key position["Angle"]: Angle of the robot.

        :return: None
        """
        mc = MotionCommand(MOTION_CMDS['SET_POSITION'], position["X"], position["Y"], position["Angle"], 0, 0)
        data = mc.get_struct()
        msg = can.Message(arbitration_id=CAN_IDS["ROBOT_POSITION"], data=data, is_extended_id=False, is_rx=False)
        self.bus.send(msg)

    def set_speed(self, speed: int) -> None:
        """
        Set the speed of the robot.

        :param speed: Speed of the robot.
        :type speed: int

        :return: None
        """
        mc = MotionCommand(MOTION_CMDS['SET_SPEED'], speed, 0, 0, 0, 0)
        data = mc.get_struct()
        msg = can.Message(arbitration_id=CAN_IDS["ROBOT_MOTION_COMMAND"], data=data, is_extended_id=False, is_rx=False)
        self.bus.send(msg)

    def init_lidar(self) -> None:
        """
        Initialize the lidar object of the robot using the LIDAR_DEVICE constant.
        :return: None
        """
        if not DEBUG_VIRTUAL and not DEBUG_VCAN:
            self.laser = URG04LX(LIDAR_DEVICE)

    def get_lidar_data(self) -> List[int]:
        """
        Get the data from the lidar. If DEBUG_VIRTUAL or DEBUG_VCAN are True, the data is mocked.
        :return: List[int]
        """
        if DEBUG_VIRTUAL or DEBUG_VCAN:
            index = randrange(0, len(SCANDATA_MOCKS))
            laser_data = SCANDATA_MOCKS[index]
        else:
            laser_data = self.laser.getScan()

        if laser_data:
            if DEBUG_LIDAR:
                print(laser_data)
            return laser_data

        return []

robot = Robot()
