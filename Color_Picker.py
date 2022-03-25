import cv2
import numpy as np
import requests
url = 'http://192.168.178.150:8080/shot.jpg'

def empty(x):
    pass


cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 17, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 166, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 79, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 167, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

cap = cv2.VideoCapture(0)
cap.set(3, 400)
cap.set(4, 300)
cap.set(10, 100)
while True:
    r = requests.get(url)
    img_array = np.array(bytearray(r.content), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    print(h_min, h_max, s_min, s_max, v_min, v_max)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    imgMask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=imgMask)

    imgMask = cv2.cvtColor(imgMask, cv2.COLOR_GRAY2BGR)
    imgStack = np.hstack((img, imgMask))
    cv2.imshow('Horizontal Stacking', imgStack)
    cv2.imshow('result', imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()