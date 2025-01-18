# Ophthalmology AI Research Setup Guide

This guide provides step-by-step instructions for setting up the AI tools required for processing ophthalmology-related AVI files and creating processed outputs. Follow the steps below to install Python, set up the required environment, and run the provided script.

---

## Prerequisites

1. A Windows machine.
2. Basic knowledge of using the command line.
3. AVI files to be processed.

---

## Step 1: Install Python 3.11

1. Download Python 3.11 from the official website:  
   [Python 3.11 Downloads](https://www.python.org/downloads/release/python-3110/).
2. Run the installer and **check the box** to "Add Python to PATH" before proceeding.
3. Select "Customize installation," ensure all options are checked, and proceed to install.

---

## Step 2: Install a Virtual Environment (Optional but Recommended)

1. Open the command prompt.
2. Create a virtual environment:
   - `python -m venv ophthalmology-env`
3. Activate the virtual environment:
   - `.\ophthalmology-env\Scripts\activate`

---

## Step 3: Install Required Libraries

1. Download the `requirements.txt` file or copy its content.
2. In the terminal, navigate to the folder containing the `requirements.txt` file and run:
   - `pip install -r requirements.txt`

---

## Step 4: Prepare Your Project Files

1. Place your `.avi` file(s) in the same directory as `main.py` or note their path for later use.
2. Ensure the following files are in the project folder:
   - `main.py` (the provided script)
   - `requirements.txt` (dependencies)

---

## Step 5: Running the Script

1. Open the terminal and navigate to the folder containing `main.py`.
2. Run the script with the path to your `.avi` file:
   - `python main.py <path_to_your_avi_file>`
   
   Example:
   - `python main.py example_video.avi`

---

## Script Features

- **Frame Extraction**: Extracts frames from the input `.avi` file and saves them as `.jpg` images.
- **Tile Processing**: Splits each frame into tiles, processes them using a YOLO model, and overlays bounding boxes.
- **TIF Stack Creation**: Combines processed frames into a TIF stack for further analysis.

---

## Outputs

1. **Frames Directory**: Extracted frames from the `.avi` file.
2. **Processed Frames Directory**: Frames with bounding boxes overlayed.
3. **TIF File**: A single `.tif` file combining all processed frames.

---

## Troubleshooting

- If Python is not recognized as a command, ensure it is added to your PATH during installation.
- If libraries fail to install, ensure your Python version is 3.11 and your virtual environment is activated.

---

Feel free to reach out for additional support or clarification while setting up or using the script!
