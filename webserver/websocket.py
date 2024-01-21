
import asyncio
import json

import websockets
from websockets import WebSocketServerProtocol, serve

from robot.robot import robot

CLIENTS = set()

async def handler(websocket: WebSocketServerProtocol):
    CLIENTS.add(websocket)

    try:
        await websocket.wait_closed()
    finally:
        CLIENTS.remove(websocket)

async def broadcast():
    while True:
        print(f"clients = {len(CLIENTS)}")
        message = 'this is a broadcast message'
        websockets.broadcast(CLIENTS, message)
        websockets.broadcast(CLIENTS, get_lidar_data())
        await asyncio.sleep(1) # delay
        print()

async def start_websocket(host: str, port: int):
    async with serve(handler, host, port):
        await broadcast()

def get_lidar_data() -> str:
    laser_data_msg = {
        "type": "lidar",
        "data": robot.get_lidar_data(),
    }
    return json.dumps(laser_data_msg)
