import cv2  # OpenCV 3.0
import numpy as np  # Numpy for matrix operations and array operations in Python (e.g. np.array)
from tensorflow.keras.models import load_model  # TensorFlow Keras Model Load Function (Loads the Model)
import modules.WebcamModule as wM  # WebcamModule (Webcam Module)

#######################################
model = load_model('D:\\Desktop\\Universitate\\Teza\\NN_Self_Driving\\model.h5')  # Load the Model


######################################


def preProcess(img):  # Pre-Processing Function
    img = img[54:120, :, :]  # Crop the image
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)  # Convert the image to YUV
    img = cv2.GaussianBlur(img, (3, 3), 0)  # Gaussian Blur the image
    img = cv2.resize(img, (200, 66))  # Resize the image
    img = img / 255  # Normalize the image
    return img  # Return the image


while True:
    img = wM.getImg(True, size=[240, 120])  # Get the image from the webcam
    img = np.asarray(img)  # Convert the image to an array
    img = preProcess(img)  # Pre-Process the image
    img = np.array([img])  # Convert the image to an array
    steering = float(model.predict(img))  # Predict the steering angle
    print(steering)  # Print the steering angle
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Break the loop if the user presses 'q'
        break  # Break the loop
cv2.destroyAllWindows()  # Destroy all the windows
print("End")  # Print End
######################################
