import logging

from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@socketio.on('message')
def message(data):
    print("####################")
    print(data)  # {'from': 'client'}
    print("####################")
    emit('response', {'from': 'server'})


@socketio.on("connect")
def on_connect():
    socketio.emit("Hello World")
    print("Web Client Connected (socketIO)")


if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True)
