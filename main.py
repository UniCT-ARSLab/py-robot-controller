import time

from can.interface import Bus
from pymitter import EventEmitter

from models.debug_messages import init_debug
from models.message_queue_events import MessageQueueEvents
from robot.config import (
    CAN_BAUD,
    CHANNEL,
    DEBUG_CAN,
    DEBUG_CYCLE,
    DEBUG_VCAN,
    DEBUG_VIRTUAL,
    VCHANNEL,
)
from robot.robot import Robot
from utils.colors import bcolors, colorit
from utils.helper import proper_exit
from webserver.webserver import WebServer

_bustype = "virtual" if DEBUG_VIRTUAL or DEBUG_VCAN else "socketcan"
_channel = VCHANNEL if DEBUG_VCAN else CHANNEL
bus = Bus(channel=_channel, bustype=_bustype, bitrate=CAN_BAUD)

events = EventEmitter()
robot = Robot(bus, events)

try:
    webServer = WebServer(host="0.0.0.0", port=5000, global_events=events)
    webServer.start()

    if DEBUG_VIRTUAL:
        time.sleep(5)  # wait that the web clients connection

    if DEBUG_CAN or DEBUG_VIRTUAL or DEBUG_VCAN:
        v_bus = init_debug(bus, _bustype, _channel, events)

    while True:
        message = bus.recv()  # potential bottle-neck

        if message is not None:
            events.emit(MessageQueueEvents.NEW_CAN_PACKET.value, message)

        if DEBUG_CAN:
            print(colorit(str(message), bcolors.OKCYAN))

        if DEBUG_CYCLE:
            events.emit(MessageQueueEvents.END_CYCLE.value)
            time.sleep(1)

except KeyboardInterrupt:
    print(colorit("KeyboardInterrupt", bcolors.FAIL))
except Exception as e:
    print(colorit(str(e), bcolors.FAIL))
finally:
    bus.shutdown()

    if DEBUG_VIRTUAL:
        v_bus.shutdown()

    proper_exit()
