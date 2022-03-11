import cv2
import time

width_cam, height_cam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, height_cam)
cap.set(4, width_cam)

p_time = 0

while True:
    success, img = cap.read()

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv2.putText(
        img, f'FPS: {int(fps)}', (10, 50),
        cv2.FONT_HERSHEY_PLAIN, 2,
        (255, 0, 0), 2
    )
    cv2.imshow("Image", img)
    cv2.waitKey(1)