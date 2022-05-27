import RPi.GPIO as GPIO
import time
from modules.MotorControl import MotorControl
import cv2


class ObstacleDetection:
    def __init__(self, motor):
        print("Obstacle Detection")
        self.motor = motor
        self.TRIG = 23
        self.ECHO = 22

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    def dist(self):
        GPIO.output(self.TRIG, False)  # Set TRIG as LOW
        time.sleep(0.1)  # Delay

        GPIO.output(self.TRIG, True)  # Set TRIG as HIGH
        time.sleep(0.00001)  # Delay of 0.00001 seconds
        GPIO.output(self.TRIG, False)  # Set TRIG as LOW

        while GPIO.input(self.ECHO) == 0:  # Check whether the ECHO is LOW
            pass  # Wait for ECHO to go HIGH
        pulse_start = time.time()

        while GPIO.input(self.ECHO) == 1:  # Check whether the ECHO is HIGH
            pass  # Wait for ECHO to go LOW

        pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start  # time to get back the pulse to sensor

        distance = pulse_duration * 17150  # Multiply pulse duration by 17150 (34300/2) to get distance
        distance = round(distance, 2)  # Round to two decimal points
        return distance

    def start(self):
        Car_cascade = cv2.CascadeClassifier('cars.xml')
        cap = cv2.VideoCapture(0)
        # reduce the resolution to increase the FPS
        cap.set(3, 320)
        cap.set(4, 240)
        obstacle = False
        timeNow = time.time()
        while True:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            Cars = Car_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in Cars:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                motor.stop()

            cv2.imshow('img', img)

            distance = self.dist()
            print("Distance:", distance, "cm")
            if distance < 30:
                print("Obstacle detected")
                self.motor.forward()
                time.sleep(2)
                obstacle = True

            if distance > 30 and obstacle:
                print("Obstacle cleared")
                obstacle = False
                print("Turning Left")
                self.motor.turn_left()
                time.sleep(5)
            else:
                self.motor.backward()

            if timeNow + 30 < time.time():
                self.motor.stop()
                print("Time up")
                break


if __name__ == "__main__":
    motor = MotorControl()
    obstacle = ObstacleDetection(motor)
    obstacle.start()