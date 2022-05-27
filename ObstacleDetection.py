import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
import time  # Import the time library
from modules.MotorControl import MotorControl  # Import the MotorControl class
import cv2  # Import OpenCV library


class ObstacleDetection:  # Define the class
    def __init__(self, motor):  # Define the constructor
        print("Obstacle Detection")  # Print a message
        self.motor = motor  # Assign the motor variable to the motor variable in the class
        self.TRIG = 23  # Trigger
        self.ECHO = 22  # Echo

        GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
        GPIO.setup(self.TRIG, GPIO.OUT)  # Set pin as GPIO out
        GPIO.setup(self.ECHO, GPIO.IN)  # Set pin as GPIO in

    def dist(self):  # Define the distance function
        GPIO.output(self.TRIG, False)  # Set TRIG as LOW
        time.sleep(0.1)  # Delay

        GPIO.output(self.TRIG, True)  # Set TRIG as HIGH
        time.sleep(0.00001)  # Delay of 0.00001 seconds
        GPIO.output(self.TRIG, False)  # Set TRIG as LOW

        while GPIO.input(self.ECHO) == 0:  # Check whether the ECHO is LOW
            pass  # Wait for ECHO to go HIGH
        pulse_start = time.time()  # Saves the last known time of LOW pulse

        while GPIO.input(self.ECHO) == 1:  # Check whether the ECHO is HIGH
            pass  # Wait for ECHO to go LOW

        pulse_end = time.time()  # Saves the last known time of HIGH pulse
        pulse_duration = pulse_end - pulse_start  # time to get back the pulse to sensor

        distance = pulse_duration * 17150  # Multiply pulse duration by 17150 (34300/2) to get distance
        distance = round(distance, 2)  # Round to two decimal points
        return distance  # Return the distance

    def start(self):  # Define the start function
        Car_cascade = cv2.CascadeClassifier(
            'cars.xml')  # Load the car cascade file for detecting cars in the video stream
        cap = cv2.VideoCapture(0)  # Capture the video from the camera
        # reduce the resolution to increase the FPS
        cap.set(3, 320)  # Width
        cap.set(4, 240)  # Height
        obstacle = False  # Set the obstacle variable to false
        timeNow = time.time()  # Get the current time
        while True:
            ret, img = cap.read()  # Read the frame from the camera
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale

            Cars = Car_cascade.detectMultiScale(gray, 1.3, 5)  # Detect the cars in the frame
            for (x, y, w, h) in Cars:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Draw a rectangle around the car
                motor.stop()  # Stop the motor

            cv2.imshow('img', img)  # Show the frame

            distance = self.dist()  # Get the distance
            print("Distance:", distance, "cm")  # Print the distance
            if distance < 30:  # If the distance is less than 30 cm
                print("Obstacle detected")  # Print a message
                self.motor.forward()  # Move forward
                time.sleep(2)  # Wait for 2 seconds
                obstacle = True  # Set the obstacle variable to true

            if distance > 30 and obstacle:  # If the distance is greater than 30 cm and the obstacle variable is true
                print("Obstacle cleared")  # Print a message
                obstacle = False  # Set the obstacle variable to false
                print("Turning Left")  # Print a message
                self.motor.turn_left()  # Turn left
                time.sleep(5)  # Wait for 5 seconds
            else:  # If the distance is greater than 30 cm and the obstacle variable is false
                self.motor.backward()  # Move backward

            if timeNow + 30 < time.time():  # If the current time is greater than 30 seconds
                self.motor.stop()  # Stop the motor
                print("Time up")  # Print a message
                break  # Break the loop


if __name__ == "__main__":  # If the script is run directly
    motor = MotorControl()  # Create an object of the MotorControl class
    obstacle = ObstacleDetection(motor)  # Create an object of the ObstacleDetection class
    obstacle.start()  # Start the obstacle detection
