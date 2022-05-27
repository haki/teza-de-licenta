import cv2
import numpy as np
from tensorflow.keras.models import load_model
import modules.WebcamModule as wM

#######################################
model = load_model('D:\\Desktop\\Universitate\\Teza\\NN_Self_Driving\\model.h5')
######################################


def preProcess(img):
    img = img[54:120, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img


while True:

    img = wM.getImg(True, size=[240, 120])
    img = np.asarray(img)
    img = preProcess(img)
    img = np.array([img])
    steering = float(model.predict(img))
    print(steering)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
print("End")
######################################
