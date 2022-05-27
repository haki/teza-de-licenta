import socket  # Import socket module
import sys  # Import sys module
import cv2  # Import cv2 module
import pickle  # Import pickle module
import numpy as np  # Import numpy module
import struct  # Import struct module
from math import ceil  # Import ceil module
import requests  # Import requests module
from tensorflow.keras.models import load_model  # Import load_model module

model = load_model('D:\\Desktop\\Universitate\\Teza\\NN_Self_Driving\\models\\model.h5')  # Load model from disk

client_address = "192.168.52.129"  # Set client address


def preProcess(img):  # Function to preprocess image
    img = img[54:120, :, :]  # Crop image
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)  # Convert image to YUV color space
    img = cv2.GaussianBlur(img, (3, 3), 0)  # Apply Gaussian blur
    img = cv2.resize(img, (200, 66))  # Resize image
    img = img / 255  # Normalize image
    return img  # Return image


HOST = ''  # Symbolic name meaning all available interfaces
PORT = 8485  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
print('Socket created')  # Print message

s.bind((HOST, PORT))  # Bind to the port
print('Socket bind complete')  # Print message
s.listen(10)  # Listen for connections
print('Socket now listening')  # Print message

conn, addr = s.accept()  # Establish connection with client

data = b""  # Initialize data variable as byte
payload_size = struct.calcsize(">L")  # Initialize payload size variable >L is unsigned long and L is long
print("payload_size: {}".format(payload_size))  # Print message
lastSteering = 100  # Initialize last steering variable
while True:
    while len(data) < payload_size:  # While data is less than payload size
        data += conn.recv(4096)  # Receive data from client

    packed_msg_size = data[:payload_size]  # Get first 4 bytes
    data = data[payload_size:]  # Remove first 4 bytes from data
    msg_size = struct.unpack(">L", packed_msg_size)[0]  # Unpack first 4 bytes
    while len(data) < msg_size:
        data += conn.recv(4096)  # Receive data from client
    frame_data = data[:msg_size]  # Get first frame
    data = data[msg_size:]  # Remove first frame from data

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")  # Load frame from byte
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)  # Decode frame color from byte
    frame = cv2.resize(frame, (240, 120))  # Resize frame 240x120 pixels
    cv2.imshow('ImageWindow', frame)  # Show frame
    frame = np.asarray(frame)  # Convert frame to array
    frame = preProcess(frame)  # Preprocess frame
    frame = np.array([frame])  # Convert frame to array

    steering = float(model.predict(frame))  # Predict steering angle
    steeringInt = ceil(abs(steering))  # Convert steering angle to integer

    if lastSteering != steeringInt:  # If last steering angle is not equal to current steering angle
        print("Steering INT: {}".format(steeringInt))  # Print message
        print("Steering: {}".format(steering))  # Print message
        lastSteering = steeringInt  # Set last steering angle to current steering angle
        url = "http://" + client_address + ":5000 / {}".format(steeringInt)  # Set url to send to server
        requests.get(url)  # Send url to server

        if steeringInt == 0:  # If steering angle is 0
            print("STOP")  # Print message
        elif steeringInt == 1:  # If steering angle is 1
            print("FORWARD")  # Print message
        elif steeringInt == 2:  # If steering angle is 2
            print("BACK")  # Print message
        elif steeringInt == 3:  # If steering angle is 3
            print("LEFT")  # Print message
        elif steeringInt == 4:  # If steering angle is 4
            print("RIGHT")  # Print message

    if cv2.waitKey(1) & 0xFF == ord('q'):  # If q is pressed
        break  # Break loop

cv2.destroyAllWindows()  # Destroy all windows
conn.close()  # Close connection
s.close()  # Close socket
url = "http://" + client_address + ":5000/0"  # Set url to send to server
requests.get(url)  # Send url to server
print('Socket closed')  # Print message
sys.exit()  # Exit program
# End of file
