import cv2  # OpenCV

cap = cv2.VideoCapture(0)  # 0 = Webcam


def getImg(display=False, size=[480, 240]):  # size = [width, height]
    _, img = cap.read()  # _ = return value, img = image
    img = cv2.resize(img, (size[0], size[1]))  # Resize image
    if display:  # If display is true
        cv2.imshow('IMG', img)  # Display image
    return img  # Return image


if __name__ == '__main__':  # If this is the main file
    while True:
        img = getImg(True)  # Get image and display it on screen
