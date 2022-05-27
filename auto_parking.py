import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
import time  # Import the time library
from MotorControl import MotorControl  # Import the MotorControl library

motor = MotorControl()  # Create an instance of the MotorControl class
TRIG = 17  # Set GPIO pin 17 as the TRIG pin
ECHO = 18  # Set GPIO pin 18 as the ECHO pin

ECHO2 = 22  # Set GPIO pin 22 as the ECHO pin
TRIG2 = 23  # Set GPIO pin 23 as the TRIG pin

GPIO.setup(TRIG, GPIO.OUT)  # Set pin as GPIO out
GPIO.setup(ECHO, GPIO.IN)  # Set pin as GPIO in
GPIO.setup(TRIG2, GPIO.OUT)  # Set pin as GPIO out
GPIO.setup(ECHO2, GPIO.IN)  # Set pin as GPIO in
time.sleep(5)  # Wait 5 seconds for sensors to initialize

echo = 2  # Set echo to 2


def dist():  # Function to calculate distance of ultrasonic sensor
    global echo  # Set echo to global variable
    GPIO.output(TRIG, False)  # Set TRIG as LOW
    time.sleep(0.1)  # Delay of 0.1 seconds

    GPIO.output(TRIG, True)  # Set TRIG as HIGH
    time.sleep(0.00001)  # Delay of 0.00001 seconds
    GPIO.output(TRIG, False)  # Set TRIG as LOW

    while GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW
        pass  # Wait for ECHO to go HIGH
    pulse_start = time.time()  # Saves the last known time of LOW pulse

    while GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH
        pass  # Wait for ECHO to go LOW

    pulse_end = time.time()  # Saves the last known time of HIGH pulse
    pulse_duration = pulse_end - pulse_start  # time to get back the pulse to sensor

    distance = pulse_duration * 17150  # Multiply pulse duration by 17150 (34300/2) to get distance
    distance = round(distance, 2)  # Round to two decimal points
    return distance  # Return the distance of ultrasonic sensor


def dist2():  # Function to calculate distance of ultrasonic sensor
    GPIO.output(TRIG2, False)  # Set TRIG as LOW
    time.sleep(0.1)  # Delay of 0.1 seconds

    GPIO.output(TRIG2, True)  # Set TRIG as HIGH
    time.sleep(0.00001)  # Delay of 0.00001 seconds
    GPIO.output(TRIG2, False)  # Set TRIG as LOW

    while GPIO.input(ECHO2) == 0:  # Check whether the ECHO is LOW
        pass  # Wait for ECHO to go HIGH
    pulse_start = time.time()  # Saves the last known time of LOW pulse

    while GPIO.input(ECHO2) == 1:  # Check whether the ECHO is HIGH
        pass  # Wait for ECHO to go LOW

    pulse_end = time.time()  # Saves the last known time of HIGH pulse
    pulse_duration = pulse_end - pulse_start  # time to get back the pulse to sensor

    distance = pulse_duration * 17150  # Multiply pulse duration by 17150 (34300/2) to get distance
    distance = round(distance, 2)  # Round to two decimal points
    print(distance)  # Print the distance of ultrasonic sensor
    return distance  # Return the distance of ultrasonic sensor


def main():  # Main function
    p = 0  # Set p to 0
    motor.forward()  # Move forward
    print("Inainte")  # Print message
    while True:  # Loop forever
        if (p == 1):  # If p is 1
            motor.stop()  # Stop the motor
            print("Stop")  # Print message

            now = time.time()  # Get the current time
            while (
                    time.time() <= now + 1.2):  # Loop until the current time is greater than the current time plus 1.2 seconds
                motor.turn_left()  # Turn left
                print("Intoarce la stanga")  # Print message
                time.sleep(1.6)  # Wait 1.6 seconds
            motor.stop()  # Stop the motor
            print("Stop")  # Print message
            now = time.time()  # Get the current time
            stop = 0  # Set stop to 0
            distance2 = dist2()  # Get the distance of ultrasonic sensor
            while (distance2 > 18):  # Loop until the distance of ultrasonic sensor is greater than 18
                time.sleep(0.1)  # Wait 0.1 seconds
                motor.backward()  # Move backward
                print("Inapoi")  # Print message
                distance2 = dist2()  # Get the distance of ultrasonic sensor
                print("Senzor din spate: {}cm".format(distance2))  # Print message

            print("A intrat in parcare")  # Print message
            motor.stop()  # Stop the motor
            print("Stop")  # Print message
            break
        distance = dist()  # Get the distance of ultrasonic sensor

        if (distance > 30):  # If the distance of ultrasonic sensor is greater than 30

            now = time.time()  # Get the current time
            while (
                    time.time() <= now + 0.3):  # Loop until the current time is greater than the current time plus 0.3 seconds
                distance = dist()  # Get the distance of ultrasonic sensor
                print("Senzor din dreapta: {}cm".format(distance))  # Print message
                if (distance < 30):  # If the distance of ultrasonic sensor is less than 30
                    p = 0  # Set p to 0
                    break  # Break the loop
                p = 1  # Set p to 1
