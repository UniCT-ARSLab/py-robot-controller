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
from utils.helper import proper_exit
from webserver.webserver import WebServer

# run webserver asynchronously in a separate thread
# threading.Thread(target=start_socket).start()

_bustype = "virtual" if DEBUG_VIRTUAL or DEBUG_VCAN else "socketcan"
_channel = VCHANNEL if DEBUG_VCAN else CHANNEL
bus = Bus(channel=_channel, bustype=_bustype, bitrate=CAN_BAUD)

if DEBUG_CAN or DEBUG_VIRTUAL or DEBUG_VCAN:
    v_bus = init_debug(bus, _bustype, _channel)

events = EventEmitter()
robot = Robot(events)
robot.init_lidar()

try:
    webServer = WebServer(host="0.0.0.0", port=5000, global_events=events)
    webServer.start()

    while True:
        robot.get_lidar_data()

        message = bus.recv()
        if DEBUG_CAN:
            print(message)

        if message is not None:
            time.sleep(5)
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
