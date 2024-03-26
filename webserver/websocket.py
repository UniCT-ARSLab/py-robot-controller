import asyncio
import json
from typing import Union

import websockets
from websockets import Data, WebSocketServerProtocol, serve

CLIENTS: set[WebSocketServerProtocol] = set()
clients_map = {}


async def handler(websocket: WebSocketServerProtocol) -> None:
    print("\n#########################")
    print("### new client connected")
    print("#########################\n")

    CLIENTS.add(websocket)

    try:
        await websocket.wait_closed()
    finally:
        CLIENTS.remove(websocket)


async def start_receive_from_client(websocket: WebSocketServerProtocol) -> None:
    try:
        message = await websocket.recv()

        handle_message(message)

        clients_map[websocket] = False
    except Exception as e:  # pylint: disable=unused-variable
        # print(f"error creating task for receiving message: {str(e)}")
        pass


def handle_message(message: Data) -> None:
    if message == "ALIGN":
        # robot.send_align()
        pass


async def websocket_loop() -> None:
    while True:
        # print(f"clients = {len(CLIENTS)}")
        websockets.broadcast(CLIENTS, get_lidar_data())
        websockets.broadcast(CLIENTS, get_robot_data())

        for websocket in CLIENTS:
            if websocket not in clients_map or clients_map[websocket] is False:
                asyncio.create_task(start_receive_from_client(websocket))
                clients_map[websocket] = True

        await asyncio.sleep(1) # delay


async def start_websocket(host: Union[str, None], port: int):
    async with serve(handler, host, port):
        await websocket_loop()


def get_lidar_data() -> str:
    laser_data_msg = {"type": "lidar", "data": "data"}  # robot.get_lidar_data(),
    return json.dumps(laser_data_msg)


def get_robot_data() -> str:
    robot_position_msg = {
        "type": "robot_data",
        "data": "data",  # robot.get_robot_data(),
    }
    return json.dumps(robot_position_msg)
