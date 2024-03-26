from typing import List

import eventlet

# this fix the missing socketio emitted events
eventlet.monkey_patch()  # pylint: disable=wrong-import-position

from threading import Semaphore, Thread

from can import Message
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from pymitter import EventEmitter

from models.message_queue_events import MessageQueueEvents
from utils.colors import bcolors, colorit
from utils.helper import proper_exit
from webserver.routes import define_routes


# pylint: disable=too-many-instance-attributes
class WebServer:

    def __init__(self, host: str, port: int, global_events: EventEmitter) -> None:
        self.host = host
        self.port = port

        self.flask_app = Flask(__name__)
        self.cors = CORS(self.flask_app)
        self.flask_app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
        self.flask_app.config["CORS_HEADERS"] = "Content-Type"

        self.socketio = SocketIO(
            self.flask_app, cors_allowed_origins="*", async_mode="eventlet"
        )
        self.running_mutex = Semaphore(0)
        self.events = global_events

        self.events_management()

        define_routes(self.flask_app)
        self.define_socket_io_events()

        self.main_thread = Thread(
            target=self.start_server, name="WebServerThread", daemon=True
        )

    def start(self) -> None:
        try:
            self.main_thread.start()
            print(colorit("Web Server Started", bcolors.OKBLUE))
            print(colorit(f"[http://127.0.0.1:{str(self.port)}]", bcolors.OKBLUE))
            # self.running_mutex.acquire()
        except KeyboardInterrupt:
            print(colorit("Web Server closed", bcolors.OKBLUE))
            # self.running_mutex.release()
            proper_exit()

    def start_server(self) -> None:
        try:
            self.socketio.run(
                self.flask_app,
                host=self.host,
                port=self.port,
                debug=False,
            )
        except KeyboardInterrupt:
            self.running_mutex.release()
            print(colorit("Web Server closed", bcolors.OKBLUE))
            proper_exit()

    def define_socket_io_events(self) -> None:
        @self.socketio.on("connect")
        def on_connect() -> None:
            print(colorit("Web Client Connected (socketIO)", bcolors.OKBLUE))
            self.socketio.emit("CONNECT")

        @self.socketio.on("disconnect")
        def on_disconnect() -> None:
            print(colorit("Web Client Disconnected (socketIO)", bcolors.OKBLUE))

        @self.socketio.on("ping")
        def on_ping() -> None:
            self.socketio.emit("pong")
            print(colorit("Web Client Pinged (socketIO)", bcolors.OKBLUE))

        @self.socketio.on("message")
        def on_message(message) -> None:
            self.socketio.emit("message pong")
            print(colorit(message, bcolors.OKBLUE))
            self.events.emit(MessageQueueEvents.NEW_CAN_PACKET.value, message)

        @self.socketio.on(MessageQueueEvents.SEND_ALIGN.value)
        def on_send_align(data) -> None:
            self.events.emit(MessageQueueEvents.SEND_ALIGN.value, data)

    def events_management(self) -> None:
        self.events.on(MessageQueueEvents.NEW_CAN_PACKET.value, self.on_new_can_packet)
        self.events.on(MessageQueueEvents.ROBOT_DATA.value, self.on_robot_data)
        self.events.on(MessageQueueEvents.LIDAR_DATA.value, self.on_lidar_data)

    def on_new_can_packet(self, payload: Message) -> None:
        self.socketio.emit(MessageQueueEvents.NEW_CAN_PACKET.value, str(payload))

    def on_robot_data(self, payload: dict) -> None:
        self.socketio.emit(MessageQueueEvents.ROBOT_DATA.value, payload)

    def on_lidar_data(self, payload: List[int]) -> None:
        self.socketio.emit(MessageQueueEvents.LIDAR_DATA.value, payload)
