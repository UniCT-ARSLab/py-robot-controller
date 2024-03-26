from flask import Flask
from flask_cors import cross_origin

from models.constants import HEALTHCHECK_MESSAGE


def define_routes(flask_app: Flask) -> None:

    @flask_app.get("/ping")
    @cross_origin()
    def ping():
        return {"error": False}

    # healthcheck
    @flask_app.get("/healthcheck")
    @cross_origin()
    def healthcheck() -> str:
        return HEALTHCHECK_MESSAGE

    # Get robot position
    @flask_app.get("/robot/position")
    @cross_origin()
    def get_robot_position():
        pass

    # Set robot position
    @flask_app.post("/robot/position")
    @cross_origin()
    def set_robot_position():
        pass

    # Get robot battery percentage
    @flask_app.get("/robot/battery")
    @cross_origin()
    def get_robot_battery():
        pass

    # Reset robot context
    @flask_app.get("/robot/reset")
    @cross_origin()
    def reset_robot_context():
        pass

    # Get robot speed
    @flask_app.get("/robot/speed")
    @cross_origin()
    def get_robot_speed():
        pass

    # Set robot speed
    @flask_app.post("/robot/speed")
    @cross_origin()
    def set_robot_speed():
        pass

    # Move robot forward by a certain distance
    @flask_app.post("/robot/move/distance")
    @cross_origin()
    def robot_forward_distance():
        pass

    # Move robot forward to a specific point
    @flask_app.post("/robot/move/point")
    @cross_origin()
    def robot_forward_point():
        pass

    # Rotate robot relative to its current orientation
    @flask_app.post("/robot/rotate/relative")
    @cross_origin()
    def robot_relative_rotation():
        pass

    # Rotate robot to an absolute angle
    @flask_app.post("/robot/rotate/absolute")
    @cross_origin()
    def robot_absolute_rotation():
        pass

    # Stop robot motors
    @flask_app.post("/robot/motors/stop")
    @cross_origin()
    def send_stop():
        pass

    # Align robot to a specified color
    @flask_app.post("/robot/st/align")
    @cross_origin()
    def robot_align():
        pass

    # Toggle robot starter (enable/disable)
    @flask_app.post("/robot/st/starter")
    @cross_origin()
    def robot_starter_toggle():
        pass
