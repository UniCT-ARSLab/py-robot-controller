from typing import List, Literal

from models.interfaces import Position

MessageType = Literal['lidar', 'position']

position_mocks: List[Position] = [
    {"X": 100, "Y": 200, "Angle": 90, "Flags": 0, "Bumpers": 0},
    {"X": 500, "Y": 600, "Angle": 180, "Flags": 0, "Bumpers": 0},
    {"X": 800, "Y": 800, "Angle": 270, "Flags": 0, "Bumpers": 0},
    {"X": 2000, "Y": 2000, "Angle": 360, "Flags": 0, "Bumpers": 0},
    {"X": 3000, "Y": 2000, "Angle": 90, "Flags": 0, "Bumpers": 0},
]
