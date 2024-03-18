from models.interfaces import (
    DistanceSensor,
    Position,
    RobotStatus,
    StrategyCommand,
    Velocity,
)

CAN_IDS = {
    "ROBOT_POSITION": 0x3E3,
    "ROBOT_SPEED": 0x3E4,
    "OTHER_ROBOT_POSITION": 0x3E5,
    "ROBOT_STATUS": 0x402,
    "DISTANCE_SENSOR": 0x670,
    "MOTION_CMD": 0x7F0,
    "ST_CMD": 0x710,
    "OBST_MAP": 0x70F,
    "STRATEGY_COMMAND": 0x710,
}

MOTION_CMDS = {
    'STOP': 0x82,
    'BRAKE': 0x83,
    'SET_POSITION': 0x84,
    'FW_TO_DISTANCE': 0x85,
    'ROTATE_RELATIVE': 0x88,
    'SET_SPEED': 0x8C,
}

STRATEGY_CMDS = {
    "STRATEGY_COMMAND_ALIGN_GRANDE1": 0x01,
    "STRATEGY_COMMAND_ALIGN_PICCOLO": 0x03,
}

CAN_FORMATS = {
    "POSITION": "<hhhBB",
    "VELOCITY": "<hxxxxxx",
    "ROBOT_STATUS": "<ii",
    "DISTANCE_SENSOR": "<BHBxxxx",
    "ALIGN": "<BBhBBxx",
}

CAN_position: Position = {
    "X": 10,
    "Y": 20,
    "Angle": 300,
    "Flags": 0,
    "Bumpers": 0,
}

CAN_velocity: Velocity = {
    "linear_speed": 10
}

CAN_robot_status: RobotStatus = {
    "robot_selected": 10,
    "status_display": 20,
}

CAN_distance_sensor: DistanceSensor = {
    "sensor": 1,
    "distance": 10,
    "alarm": 2,
}


CAN_align: StrategyCommand = {
    "cmd": STRATEGY_CMDS["STRATEGY_COMMAND_ALIGN_GRANDE1"],
    "flags": 0,
    "elapsed_time": 0,
    "stgy": 1,
    "align": 1,
}
