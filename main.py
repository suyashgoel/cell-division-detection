import matplotlib.pyplot as plt
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
import os
import re

# Load the YOLOv8 model with your custom weights
model = YOLO("best-v10.pt")  # Path to your YOLOv8 weights

# Function to split the image into 3x3 tiles and keep track of original coordinates
def split_image_into_tiles(image, grid_size=(3, 3)):
    width, height = image.size
    tile_width = width // grid_size[0]
    tile_height = height // grid_size[1]
    
    tiles = []
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            box = (i * tile_width, j * tile_height, (i + 1) * tile_width, (j + 1) * tile_height)
            tile = image.crop(box)
            tiles.append((tile, box))  # Save the tile and its box (coordinates)
    return tiles

# Function to draw bounding boxes on the full image
def draw_boxes_on_full_image(full_image, results, tile_box):
    image_with_boxes = np.array(full_image)  # Convert to NumPy array for OpenCV operations
    tile_x1, tile_y1, tile_x2, tile_y2 = tile_box  # Tile's position in the full image
    
    for result in results:
        for box in result.boxes.xyxy:  # xyxy format for bounding box
            x1, y1, x2, y2 = map(int, box)  # Get the coordinates of the bounding box
            # Adjust coordinates relative to the original image
            x1 += tile_x1
            y1 += tile_y1
            x2 += tile_x1
            y2 += tile_y1
            # Draw the box on the full image
            image_with_boxes = cv2.rectangle(image_with_boxes, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box
    
    return image_with_boxes

# Function to stitch the tiles back into a single image and draw predictions
def stitch_tiles_back(full_image, tiles):
    image_with_boxes = np.array(full_image)  # Start with the full image as a background
    
    # Process each tile with the model and draw the predictions on the full image
    for tile, tile_box in tiles:
        # Run YOLOv8 inference on the tile with a lower confidence threshold
        results = model(tile, conf=0.2)  # YOLO inference with a lower confidence threshold
        
        # Draw bounding boxes on the full image relative to their tile position
        if len(results[0].boxes) > 0:
            image_with_boxes = draw_boxes_on_full_image(image_with_boxes, results, tile_box)
    
    return image_with_boxes

# Main function to process the image and re-stitch tiles with predictions
def process_image_with_tiles(image_path, output_path):
    # Load the original image
    full_image = Image.open(image_path)
    
    # Split the image into 3x3 tiles and track their original positions
    tiles = split_image_into_tiles(full_image)
    
    # Stitch the tiles back into the full image with bounding boxes
    image_with_boxes = stitch_tiles_back(full_image, tiles)

    # Convert back to PIL Image to save
    image_with_boxes_pil = Image.fromarray(image_with_boxes)
    
    # Save the final image with bounding boxes
    image_with_boxes_pil.save(output_path)

# Function to sort filenames numerically
def numeric_sort(value):
    numbers = re.findall(r'\d+', value)
    return int(numbers[0]) if numbers else float('inf')  # Use 'inf' for files without numbers

# Folder path where the images are stored
folder_path = "/Users/suyashgoel/Bioelectricity-Annotation/LESC EF 100 mV_pos 3"
output_folder = "out"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process the images in numeric order
image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".jpg") or f.endswith(".png")], key=numeric_sort)

for filename in image_files:
    image_path = os.path.join(folder_path, filename)
    output_path = os.path.join(output_folder, f"processed_{filename}")
    
    # Process each image and save the result
    process_image_with_tiles(image_path, output_path)

print(f"Processed {len(image_files)} images and saved to {output_folder}")
