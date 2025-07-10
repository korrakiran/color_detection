# Fingertip Color Detection with Real-Time Text-to-Speech

This project uses a webcam to detect the color at your **index fingertip** and speaks out the color name using **Google Text-to-Speech (gTTS)**. It's powered by computer vision, MediaPipe hand tracking, and a custom RGB-to-color-name mapping from a CSV dataset.

---

## Features
- Real-time hand tracking using MediaPipe.
- Live color detection at the fingertip.
- Speaks the detected color using gTTS and pygame.
- Prevents spam by only speaking when the color changes.

---

## Requirements

Install these Python packages:

```bash
pip install opencv-python mediapipe pandas imutils gTTS pygame numpy
```

---

## Files Required

- `Updated_Fixed_RGB_Colors.csv`  
  A CSV file containing columns: `Red`, `Green`, `Blue`, and `Main Color`.  
  Place this in the same directory as the script.

---

## How It Works

1. Your webcam starts.
2. MediaPipe detects your hand and tracks the **index fingertip** (landmark 8).
3. The script takes the RGB average of a small region near your fingertip.
4. It matches the color with the closest color in the dataset.
5. If the color is different from the previous one, it uses gTTS to speak the name.

---

## Run the Script

```bash
python detect.py
```
## Or can use this

```bash
python backup.py
```

Make sure your webcam is enabled. Point your index finger to an object. The script will say the color name out loud.

---

## Notes

- It won’t spam the same color; it only speaks when the color **changes**.
- Audio is played with `pygame.mixer` and removed afterward to avoid file lock issues.
- Works best in good lighting.

---

## License

MIT License

---

## ✨ Created on July 04, 2025
