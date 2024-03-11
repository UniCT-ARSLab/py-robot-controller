import asyncio
import json
from typing import Union

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
        # print(f"clients = {len(CLIENTS)}")
        websockets.broadcast(CLIENTS, get_lidar_data())
        websockets.broadcast(CLIENTS, get_robot_data())

        for websocket in CLIENTS:
            message = await websocket.recv()
            print(message)
            if message == "ALIGN":
                print("## align received!")

        await asyncio.sleep(1) # delay


async def start_websocket(host: Union[str, None], port: int):
    async with serve(handler, host, port):
        await broadcast()


def get_lidar_data() -> str:
    laser_data_msg = {
        "type": "lidar",
        "data": robot.get_lidar_data(),
    }
    return json.dumps(laser_data_msg)


def get_robot_data() -> str:
    robot_position_msg = {
        "type": "robot_data",
        "data": robot.get_robot_data(),
    }
    return json.dumps(robot_position_msg)
