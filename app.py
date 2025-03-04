from flask import Flask, request, send_file, render_template, Response
import shutil
from PIL import Image
import cv2
import os
from ultralytics import YOLO
import numpy as np
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['FRAMES_FOLDER'] = 'frames'

model = YOLO("yolov8.pt")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    confidence = float(request.form.get('confidence', 0.15))
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        avi_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure the directory exists
        file.save(avi_path)

        frame_output_dir = app.config['FRAMES_FOLDER']
        processed_output_dir = app.config['PROCESSED_FOLDER']
        tiff_output_path = f"{os.path.splitext(filename)[0]}_processed.tif"

        clear_or_create_directory(frame_output_dir)
        clear_or_create_directory(processed_output_dir)

        extract_frames_from_avi(avi_path, frame_output_dir)

        frame_files = sorted(
            [f for f in os.listdir(frame_output_dir) if f.endswith('.jpg')],
            key=numeric_sort
        )

        for frame_file in frame_files:
            frame_path = os.path.join(frame_output_dir, frame_file)
            output_path = os.path.join(processed_output_dir, frame_file)
            process_image_with_tiles(frame_path, output_path, confidence)

        create_tif_stack(processed_output_dir, tiff_output_path)

        # Stream the file in chunks
        return Response(generate_large_file(tiff_output_path),
                        mimetype='image/tiff',
                        headers={'Content-Disposition': f'attachment; filename={os.path.basename(tiff_output_path)}'})

    return 'No file uploaded', 400

def generate_large_file(filepath, chunk_size=8192):
    """Stream the file in chunks to avoid memory overload."""
    with open(filepath, 'rb') as file:
        while chunk := file.read(chunk_size):
            yield chunk

def extract_frames_from_avi(avi_path, output_dir):
    cap = cv2.VideoCapture(avi_path)
    if not cap.isOpened():
        raise Exception("Could not open the .avi file.")

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        jpg_filename = os.path.join(output_dir, f'frame_{frame_count:04d}.jpg')
        cv2.imwrite(jpg_filename, frame)
        frame_count += 1

    cap.release()

def clear_or_create_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def process_image_with_tiles(image_path, output_path, confidence=0.15):
    full_image = Image.open(image_path)
    tiles = split_image_into_tiles(full_image)
    image_with_boxes = np.array(full_image)
    for tile, tile_box in tiles:
        results = model(tile, conf=confidence)
        if len(results[0].boxes) > 0:
            image_with_boxes = draw_boxes_on_full_image(image_with_boxes, results, tile_box)
    image_with_boxes_pil = Image.fromarray(image_with_boxes)
    image_with_boxes_pil.save(output_path)

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
            image_with_boxes = cv2.rectangle(image_with_boxes, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return image_with_boxes

def create_tif_stack(input_dir, output_tif_path):
    image_files = sorted(
        [f for f in os.listdir(input_dir) if f.endswith('.jpg')],
        key=numeric_sort
    )
    img, *imgs = [Image.open(os.path.join(input_dir, f)) for f in image_files]
    img.save(output_tif_path, save_all=True, append_images=imgs)

def numeric_sort(filename):
    numbers = re.findall(r'(\d+)', filename)
    return int(numbers[-1]) if numbers else float('inf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
