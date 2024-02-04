from typing import Literal

MessageType = Literal['lidar', 'position']

position_mocks = [
    { "X": 100, "Y": 200, "Angle": 90 },
    { "X": 500, "Y": 600, "Angle": 180 },
    { "X": 800, "Y": 800, "Angle": 270 },
    { "X": 2000, "Y": 2000, "Angle": 360 },
    { "X": 3000, "Y": 2000, "Angle": 90 },
]
