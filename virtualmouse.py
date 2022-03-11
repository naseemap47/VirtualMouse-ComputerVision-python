import cv2
import time
import mediapipe as mp
import autopy
import numpy as np

width_cam, height_cam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, height_cam)
cap.set(4, width_cam)

mp_hand = mp.solutions.hands
hand = mp_hand.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
p_time = 0

width_screen, height_screen = autopy.screen.size()

while True:
    # Draw Hand Landmarks
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hand.process(img_rgb)
    if result.multi_hand_landmarks:
        lm_list = []
        x_list = []
        y_list = []
        for hand_lm in result.multi_hand_landmarks:
            for id, lm in enumerate(hand_lm.landmark):
                height, width, channel = img.shape
                x, y = int(lm.x * width), int(lm.y * height)
                x_list.append(x)
                y_list.append(y)
                lm_list.append([id, x, y])
                mp_draw.draw_landmarks(img, hand_lm, mp_hand.HAND_CONNECTIONS)

                x_min, x_max = min(x_list), max(x_list)
                y_min, y_max = min(y_list), max(y_list)
            cv2.rectangle(
                img, (x_min - 20, y_min - 20),
                (x_max + 20, y_max + 20),
                (0, 255, 0), 2
            )
        # print(lm_list)
        if len(lm_list) > 15:
            x1, y1 = lm_list[8][1:]
            x2, y2 = lm_list[12][1:]

            # Moving Mode - Index finger Up
            if y1 < lm_list[6][2] and y2 > lm_list[10][2]:
                print("Index Finger Up")
                # Convert Coordinates into mouse Coordinates
                x3 = np.interp(x1, (0, width_cam), (0, width_screen))
                y3 = np.interp(y1, (0, height_cam), (0, height_screen))

                # Move Mouse
                autopy.mouse.move(width_screen - x3, y3)
                cv2.circle(
                    img, (x1, y1), 10,
                    (255, 0, 255), cv2.FILLED
                )
            # Selection Mode - Index and Middle fingers are Up
            elif y1 < lm_list[6][2] and y2 < lm_list[10][2]:
                print("Index and Middle fingers are Up")

    # Frame Per Sec
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