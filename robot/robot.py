import can
import struct

class Robot:
    def __init__(self):
        # Initialize the starting and current positions of the robot
        self.StartPosition = {"X": -1000, "Y": -1000, "Angle": 0}
        self.Position = {"X": 0, "Y": 0, "Angle": 0}

    def on_data_received(self, frm):
        # Extract data from the CAN message
        data = frm.data

        # Check if the message ID matches the expected ID for robot position
        if frm.arbitration_id == ID_ROBOT_POSITION:
            # Unpack the data using the struct module
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

            # Print the received position information for debugging
            if DEBUG_CAN:
                print(f"Position: [X: {posX}, Y: {posY}, A: {angle}]")

# Constants
ID_ROBOT_POSITION = 0x3e3
DEBUG_CAN = True

# Create an instance of the Robot class
robot = Robot()

# Create a bus instance
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Enter a loop to receive messages
while True:
    # Receive a CAN message
    message = bus.recv()

    # Check if the message is a valid CAN message
    if message is not None:
        # Handle the received message
        robot.on_data_received(message)
