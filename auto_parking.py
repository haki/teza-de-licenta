import RPi.GPIO as GPIO  # Import GPIO library
import time
from MotorControl import MotorControl

motor = MotorControl()
TRIG = 17
ECHO = 18

ECHO2 = 22
TRIG2 = 23

GPIO.setup(TRIG, GPIO.OUT)  # initialize GPIO Pin as outputs
GPIO.setup(ECHO, GPIO.IN)  # initialize GPIO Pin as input
GPIO.setup(TRIG2, GPIO.OUT)  # initialize GPIO Pin as outputs
GPIO.setup(ECHO2, GPIO.IN)  # initialize GPIO Pin as input
time.sleep(5)

echo = 2


def dist():
    global echo
    GPIO.output(TRIG, False)  # Set TRIG as LOW
    time.sleep(0.1)  # Delay

    GPIO.output(TRIG, True)  # Set TRIG as HIGH
    time.sleep(0.00001)  # Delay of 0.00001 seconds
    GPIO.output(TRIG, False)  # Set TRIG as LOW

    while GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW
        pass  # Wait for ECHO to go HIGH
    pulse_start = time.time()

    while GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH
        pass  # Wait for ECHO to go LOW

    pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start  # time to get back the pulse to sensor

    distance = pulse_duration * 17150  # Multiply pulse duration by 17150 (34300/2) to get distance
    distance = round(distance, 2)  # Round to two decimal points
    return distance


def dist2():
    GPIO.output(TRIG2, False)  # Set TRIG as LOW
    time.sleep(0.1)  # Delay

    GPIO.output(TRIG2, True)  # Set TRIG as HIGH
    time.sleep(0.00001)  # Delay of 0.00001 seconds
    GPIO.output(TRIG2, False)  # Set TRIG as LOW

    while GPIO.input(ECHO2) == 0:  # Check whether the ECHO is LOW
        pass  # Wait for ECHO to go HIGH
    pulse_start = time.time()

    while GPIO.input(ECHO2) == 1:  # Check whether the ECHO is HIGH
        pass  # Wait for ECHO to go LOW

    pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start  # time to get back the pulse to sensor

    distance = pulse_duration * 17150  # Multiply pulse duration by 17150 (34300/2) to get distance
    distance = round(distance, 2)  # Round to two decimal points
    print(distance)
    return distance


def main():
    p = 0
    motor.forward()
    print("Inainte")
    while True:
        if (p == 1):
            motor.stop()
            print("Stop")

            now = time.time()
            while (time.time() <= now + 1.2):
                motor.turn_left()
                print("Intoarce la stanga")
                time.sleep(1.6)
            motor.stop()
            print("Stop")
            now = time.time()
            stop = 0
            distance2 = dist2()
            while (distance2 > 18):
                time.sleep(0.1)
                motor.backward()
                print("Inapoi")
                distance2 = dist2()
                print("Senzor din spate: {}cm".format(distance2))

            print("A intrat in parcare")
            motor.stop()
            print("Stop")
            break
        distance = dist()

        if (distance > 30):

            now = time.time()
            while (time.time() <= now + 0.3):
                distance = dist()
                print("Senzor din dreapta: {}cm".format(distance))
                if (distance < 30):
                    p = 0
                    break
                p = 1
