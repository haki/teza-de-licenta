import WebcamModule as wM  # Webcam Module
import DataCollectionModule as dcM  # Data Collection Module
import KeyPressModule as kpM  # Key Press Module
from MotorControl import MotorControl  # Motor Control Module
import cv2  # OpenCV
from time import sleep  # Sleep

motor = MotorControl()  # Initialize Motor Control

record = 0  # Initialize Record
while True:
    kpM.init()  # Initialize Key Press Module
    if kpM.getKey("UP"):  # If Up Key is Pressed
        motor.forward()  # Move Forward
        steering = 1  # Set Steering to 1
    elif kpM.getKey("DOWN"):  # If Down Key is Pressed
        motor.backward()  # Move Backward
        steering = 2  # Set Steering to 2
    elif kpM.getKey("LEFT"):  # If Left Key is Pressed
        motor.turn_left()  # Turn Left
        steering = 3  # Set Steering to 3
    elif kpM.getKey("RIGHT"):  # If Right Key is Pressed
        motor.turn_right()  # Turn Right
        steering = 4  # Set Steering to 4
    else:  # If No Key is Pressed
        steering = 0  # Set Steering to 0
        motor.stop()  # Stop
    if kpM.getKey("SPACE"):  # If Spacebar is Pressed
        if record == 0:  # If Record is 0
            print('Recording Started ...')  # Print
        record += 1  # Increment Record
        sleep(0.300)  # Sleep 300ms
    if record == 1:  # If Record is 1 (Recording)
        img = wM.getImg(True, size=[240, 120])  # Get Image from Webcam
        dcM.saveData(img, steering)  # Save Data
    elif record == 2:  # If Record is 2
        dcM.saveLog()  # Save Log
        record = 0  # Reset Record
    cv2.waitKey(1)  # Wait 1ms
