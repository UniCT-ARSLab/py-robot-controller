from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def index():
    return "index"


@socketio.on("message")
def handle_message(data):
    print("received message: " + data)


@socketio.on("connect")
def on_connect():
    socketio.emit("Hello World")
    print("Web Client Connected (socketIO)")


@socketio.on("disconnect")
def on_disconnect():
    print("Web Client Disconnected (socketIO)")


@socketio.on("ping")
def on_ping():
    socketio.emit("pong")
    print("Web Client Pinged (socketIO)")


if __name__ == "__main__":
    socketio.run(app)
