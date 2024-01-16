import struct

import can

from robot.constants import DEBUG_CAN, ID_ROBOT_POSITION


class Robot:
    def __init__(self):
        # Initialize the starting and current positions of the robot
        self.StartPosition = {"X": -1000, "Y": -1000, "Angle": 0}
        self.Position = {"X": 0, "Y": 0, "Angle": 0}

    def on_data_received(self, frm: can.Message):
        # Extract data from the CAN message
        data = frm.data

        if frm.arbitration_id == ID_ROBOT_POSITION:
            posX, posY, angle = struct.unpack("<hhh", data[:6])

            # Convert the angle to a float by dividing by 100
            angle /= 100.0

            # Update the robot's position information
            if self.StartPosition["X"] < -999:
                self.StartPosition["X"] = posX
                self.StartPosition["Y"] = posY
                self.StartPosition["Angle"] = angle

            self.Position["X"] = posX
            self.Position["Y"] = posY
            self.Position["Angle"] = angle

            if DEBUG_CAN:
                print(f"Position: [X: {posX}, Y: {posY}, A: {angle}]")
