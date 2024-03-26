import threading
from threading import Semaphore

import eventlet
from can import Message
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from pymitter import EventEmitter

from models.message_queue_events import MessageQueueEvents
from utils.helper import proper_exit
from webserver.routes import define_routes

eventlet.monkey_patch()  # this fix the missing socketio emitted events

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

        self.main_thread = threading.Thread(
            target=self.start_server, name="WebServerThread", daemon=True
        )

    def start(self) -> None:
        try:
            self.main_thread.start()
            print("Web Server Started")
            print(f"[http://127.0.0.1:{str(self.port)}]")
            # self.running_mutex.acquire()
        except KeyboardInterrupt:
            print("Web Server closed")
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
            print("Web Server closed")
            proper_exit()

    def define_socket_io_events(self) -> None:
        @self.socketio.on("connect")
        def on_connect() -> None:
            print("Web Client Connected (socketIO)")
            self.socketio.emit("CONNECT")

        @self.socketio.on("disconnect")
        def on_disconnect() -> None:
            print("Web Client Disconnected (socketIO)")

        @self.socketio.on("ping")
        def on_ping() -> None:
            self.socketio.emit("pong")
            print("Web Client Pinged (socketIO)")

        @self.socketio.on("message")
        def on_message(message) -> None:
            self.socketio.emit("message pong")
            print(message)
            self.events.emit(MessageQueueEvents.NEW_CAN_PACKET.value, message)

    def events_management(self) -> None:
        self.events.on(MessageQueueEvents.NEW_CAN_PACKET.value, self.on_new_can_packet)

    def on_new_can_packet(self, payload: Message) -> None:
        self.socketio.emit(MessageQueueEvents.NEW_CAN_PACKET.value, str(payload))
