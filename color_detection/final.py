import numpy as np
import pandas as pd
import cv2
import imutils

# Initialize camera with error handling
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    raise ValueError("Could not open camera! Please check if webcam is connected.")

# Initialize variables
r = g = b = xpos = ypos = 0
clicked = False  # Initialize clicked variable

# Read and verify CSV file
try:
    index = ['Main Color', 'Red', 'Green', 'Blue']
    df = pd.read_csv('RGB_Main_Colors_Dataset.csv', names=index, header=None)
except FileNotFoundError:
    raise FileNotFoundError("RGB_Main_Colors_Dataset.csv not found in current directory")

def getColorName(Red, Green, Blue):
    minimum = 10000
    cname = "Unknown"  # Default value
    try:
        for i in range(len(df)):
            d = abs(Red - int(df.loc[i,"Red"])) + abs(Green - int(df.loc[i,"Green"])) + abs(Blue - int(df.loc[i,"Blue"]))
            if (d <= minimum):
                minimum = d
                cname = df.loc[i, 'Main Color']
    except Exception as e:
        print(f"Error in color detection: {e}")
        return "Error"
    return cname

def identify_color(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDOWN:  # Only update on mouse click
        xpos = x
        ypos = y
        try:
            b, g, r = frame[y,x]
            b = int(b)
            g = int(g)
            r = int(r)
            clicked = True
        except:
            print("Error getting color at point")

# Create window and set mouse callback
cv2.namedWindow('image')
cv2.setMouseCallback('image', identify_color)

print("Program started. Press 'ESC' to exit.")

while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to grab frame")
        break
        
    try:
        frame = imutils.resize(frame, width=900)
        
        # Draw color rectangle
        cv2.rectangle(frame, (20,20), (800, 60), (b,g,r), -1)
        
        # Prepare and draw text
        # Instead of using f-string, let's use the string concatenation method that was working before
        text = getColorName(r,g,b) + '   R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        
        # Choose text color based on background brightness
        if(r+g+b >= 600):
            text_color = (0,0,0)
        else:
            text_color = (255,255,255)
            
        cv2.putText(frame, text, (50,50), 2, 0.8, text_color, 2, cv2.LINE_AA)
        
        # Show the frame
        cv2.imshow('image', frame)
        
        # Check for ESC key
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key
            print("ESC pressed. Exiting...")
            break
            
    except Exception as e:
        print(f"Error in main loop: {e}")
        break

# Cleanup
print("Cleaning up...")
camera.release()
cv2.destroyAllWindows()