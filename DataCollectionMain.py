import WebcamModule as wM
import DataCollectionModule as dcM
import KeyPressModule as kpM
from MotorControl import MotorControl
import cv2
from time import sleep

motor = MotorControl()

record = 0
while True:
    kpM.init()
    if kpM.getKey("UP"):
        motor.forward()
        steering = 1
    elif kpM.getKey("DOWN"):
        motor.backward()
        steering = 2
    elif kpM.getKey("LEFT"):
        motor.turn_left()
        steering = 3
    elif kpM.getKey("RIGHT"):
        motor.turn_right()
        steering = 4
    else:
        steering = 0
        motor.stop()
    if kpM.getKey("SPACE"):
        if record == 0:
            print('Recording Started ...')
        record += 1
        sleep(0.300)
    if record == 1:
        img = wM.getImg(True, size=[240, 120])
        dcM.saveData(img, steering)
    elif record == 2:
        dcM.saveLog()
        record = 0
    cv2.waitKey(1)