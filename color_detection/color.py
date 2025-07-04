import csv
import math

# Main color references
main_colors_ref = {
    "Red": (255, 0, 0),
    "Blue": (0, 0, 255),
    "Green": (0, 255, 0),
    "Yellow": (255, 255, 0),
    "Pink": (255, 192, 203),
    "Purple": (128, 0, 128),
    "Orange": (255, 165, 0),
    "Brown": (139, 69, 19),
    "Black": (0, 0, 0),
    "White": (255, 255, 255)
}

def euclidean_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

# Generate RGB values in steps of 10
rows = []
for r in range(0, 256, 10):
    for g in range(0, 256, 10):
        for b in range(0, 256, 10):
            rgb = (r, g, b)
            closest_color = min(main_colors_ref.items(), key=lambda x: euclidean_distance(rgb, x[1]))[0]
            rows.append([closest_color, r, g, b])  # Note the order: Main Color, R, G, B

# Write to CSV
with open("RGB_Main_Colors_Dataset.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(rows)  # We'll skip the header as per the original code

print("RGB_Main_Colors_Dataset.csv created successfully!")