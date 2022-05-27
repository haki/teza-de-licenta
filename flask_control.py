from flask import Flask  # Import Flask
from MotorControl import MotorControl  # Import MotorControl
import auto_parking as ap  # Import auto_parking

app = Flask(__name__)  # Create an instance of Flask
motor = MotorControl()  # Create an instance of MotorControl
parking = False  # Set parking to False


@app.route('/<int:control>')  # Route for the control
def hello_world(control):  # Function for the control
    if control == 0:  # If control is 0
        motor.stop()  # Stop the motor
    elif control == 1:  # If control is 1
        motor.forward()  # Move forward
    elif control == 2:  # If control is 2
        motor.backward()  # Move backward
    elif control == 3:  # If control is 3
        motor.turn_left()  # Turn left
    elif control == 4:  # If control is 4
        motor.turn_right()  # Turn right
    else:  # If control is not 0, 1, 2, 3, or 4
        motor.stop()  # Stop the motor
    return 'Hello World!'  # Return 'Hello World!'


@app.route('/parking')  # Route for the parking
def park():  # Function for the parking
    global parking  # Set parking to global
    if not parking:  # If parking is not True
        parking = True  # Set parking to True
        ap.main()  # Run auto_parking
    parking = False  # Set parking to False
    return 'Hello World!'  # Return 'Hello World!'


if __name__ == '__main__':  # If the file is run directly
    app.run(debug=True, host='192.168.52.129', port=5000)  # Run the app on port 5000 and host
