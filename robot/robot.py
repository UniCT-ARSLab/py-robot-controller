import struct
from random import randrange
from typing import List

import can
from breezylidar import URG04LX

from models.can_packet import MotionCommand, Position
from models.lidar_mock import SCANDATA_MOCKS
from robot.constants import (
    CAN_IDS,
    CHANNEL,
    DEBUG_CAN,
    DEBUG_LIDAR,
    DEBUG_VCAN,
    DEBUG_VIRTUAL,
    LIDAR_DEVICE,
    MOTION_CMDS,
    VCHANNEL,
)


class Robot:
    def __init__(self):
        # Initialize the CAN bus
        _channel = VCHANNEL if DEBUG_VCAN else CHANNEL
        _bustype = "virtual" if DEBUG_VIRTUAL or DEBUG_VCAN else "socketcan"
        self.bus = can.interface.Bus(channel=_channel, bustype=_bustype)

        # Initialize the lidar
        self.laser_data = []
        self.laser = None

        # Initialize the starting and current positions of the robot
        self.StartPosition: Position = {"X": -1000, "Y": -1000, "Angle": 0}
        self.Position: Position = {"X": 0, "Y": 0, "Angle": 0}

    def on_data_received(self, frm: can.Message):
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
            posX, posY, angle = struct.unpack("<hhh", data[:6])

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

            if DEBUG_CAN: # debug can viene usata per scopi diversi (switch da virtual a socket / logging), forse serve un altro flag
                print(f"Position: [X: {posX}, Y: {posY}, A: {angle}]")

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
        mc = MotionCommand(MOTION_CMDS['SET_POSITION'], position["X"], position["Y"], position["Angle"], 0)
        data = mc.get_struct()
        msg = can.Message(arbitration_id=CAN_IDS["ROBOT_POSITION"], data=data, extended_id=False)
        self.bus.send(msg)
    def set_position(self, x: int, y: int, angle: int) -> None:
        """
        Set the position of the robot using individual X, Y, and Angle values.

        :param x: X-coordinate of the robot.
        :type x: int
        :param y: Y-coordinate of the robot.
        :type y: int
        :param angle: Angle of the robot.
        :type angle: int

        :return: None
        """
        mc = MotionCommand(MOTION_CMDS['SET_POSITION'], x, y, angle, 0)
        data = mc.get_struct()
        msg = can.Message(arbitration_id=CAN_IDS["ROBOT_POSITION"], data=data, extended_id=False)
        self.bus.send(msg)

    def set_speed(self, speed: int) -> None:
        """
        Set the speed of the robot.

        :param speed: Speed of the robot.
        :type speed: int

        :return: None
        """
        mc = MotionCommand(MOTION_CMDS['SET_SPEED'], speed, 0, 0, 0)
        data = mc.get_struct()
        msg = can.Message(arbitration_id=CAN_IDS["ROBOT_MOTION_COMMAND"], data=data, extended_id=False)
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
