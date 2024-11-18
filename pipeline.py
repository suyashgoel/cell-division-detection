from ij import IJ

# Specify the path to your .tif file (uploaded by your team)
tif_path = "LESC_NM EF_pos 3_plate 3 (1).tif"  # Replace with the actual .tif file path
avi_path = "LESC_NM EF_pos 3_plate 3 (1).avi"  # Replace with the desired output .avi path

# Load the .tif file as a stack
stack = IJ.openImage(tif_path)

if stack is None:
    print("Error: Unable to load the .tif file. Check the file path!")
else:
    # Set animation options (frame rate: 1 FPS or desired frame rate)
    IJ.run(stack, "Animation Options...", "frame=1")  # Update frame rate as needed

    # Export the stack as an .avi file
    IJ.run(stack, "AVI... ", f"compression=Uncompressed frame=1 save=[{avi_path}]")

    print(f"AVI file saved successfully at: {avi_path}")

    # Close the stack to free memory
    stack.close()
