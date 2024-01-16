from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# Get robot position
@app.route('/robot/position', methods=['GET'])
def get_robot_position():
    pass

# Set robot position
@app.route('/robot/position', methods=['POST'])
def set_robot_position():
    pass

# Get robot battery percentage
@app.route('/robot/battery', methods=['GET'])
def get_robot_battery():
    pass

# Reset robot context
@app.route('/robot/reset', methods=['GET'])
def reset_robot_context():
    pass

# Get robot speed
@app.route('/robot/speed', methods=['GET'])
def get_robot_speed():
    pass

# Set robot speed
@app.route('/robot/speed', methods=['POST'])
def set_robot_speed():
    pass

# Move robot forward by a certain distance
@app.route('/robot/move/distance', methods=['POST'])
def robot_forward_distance():
    pass

# Move robot forward to a specific point
@app.route('/robot/move/point', methods=['POST'])
def robot_forward_point():
    pass

# Rotate robot relative to its current orientation
@app.route('/robot/rotate/relative', methods=['POST'])
def robot_relative_rotation():
    pass

# Rotate robot to an absolute angle
@app.route('/robot/rotate/absolute', methods=['POST'])
def robot_absolute_rotation():
    pass

# Stop robot motors
@app.route('/robot/motors/stop', methods=['POST'])
def send_stop():
    pass

# Align robot to a specified color
@app.route('/robot/st/align', methods=['POST'])
def robot_align():
    pass

# Toggle robot starter (enable/disable)
@app.route('/robot/st/starter', methods=['POST'])
def robot_starter_toggle():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)