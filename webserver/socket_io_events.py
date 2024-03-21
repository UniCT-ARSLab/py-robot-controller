from flask_socketio import SocketIO


def define_socket_io_events(socketio: SocketIO) -> None:
    @socketio.on("connect")
    def on_connect() -> None:
        print("Web Client Connected (socketIO)")

    @socketio.on("disconnect")
    def on_disconnect() -> None:
        print("Web Client Disconnected (socketIO)")

    @socketio.on("ping")
    def on_ping() -> None:
        socketio.emit("pong")
        print("Web Client Pinged (socketIO)")

    # @socketio.on("message")
    # def on_message(arg) -> None:
    #     socketio.emit("pong mex", arg)
    #     print("Web Client Pinged MEX (socketIO)")
