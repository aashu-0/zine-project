import numpy as np
import cv2

dist = 0
focal = 450
pixels = 30
width = 6

def get_dist(rectangle_params, image):
    pixels = rectangle_params[1][0]
    print(pixels)

    dist = (width * focal) / pixels

    image = cv2.putText(image, 'Distance from Camera in cm :', org, font,
                        1, color, 2, cv2.LINE_AA)

    image = cv2.putText(image, str(dist), (110, 50), font,
                        fontScale, color, 1, cv2.LINE_AA)

    return image



cap = cv2.VideoCapture(0)

kernel = np.ones((3, 3), 'uint8')
font = cv2.FONT_HERSHEY_SIMPLEX
org = (0, 20)
fontScale = 0.6
color = (0, 0, 255)
thickness = 2

cv2.namedWindow('Object Distance Measure ', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Object Distance Measure ', 700, 600)

while True:
    ret, img = cap.read()

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # mask for detection
    # change the ranges as per object using color.py program
    lower = np.array([21, 0, 194])
    upper = np.array([179, 255, 255])
    mask = cv2.inRange(hsv_img, lower, upper)

    # garbage removal
    d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=5)

    cont, hei = cv2.findContours(d_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cont = sorted(cont, key=cv2.contourArea, reverse=True)[:1]

    for cnt in cont:
        if (cv2.contourArea(cnt) > 100 and cv2.contourArea(cnt) < 306000):
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img, [box], -1, (255, 0, 0), 3)

            img = get_dist(rect, img)

    cv2.imshow('Object Dist Measure ', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()