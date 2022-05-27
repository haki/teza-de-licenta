import cv2  # OpenCV

SS_cascade = cv2.CascadeClassifier(
    'xml/stopsign_classifier.xml')  # Load the cascade classifier for stop signs detection
SpS_cascade = cv2.CascadeClassifier('xml/lbpCascade.xml')  # Load the cascade classifier for stop signs detection
Car_cascade = cv2.CascadeClassifier('xml/cars.xml')  # Load the cascade classifier for stop signs detection

cap = cv2.VideoCapture(0)  # Capture the video from the webcam

# reduce the resolution to increase the FPS and increase the speed of the program
cap.set(3, 320)  # Width
cap.set(4, 240)  # Height

while True:
    ret, img = cap.read()  # Capture the frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale

    SSs = SS_cascade.detectMultiScale(gray, 1.3, 5)  # Detect the stop signs
    for (x, y, w, h) in SSs:  # Draw a rectangle around the stop signs
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0),
                      2)  # (image, start point, end point, color, thickness)
        cv2.putText(img, "Indicatorul 'STOP'", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                    2)  # (image, text, position, font, size, color, thickness)

        print("Dimensions of Stop Sign: {}".format((x, y, w, h)))  # Print the dimensions of the stop sign

    SpSs = SpS_cascade.detectMultiScale(gray, 1.3, 5)  # Detect the stop signs
    for (a, b, c, d) in SpSs:
        cv2.rectangle(img, (a, b), (a + c, b + d), (0, 255, 0),
                      2)  # (image, start point, end point, color, thickness)
        cv2.putText(img, "Indicatorul 'Limita de viteza'", (a, b - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                    2)  # (image, text, position, font, size, color, thickness)
        print("Dimensions of Speed Sign: {}".format((a, b, c, d)))  # Print the dimensions of the speed sign

    Cars = Car_cascade.detectMultiScale(gray, 1.3, 5)  # Detect the stop signs
    for (x, y, w, h) in Cars:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255),
                      2)  # (image, start point, end point, color, thickness)
        print("Dimensions of Car: {}".format((x, y, w, h)))  # Print the dimensions of the car

    cv2.imshow('img', img)  # Show the frame

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break  # Exit the program

cap.release()  # Release the webcam
cv2.destroyAllWindows()  # Close all the windows
