from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
import os
import re

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