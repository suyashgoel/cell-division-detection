# **README: AVI to TIF Frame Processing Pipeline**

This pipeline processes `.avi` video files by extracting frames, applying YOLOv8 object detection, and combining the processed frames into a multi-page `.tif` file. It is designed to seamlessly integrate with workflows involving ImageJ and `.tif` files.

---

## **Workflow Overview**

1. **Download the Input `.tif` File**:
   - Obtain the intended `.tif` file from Box.
   
2. **Convert `.tif` to `.avi` Using ImageJ**:
   - Open the `.tif` file in **ImageJ**.
   - Export it as an `.avi` file:
     - Save the exported `.avi` file.

3. **Run the Pipeline on the Exported `.avi` File**:
   - Use this pipeline to process the `.avi` file:
     - Extract frames.
     - Run object detection using YOLOv8.
     - Combine the processed frames into a multi-page `.tif` file.

4. **Retrieve the Processed `.tif` File**:
   - Use the output `.tif` file for further analysis or visualization.

---

## **Requirements**

- **Python version**: 3.8 or later.
- **Environment**: Compatible with Windows, macOS, or Linux.
- **Dependencies**: Listed in `requirements.txt` and can be installed easily.

---

## **Setup Instructions**

1. **Install Python**:
   - Download and install Python 3.8 or later from [python.org](https://www.python.org/downloads/).

2. **Download the Repository**:
   - Obtain the project folder containing all files.

3. **Set Up a Virtual Environment (Recommended)**:
   ```bash
   python -m venv venv
   # Activate the virtual environment:
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate

4. **Install Requirements:**:
   Run the following command to install all necessary dependencies:
   ```bash
   pip install -r requirements.txt

5. **Run the Pipeline:**:
   Use the following command to process your `.avi` file:
   ```bash
   python main.py

6. **Enter file path:**:
   When prompted, enter the file path

