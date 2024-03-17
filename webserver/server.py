from flask import Flask
from flask_socketio import SocketIO, emit
import logging

app = Flask(__name__)
socketio = SocketIO(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@socketio.on('message')
def message(data):
    print(data)  # {'from': 'client'}
    emit('response', {'from': 'server'})


if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True)
