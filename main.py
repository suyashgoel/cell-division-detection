import os
import shutil
import re
from avi_to_jpg import extract_frames_from_avi
from predict import process_image_with_tiles
from PIL import Image


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
    avi_file = input("Enter the path to the AVI file: ")
    frame_output_dir = "frames"
    processed_output_dir = "processed_frames"
    tiff_output_path = "processed_frames.tif"

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
