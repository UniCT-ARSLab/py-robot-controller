import asyncio
import threading
from threading import Semaphore

from can import Message
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from pymitter import EventEmitter

from models.message_queue_events import MessageQueueEvents
from utils.helper import proper_exit
from webserver.routes import define_routes
from webserver.socket_io_events import define_socket_io_events
from webserver.websocket import start_websocket


def start_socket() -> None:
    asyncio.run(start_websocket(None, 8765))


class WebServer:

    def __init__(self, host: str, port: int, global_events: EventEmitter) -> None:
        self.host = host
        self.port = port

        self.flask_app = Flask(__name__)
        self.cors = CORS(self.flask_app)
        self.flask_app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
        self.flask_app.config["CORS_HEADERS"] = "Content-Type"

        self.socketio = SocketIO(self.flask_app, cors_allowed_origins="*")
        self.running_mutex = Semaphore(0)
        self.events = global_events

        self.events_management()

        define_routes(self.flask_app)
        define_socket_io_events(self.socketio)

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

    def events_management(self) -> None:
        self.events.on(MessageQueueEvents.NEW_CAN_PACKET.value, self.on_new_can_packet)
        pass

    def on_new_can_packet(self, payload: Message) -> None:
        print("EMITTED")
        self.socketio.emit(MessageQueueEvents.NEW_CAN_PACKET.value, str(payload))
