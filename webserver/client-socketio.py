import socketio

sio = socketio.Client()

sio.connect("http://localhost:5000")


@sio.event
def connect():
    print("connection established")
    sio.emit("my message", {"foo": "bar"})


@sio.event
def my_message(data):
    print("message received with ", data)
    sio.emit("my response", {"response": "my response"})


@sio.event
def disconnect():
    print("disconnected from server")


# sio.wait()
print("test")
sio.emit("ping", {"foo": "bar"})
sio.emit("message", {"foox": "barx"})
print("test2")

sio.emit("message", {"from": "client"})


@sio.on("response")
def response(data):
    print(data)  # {'from': 'server'}
