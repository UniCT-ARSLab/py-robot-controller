import socketio

sio = socketio.Client()
sio.connect('http://localhost:8000')

sio.emit('message', {'from': 'client'})


@sio.on('response')
def response(data):
    print(data)  # {'from': 'server'}

    sio.disconnect()
    exit(0)
