import asyncio

from webserver.rest_api import app
from webserver.websocket import start_websocket


def start_socket() -> None:
    asyncio.run(start_websocket(None, 8765))

def start_rest_api() -> None:
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
