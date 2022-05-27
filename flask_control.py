from flask import Flask
from MotorControl import MotorControl
import auto_parking as ap

app = Flask(__name__)
motor = MotorControl()
parking = False


@app.route('/<int:control>')
def hello_world(control):
    if control == 0:
        motor.stop()
    elif control == 1:
        motor.forward()
    elif control == 2:
        motor.backward()
    elif control == 3:
        motor.turn_left()
    elif control == 4:
        motor.turn_right()
    else:
        motor.stop()
    return 'Hello World!'


@app.route('/parking')
def park():
    global parking
    if not parking:
        parking = True
        ap.main()
    parking = False
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, host='192.168.52.129', port=5000)