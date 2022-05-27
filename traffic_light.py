import cv2  # OpenCV
import numpy as np  # Numpy


def detect(img):  # Detect traffic light
    font = cv2.FONT_HERSHEY_SIMPLEX  # Font for text on image
    cimg = img  # Copy of image for drawing purposes (not necessary)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convert to HSV color space

    # color range
    lower_red1 = np.array([0, 100, 100])  # Red lower range
    upper_red1 = np.array([10, 255, 255])  # Red upper range
    lower_red2 = np.array([160, 100, 100])  # Red lower range
    upper_red2 = np.array([180, 255, 255])  # Red upper range
    lower_green = np.array([40, 50, 50])  # Green lower range
    upper_green = np.array([90, 255, 255])  # Green upper range
    lower_yellow = np.array([15, 150, 150])  # Yellow lower range
    upper_yellow = np.array([35, 255, 255])  # Yellow upper range
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)  # Create mask for red
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)  # Create mask for red
    maskg = cv2.inRange(hsv, lower_green, upper_green)  # Create mask for green
    masky = cv2.inRange(hsv, lower_yellow, upper_yellow)  # Create mask for yellow
    maskr = cv2.add(mask1, mask2)  # Add both masks

    size = img.shape  # Get image size

    # hough circle detect
    r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80,
                                 param1=50, param2=10, minRadius=0, maxRadius=30)  # Detect circles

    g_circles = cv2.HoughCircles(maskg, cv2.HOUGH_GRADIENT, 1, 60,
                                 param1=50, param2=10, minRadius=0, maxRadius=30)  # Detect circles

    y_circles = cv2.HoughCircles(masky, cv2.HOUGH_GRADIENT, 1, 30,
                                 param1=50, param2=5, minRadius=0, maxRadius=30)  # Detect circles

    # traffic light detect
    r = 5  # Radius of circle
    bound = 4.0 / 10  # Bound for traffic light detection
    if r_circles is not None:  # If circles are detected
        r_circles = np.uint16(np.around(r_circles))  # Round detected circles

        for i in r_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:  # If circle is out of image or out of bound
                continue  # Skip this circle

            h, s = 0.0, 0.0  # Initialize hue and saturation
            for m in range(-r, r):
                for n in range(-r, r):

                    if (i[1] + m) >= size[0] or (i[0] + n) >= size[1]:  # If pixel is out of image
                        continue  # Skip this pixel
                    h += maskr[i[1] + m, i[0] + n]  # Add pixel value to hue
                    s += 1  # Add 1 to saturation
            if h / s > 50:  # If hue is greater than 50
                cv2.circle(cimg, (i[0], i[1]), i[2] + 10, (0, 255, 0), 2)  # Draw circle
                cv2.circle(maskr, (i[0], i[1]), i[2] + 30, (255, 255, 255), 2)  # Draw circle
                cv2.putText(cimg, 'Rosu', (i[0], i[1]), font, 1, (255, 0, 0), 2, cv2.LINE_AA)  # Put text on image

    if g_circles is not None:  # If circles are detected
        g_circles = np.uint16(np.around(g_circles))  # Round detected circles

        for i in g_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:  # If circle is out of image or out of bound
                continue  # Skip this circle

            h, s = 0.0, 0.0  # Initialize hue and saturation
            for m in range(-r, r):
                for n in range(-r, r):

                    if (i[1] + m) >= size[0] or (i[0] + n) >= size[1]:  # If pixel is out of image
                        continue  # Skip this pixel
                    h += maskg[i[1] + m, i[0] + n]  # Add pixel value to hue
                    s += 1  # Add 1 to saturation
            if h / s > 100:  # If hue is greater than 100
                cv2.circle(cimg, (i[0], i[1]), i[2] + 10, (0, 255, 0), 2)  # Draw circle
                cv2.circle(maskg, (i[0], i[1]), i[2] + 30, (255, 255, 255), 2)  # Draw circle
                cv2.putText(cimg, 'Verde', (i[0], i[1]), font, 1, (255, 0, 0), 2, cv2.LINE_AA)  # Put text on image

    if y_circles is not None:  # If circles are detected
        y_circles = np.uint16(np.around(y_circles))  # Round detected circles

        for i in y_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:  # If circle is out of image or out of bound
                continue  # Skip this circle

            h, s = 0.0, 0.0  # Initialize hue and saturation
            for m in range(-r, r):
                for n in range(-r, r):

                    if (i[1] + m) >= size[0] or (i[0] + n) >= size[1]:  # If pixel is out of image
                        continue  # Skip this pixel
                    h += masky[i[1] + m, i[0] + n]  # Add pixel value to hue
                    s += 1  # Add 1 to saturation
            if h / s > 50:  # If hue is greater than 50
                cv2.circle(cimg, (i[0], i[1]), i[2] + 10, (0, 255, 0), 2)  # Draw circle
                cv2.circle(masky, (i[0], i[1]), i[2] + 30, (255, 255, 255), 2)  # Draw circle
                cv2.putText(cimg, 'Albastru', (i[0], i[1]), font, 1, (255, 0, 0), 2, cv2.LINE_AA)  # Put text on image

    cv2.imshow('detected results', cimg)  # Show image


if __name__ == '__main__':  # If this file is executed as main file
    cap = cv2.VideoCapture(0)  # Open webcam
    while (True):
        ret, frame = cap.read()  # Read frame
        detect(frame)  # Detect circles
        if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed
            break  # Exit
    cap.release()  # Release webcam
    cv2.destroyAllWindows()  # Close all windows
