import cv2
import numpy as np

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


def empty(img):
    pass


video = cv2.VideoCapture(0)

kernel = np.ones((3, 3), 'uint8')
font = cv2.FONT_HERSHEY_SIMPLEX
org = (0, 20)
fontScale = 0.6
color = (0, 0, 255)
thickness = 2

cv2.namedWindow('TrackBar')
cv2.resizeWindow('TrackBar', 600, 300)
cv2.createTrackbar('hue_min', 'TrackBar', 0, 179, empty)
cv2.createTrackbar('hue_max', 'TrackBar', 179, 179, empty)
cv2.createTrackbar('sat_min', 'TrackBar', 0, 255, empty)
cv2.createTrackbar('sat_max', 'TrackBar', 255, 255, empty)
cv2.createTrackbar('val_min', 'TrackBar', 0, 255, empty)
cv2.createTrackbar('val_max', 'TrackBar', 255, 255, empty)

while True:
    ret, img = video.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue_min = cv2.getTrackbarPos('hue_min', 'TrackBar')
    hue_max = cv2.getTrackbarPos('hue_max', 'TrackBar')
    sat_min = cv2.getTrackbarPos('sat_min', 'TrackBar')
    sat_max = cv2.getTrackbarPos('sat_max', 'TrackBar')
    val_min = cv2.getTrackbarPos('val_min', 'TrackBar')
    val_max = cv2.getTrackbarPos('val_max', 'TrackBar')

    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])
    mask = cv2.inRange(hsv, lower, upper)

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
    cv2.imshow('Frame', img)
    cv2.imshow('hsv', hsv)
    cv2.imshow('mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()