import cv2
import os

def extract_frames_from_avi(avi_path, output_dir):

    base_name = os.path.splitext(os.path.basename(avi_path))[0]
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(avi_path)
    if not cap.isOpened():
        raise Exception("Could not open the .avi file.")

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save frames with zero-padded numbers
        jpg_filename = os.path.join(output_dir, f'{base_name}_{frame_count:04d}.jpg')
        cv2.imwrite(jpg_filename, frame)
        frame_count += 1

    cap.release()
    print(f"Extraction complete. {frame_count} frames have been saved in the '{output_dir}' directory.")
    return output_dir
