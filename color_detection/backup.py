import cv2
import numpy as np
import pandas as pd
import mediapipe as mp
import imutils
from gtts import gTTS
import pygame
import os
import time
import uuid

# Load color dataset
df = pd.read_csv("Updated_Fixed_RGB_Colors.csv")

# Setup MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise ValueError("Could not open webcam")

# Function to get color name from RGB
def get_color_name(R, G, B):
    min_dist = float('inf')
    color_name = "Unknown"
    for i in range(len(df)):
        d = np.sqrt((R - int(df.loc[i, "Red"]))**2 +
                    (G - int(df.loc[i, "Green"]))**2 +
                    (B - int(df.loc[i, "Blue"]))**2)
        if d < min_dist:
            min_dist = d
            color_name = df.loc[i, "Main Color"]
    return color_name

# Function to play audio
def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    # Wait until audio finishes
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()
    os.remove(file_path)  # Clean up the file after playing

# Track last spoken color
last_spoken = ""
last_spoken_time = 0

print("Point your index finger to an object. It will speak the color live. Press ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    frame = imutils.resize(frame, width=900)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, _ = frame.shape
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            x1, y1 = max(0, x - 15), max(0, y - 15)
            x2, y2 = min(w, x + 15), min(h, y + 15)
            roi = frame[y1:y2, x1:x2]

            if roi.size != 0:
                roi = cv2.GaussianBlur(roi, (5, 5), 0)
                b, g, r = np.mean(roi, axis=(0, 1)).astype(int)
                color_name = get_color_name(r, g, b)

                # Speak only if color changed and at least 2 seconds passed
                if color_name != last_spoken and time.time() - last_spoken_time > 2:
                    print(f"Speaking: {color_name}")
                    filename = f"color_{uuid.uuid4()}.mp3"
                    tts = gTTS(text=color_name, lang='en')
                    tts.save(filename)
                    play_audio(filename)
                    last_spoken = color_name
                    last_spoken_time = time.time()

                # Display overlay
                brightness = r + g + b
                text_color = (255, 255, 255) if brightness < 400 else (0, 0, 0)
                cv2.rectangle(frame, (20, 20), (850, 60), (int(b), int(g), int(r)), -1)
                text = f"{color_name}  R={r} G={g} B={b}"
                cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, text_color, 2, cv2.LINE_AA)

                cv2.circle(frame, (x, y), 10, (255, 255, 255), -1)

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.putText(frame, "Hold object under index finger. Press ESC to quit.",
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2)

    cv2.imshow("Live Fingertip Color Detection + TTS", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
