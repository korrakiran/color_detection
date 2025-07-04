import cv2
import numpy as np
import pandas as pd
import mediapipe as mp
import imutils

# Load the updated color dataset
df = pd.read_csv('Updated_RGB_Main_Colors.csv')

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    raise ValueError("Could not open camera")

def getColorName(Red, Green, Blue):
    min_dist = float('inf')
    color_name = "Unknown"
    for i in range(len(df)):
        d = np.sqrt((Red - int(df.loc[i, "Red"]))**2 +
                    (Green - int(df.loc[i, "Green"]))**2 +
                    (Blue - int(df.loc[i, "Blue"]))**2)
        if d < min_dist:
            min_dist = d
            color_name = df.loc[i, "Main Color"]
    return color_name

print("📸 Index finger color detection running... Press ESC to exit.")

while True:
    success, frame = camera.read()
    if not success:
        print("Failed to capture frame")
        break

    frame = imutils.resize(frame, width=900)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, _ = frame.shape
            # Index finger tip landmark (id=8)
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            # Region of interest: 10x10 around fingertip
            x1 = max(0, x - 5)
            y1 = max(0, y - 5)
            x2 = min(w, x + 5)
            y2 = min(h, y + 5)
            roi = frame[y1:y2, x1:x2]
            if roi.size != 0:
                b, g, r = np.mean(roi, axis=(0, 1)).astype(int)
                color_name = getColorName(r, g, b)

                # Show the box and label
                cv2.rectangle(frame, (20, 20), (800, 60), (int(b), int(g), int(r)), -1)
                label = f'{color_name}  R={r} G={g} B={b}'
                text_color = (255, 255, 255) if r+g+b < 600 else (0, 0, 0)
                cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, text_color, 2, cv2.LINE_AA)

                # Show fingertip position
                cv2.circle(frame, (x, y), 8, (255, 255, 255), -1)

            # Optional: draw full hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show the frame
    cv2.imshow("Index Finger Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release
camera.release()
cv2.destroyAllWindows()
