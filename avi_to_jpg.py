import cv2
import numpy as np
import os


avi_file = input('Enter path to .avi file: ')
base_name = os.path.splitext(os.path.basename(avi_file))[0]

output_dir = base_name
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(avi_file)
if not cap.isOpened():
    raise Exception("Could not open the .avi file.")

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    jpg_filename = os.path.join(output_dir, f'{base_name}_{frame_count:02d}.jpg')
    cv2.imwrite(jpg_filename, frame)
    frame_count += 1

cap.release()
print(f"Extraction complete. {frame_count} frames have been saved in the '{output_dir}' directory.")