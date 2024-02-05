from websockets.sync.client import connect


def test_websocket_connection():
    with connect("ws://localhost:8765") as websocket:
        message = websocket.recv()
        assert "data" in message
