import cv2
import numpy as np

#def function(value):
   # print(value)

#image = cv2.imread('Photos/WIN_20240201_22_56_29_Pro.jpg')

#cv2.namedWindow('image')
#cv2.resizeWindow('image', 600, 300)

#cv2.createTrackbar('HMin', 'image', 0, 179, function)
#cv2.createTrackbar('SMin', 'image', 0, 255, function)
#cv2.createTrackbar('VMin', 'image', 0, 255, function)
#cv2.createTrackbar('HMax', 'image', 0, 179, function)
#cv2.createTrackbar('SMax', 'image', 0, 255, function)
#cv2.createTrackbar('VMax', 'image', 0, 255, function)

def empty(img):
    pass


video = cv2.VideoCapture(0)
cv2.namedWindow('TrackBar')
cv2.resizeWindow('TrackBar', 600, 300)
cv2.createTrackbar('hue_min', 'TrackBar', 0, 179, empty)
cv2.createTrackbar('hue_max', 'TrackBar', 179, 179, empty)
cv2.createTrackbar('sat_min', 'TrackBar', 0, 255, empty)
cv2.createTrackbar('sat_max', 'TrackBar', 255, 255, empty)
cv2.createTrackbar('val_min', 'TrackBar', 0, 255, empty)
cv2.createTrackbar('val_max', 'TrackBar', 255, 255, empty)

#cv2.setTrackbarPos('HMax', 'image', 179)
#cv2.setTrackbarPos('SMax', 'image', 255)
#cv2.setTrackbarPos('VMax', 'image', 255)

hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

#while True:
    #hMin = cv2.getTrackbarPos('HMin', 'image')
    #sMin = cv2.getTrackbarPos('SMin', 'image')
    #vMin = cv2.getTrackbarPos('VMin', 'image')
    #hMax = cv2.getTrackbarPos('HMax', 'image')
    #sMax = cv2.getTrackbarPos('SMax', 'image')
    #vMax = cv2.getTrackbarPos('VMax', 'image')

    #lower = np.array([hMin, sMin, vMin])
    #upper = np.array([hMax, sMax, vMax])

    #hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #mask = cv2.inRange(hsv, lower, upper)

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
    result = cv2.bitwise_and(TrackBar, TrackBar, mask=mask)

    if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
        print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    cv2.imshow('image', result)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
