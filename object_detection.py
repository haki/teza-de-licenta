import cv2

SS_cascade = cv2.CascadeClassifier('xml/stopsign_classifier.xml')
SpS_cascade = cv2.CascadeClassifier('xml/lbpCascade.xml')
Car_cascade = cv2.CascadeClassifier('xml/cars.xml')

cap = cv2.VideoCapture(0)

# reduce the resolution to increase the FPS
cap.set(3, 320)
cap.set(4, 240)

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    SSs = SS_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in SSs:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(img, "Indicatorul 'STOP'", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        print("Dimensions of Stop Sign: {}".format((x, y, w, h)))

    SpSs = SpS_cascade.detectMultiScale(gray, 1.3, 5)
    for (a, b, c, d) in SpSs:
        cv2.rectangle(img, (a, b), (a + c, b + d), (0, 255, 0), 2)
        cv2.putText(img, "Indicatorul 'Limita de viteza'", (a, b - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        print("Dimensions of Speed Sign: {}".format((a, b, c, d)))

    Cars = Car_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in Cars:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        print("Dimensions of Car: {}".format((x, y, w, h)))

    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
