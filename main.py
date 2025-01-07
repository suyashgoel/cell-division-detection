import shutil
from PIL import Image
import cv2
import os
from ultralytics import YOLO
import numpy as np
import re
import sys

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

model = YOLO("yolov8.pt") 

def split_image_into_tiles(image, grid_size=(3, 3)):
    width, height = image.size
    tile_width = width // grid_size[0]
    tile_height = height // grid_size[1]
    
    tiles = []
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            box = (i * tile_width, j * tile_height, (i + 1) * tile_width, (j + 1) * tile_height)
            tile = image.crop(box)
            tiles.append((tile, box))
    return tiles

def draw_boxes_on_full_image(full_image, results, tile_box):
    image_with_boxes = np.array(full_image)
    tile_x1, tile_y1, tile_x2, tile_y2 = tile_box
    
    for result in results:
        for box, conf in zip(result.boxes.xyxy, result.boxes.conf):
            x1, y1, x2, y2 = map(int, box)
            x1 += tile_x1
            y1 += tile_y1
            x2 += tile_x1
            y2 += tile_y1
            
            if conf >= 0.4:
                color = (0, 255, 0)
            elif conf >= 0.25:
                color = (255, 165, 0)
            else:
                color = (255, 0, 0)

            image_with_boxes = cv2.rectangle(image_with_boxes, (x1, y1), (x2, y2), color, 2)

    return image_with_boxes

def process_image_with_tiles(image_path, output_path):
    full_image = Image.open(image_path)
    tiles = split_image_into_tiles(full_image)
    
    image_with_boxes = np.array(full_image)
    for tile, tile_box in tiles:
        results = model(tile, conf=0.10)
        if len(results[0].boxes) > 0:
            image_with_boxes = draw_boxes_on_full_image(image_with_boxes, results, tile_box)
    
    image_with_boxes_pil = Image.fromarray(image_with_boxes)
    image_with_boxes_pil.save(output_path)


def numeric_sort(filename):
    numbers = re.findall(r'(\d+)', filename)
    return int(numbers[-1]) if numbers else float('inf')


def clear_or_create_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory) 
    os.makedirs(directory)


def create_tif_stack(input_dir, output_tif_path):
    image_files = sorted(
        [f for f in os.listdir(input_dir) if f.endswith('.jpg')],
        key=numeric_sort
    )
    img, *imgs = [Image.open(os.path.join(input_dir, f)) for f in image_files]
    img.save(output_tif_path, save_all=True, append_images=imgs)
    print(f"TIF stack saved to {output_tif_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_avi_file>")
        sys.exit(1)
    avi_file = sys.argv[1]
    avi_name = os.path.splitext(os.path.basename(avi_file))[0]
    tiff_output_path = f"{avi_name}_processed.tif"

    frame_output_dir = "frames"
    processed_output_dir = "processed_frames"

    print("Setting up directories...")
    clear_or_create_directory(frame_output_dir)
    clear_or_create_directory(processed_output_dir)

    print("Extracting frames...")
    extract_frames_from_avi(avi_file, frame_output_dir)

    print("Processing frames...")
    frame_files = sorted(
        [f for f in os.listdir(frame_output_dir) if f.endswith('.jpg')],
        key=numeric_sort
    )

    for frame_file in frame_files:
        frame_path = os.path.join(frame_output_dir, frame_file)
        output_path = os.path.join(processed_output_dir, frame_file)
        process_image_with_tiles(frame_path, output_path)

    print("Creating TIF stack...")
    create_tif_stack(processed_output_dir, tiff_output_path)

    print("All processing complete.")

if __name__ == "__main__":
    main()