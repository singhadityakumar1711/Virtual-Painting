import cv2
import numpy as np
import requests

# url = 'http://192.168.178.150:8080/shot.jpg'
cap = cv2.VideoCapture(0)

myColors = [17, 166, 79, 255, 167, 255]

myColorValues = [47, 255, 178]

myPoints = []


def findColor(img, myColors, color):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([myColors[0], myColors[2], myColors[4]])
    upper = np.array([myColors[1], myColors[3], myColors[5]])
    imgMask = cv2.inRange(imgHSV, lower, upper)
    x, y = getContours(imgMask)
    cv2.circle(imgResult, (x, y), 10, (color[0], color[1], color[2]), cv2.FILLED)
    cv2.imshow("image", imgMask)
    return x, y


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        corner_points = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
        # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
        x, y, w, h = cv2.boundingRect(corner_points)
    return x + w // 2, y


def drawOnCanvas(myPoints, color):
    cv2.circle(imgResult, (myPoints[0], myPoints[1]), 10, (color[0], color[1], color[2]), cv2.FILLED)


while True:
    # r = requests.get(url)
    # img_array = np.array(bytearray(r.content), dtype=np.uint8)
    # img = cv2.imdecode(img_array, -1)
    success, img = cap.read()
    imgResult = img.copy()
    abs, order = findColor(img, myColors, myColorValues)
    myPoints.append(abs)
    myPoints.append(order)
    cv2.imshow("Video", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
