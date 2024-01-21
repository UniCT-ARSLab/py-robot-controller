import asyncio
import threading

from rest_api import app
from websocket import start_websocket


def start_webservices() -> None:
    asyncio.run(start_websocket("localhost", 8765))
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

if __name__ == '__main__':
    start_webservices()