import struct

import can

from robot.constants import DEBUG_CAN, CAN_IDS


class Robot:
    def __init__(self):
        # Initialize the starting and current positions of the robot
        self.StartPosition = {"X": -1000, "Y": -1000, "Angle": 0}
        self.Position = {"X": 0, "Y": 0, "Angle": 0}

    def on_data_received(self, frm: can.Message):
        # Extract data from the CAN message
        data = frm.data

        if frm.arbitration_id not in CAN_IDS.values():
            print(f"Unknown CAN ID: {frm.arbitration_id}")
            return

        if frm.arbitration_id == CAN_IDS["ID_ROBOT_POSITION"]:
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

            if DEBUG_CAN: # debug can viene usata per scopi diversi (switch da virtual a socket / logging), forse serve un altro flag
                print(f"Position: [X: {posX}, Y: {posY}, A: {angle}]")
                
    def get_position(self):
        return self.Position