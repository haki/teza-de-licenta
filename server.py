import socket
import sys
import cv2
import pickle
import numpy as np
import struct
from math import ceil
import requests
from tensorflow.keras.models import load_model

model = load_model('D:\\Desktop\\Universitate\\Teza\\NN_Self_Driving\\models\\model.h5')


def preProcess(img):
    img = img[54:120, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img


HOST = ''
PORT = 8485

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
lastSteering = 100
while True:
    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    frame = cv2.resize(frame, (240, 120))
    cv2.imshow('ImageWindow', frame)
    frame = np.asarray(frame)
    frame = preProcess(frame)
    frame = np.array([frame])

    steering = float(model.predict(frame))
    steeringInt = ceil(abs(steering))

    if lastSteering != steeringInt:
        print("Steering INT: {}".format(steeringInt))
        print("Steering: {}".format(steering))
        lastSteering = steeringInt
        url = "http://192.168.52.129:5000/{}".format(steeringInt)
        requests.get(url)

        if steeringInt == 0:
            print("STOP")
        elif steeringInt == 1:
            print("FORWARD")
        elif steeringInt == 2:
            print("BACK")
        elif steeringInt == 3:
            print("LEFT")
        elif steeringInt == 4:
            print("RIGHT")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
conn.close()
s.close()
url = "http://192.168.52.129:5000/0"
requests.get(url)
print('Socket closed')
sys.exit()
# End of file
