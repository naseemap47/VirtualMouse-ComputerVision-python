import cv2
import time
import mediapipe as mp

width_cam, height_cam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, height_cam)
cap.set(4, width_cam)

mp_hand = mp.solutions.hands
hand = mp_hand.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

p_time = 0

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
        print(lm_list)

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