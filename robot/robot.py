import struct
from random import randrange
from time import sleep
from typing import Any, List

from breezylidar import URG04LX
from can import BusABC, Message
from pymitter import EventEmitter

# from models.socket import position_mocks
from models.can_packet import CAN_FORMATS, CAN_IDS, MOTION_CMDS, CAN_align
from models.interfaces import DistanceSensor, Position, RobotStatus
from models.lidar_mock import SCANDATA_MOCKS
from models.message_queue_events import MessageQueueEvents
from robot.config import (
    DEBUG_CAN,
    DEBUG_LIDAR,
    DEBUG_MESSAGES,
    DEBUG_VCAN,
    DEBUG_VIRTUAL,
    LIDAR_DEVICE,
)
from robot.motion_command import MotionCommand


# pylint: disable=too-many-instance-attributes
class Robot:

    def __init__(self, bus: BusABC, global_events: EventEmitter):
        self.bus = bus
        self.events = global_events

        # Initialize the lidar
        self.laser_data: list = []
        self.laser: Any = None

        # init robot values with placeholders
        self.StartPosition: Position = { "X": -1000, "Y": -1000, "Angle": 0, "Flags": 0, "Bumpers": 0 }
        self.Position: Position = { "X": 0, "Y": 0, "Angle": 0, "Flags": 0, "Bumpers": 0 }

        self.linear_speed = 0

        self.robot_status: RobotStatus = {
            "robot_selected": 0,
            "status_display": 0,
        }

        # tof alarms data
        self.distance_sensor: DistanceSensor = {"sensor": 0, "distance": 0, "alarm": 0}

        self.events_management()

    def events_management(self) -> None:
        self.events.on(MessageQueueEvents.NEW_CAN_PACKET.value, self.on_data_received)

    def on_data_received(self, frm: Message) -> None:
        """
        Handle the data received from the CAN bus depending on the CAN ID.
        this has to be called in a loop at the moment, but it should be changed to a callback somehow
        :param frm: The CAN message received.
        :type frm: can.Message
        :return: None
        """
        if not isinstance(frm, Message):
            print("⚠️  malformed CAN message")
            return

        data = frm.data

        if frm.arbitration_id not in CAN_IDS.values():
            if DEBUG_MESSAGES:
                print(f"Unknown CAN ID: {frm.arbitration_id}")
            return

        if frm.arbitration_id in (CAN_IDS["ROBOT_POSITION"], CAN_IDS["OTHER_ROBOT_POSITION"]):
            self.__handle_position(data)
        elif frm.arbitration_id == CAN_IDS["ROBOT_SPEED"]:
            self.__handle_speed(data)
        elif frm.arbitration_id == CAN_IDS["ROBOT_STATUS"]:
            self.__handle_robot_status(data)
        elif frm.arbitration_id == CAN_IDS["DISTANCE_SENSOR"]:
            self.__handle_distance_sensor(data)
        elif frm.arbitration_id == CAN_IDS["STRATEGY_COMMAND"]:
            print("## strategy command in CAN")

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
        linear_speed = struct.unpack(CAN_FORMATS["VELOCITY"], data)
        self.linear_speed = linear_speed  # type: ignore

        if DEBUG_CAN:
            print('linear_speed', linear_speed)

    def __handle_robot_status(self, data: bytearray) -> None:
        robot_selected, status_display = struct.unpack(CAN_FORMATS["ROBOT_STATUS"], data)

        self.robot_status["robot_selected"] = robot_selected
        self.robot_status["status_display"] = status_display

        if DEBUG_CAN:
            print('robot_selected', robot_selected)
            print('status_display', status_display)

    def __handle_distance_sensor(self, data: bytearray) -> None:
        sensor, distance, alarm = struct.unpack(CAN_FORMATS["DISTANCE_SENSOR"], data)
        self.distance_sensor = {"sensor": sensor, "distance": distance, "alarm": alarm}

        if DEBUG_CAN:
            print('sensor', sensor)
            print('distance', distance)
            print('alarm', alarm)

    # currently unused
    def get_position(self) -> Position:
        return self.Position

    def get_robot_data(self) -> dict:
        # for debugging
        # index = randrange(0, len(position_mocks))
        # self.Position = position_mocks[index]

        robot_data = {
            **self.Position,
            "linear_speed": self.linear_speed,
            **self.robot_status,
            **self.distance_sensor,
        }
        return robot_data

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
        msg = Message(arbitration_id=CAN_IDS["ROBOT_POSITION"], data=data, is_extended_id=False, is_rx=False)
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
        msg = Message(arbitration_id=CAN_IDS["ROBOT_MOTION_COMMAND"], data=data, is_extended_id=False, is_rx=False)
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
            self.laser_data = SCANDATA_MOCKS[index]
        else:
            try:
                self.laser_data = self.laser.getScan()
            # pylint: disable=bare-except
            except:
                # to do: we could put this in a separate thread
                print("ERROR reading LiDAR data, waiting 5 seconds")
                sleep(5)

        if self.laser_data:
            if DEBUG_LIDAR:
                print(self.laser_data)
            return self.laser_data

        return []

    def send_align(self) -> None:
        print("## send align")
        data = struct.pack(CAN_FORMATS["ALIGN"], *(CAN_align.values()))
        msg = Message(
            arbitration_id=CAN_IDS["STRATEGY_COMMAND"],
            data=data,
            is_extended_id=False,
            is_rx=False,
        )
        self.bus.send(msg)
