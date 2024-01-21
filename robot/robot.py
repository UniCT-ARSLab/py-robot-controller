import struct
from typing import List

import can
from breezylidar import URG04LX

from models.can_packet import Position
from models.lidar_mock import SCANDATA_MOCK
from robot.constants import CAN_IDS, DEBUG_CAN, DEBUG_VCAN, DEBUG_LIDAR, DEBUG_VIRTUAL, LIDAR_DEVICE, CHANNEL, VCHANNEL


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
        data = struct.pack("<hhh", position["X"], position["Y"], position["Angle"])
        msg = can.Message(arbitration_id=CAN_IDS["ROBOT_POSITION"], data=data, extended_id=False)
        self.bus.send(msg)
    def set_position(self, x: int, y: int, angle: int) -> None:
        data = struct.pack("<hhh", x, y, angle)
        msg = can.Message(arbitration_id=CAN_IDS["ROBOT_POSITION"], data=data, extended_id=False)
        self.bus.send(msg)

    def init_lidar(self) -> None:
        if not DEBUG_VIRTUAL and not DEBUG_VCAN:
            self.laser = URG04LX(LIDAR_DEVICE)

    def get_lidar_data(self) -> None:
        if DEBUG_VIRTUAL or DEBUG_VCAN:
            laser_data = SCANDATA_MOCK
        else:
            laser_data = self.laser.getScan()

        if laser_data:
            if DEBUG_LIDAR:
                print(laser_data)
            return laser_data

        return []

robot = Robot()
