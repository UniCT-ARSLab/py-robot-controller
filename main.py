import time

from can.interface import Bus
from pymitter import EventEmitter

from models.debug_messages import init_debug
from models.message_queue_events import MessageQueueEvents
from robot.config import (
    CAN_BAUD,
    CHANNEL,
    DEBUG_CAN,
    DEBUG_VCAN,
    DEBUG_VIRTUAL,
    VCHANNEL,
)
from robot.robot import Robot
from utils.colors import bcolors
from utils.helper import proper_exit
from webserver.webserver import WebServer

_bustype = "virtual" if DEBUG_VIRTUAL or DEBUG_VCAN else "socketcan"
_channel = VCHANNEL if DEBUG_VCAN else CHANNEL
bus = Bus(channel=_channel, bustype=_bustype, bitrate=CAN_BAUD)

events = EventEmitter()
robot = Robot(bus, events)
robot.init_lidar()

try:
    webServer = WebServer(host="0.0.0.0", port=5000, global_events=events)
    webServer.start()

    if DEBUG_CAN:
        time.sleep(5)  # wait that the web clients connection

    if DEBUG_CAN or DEBUG_VIRTUAL or DEBUG_VCAN:
        v_bus = init_debug(bus, _bustype, _channel)

    while True:
        robot.get_lidar_data()

        message = bus.recv()
        if DEBUG_CAN:
            print(f"{bcolors.OKCYAN.value}{message}{bcolors.ENDC.value}")

        if message is not None:
            events.emit(MessageQueueEvents.NEW_CAN_PACKET.value, message)

except KeyboardInterrupt:
    print("KeyboardInterrupt")
except Exception as e:
    print(str(e))
finally:
    bus.shutdown()

    if DEBUG_VIRTUAL:
        v_bus.shutdown()

    proper_exit()
