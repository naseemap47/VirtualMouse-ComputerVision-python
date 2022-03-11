import cv2
import time

width_cam, height_cam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, height_cam)
cap.set(4, width_cam)


while True:
    success, img = cap.read()

    cv2.imshow("Image", img)
    cv2.waitKey(1)