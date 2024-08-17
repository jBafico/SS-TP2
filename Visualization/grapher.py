import json
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO

file_path= './files/simulationOutput.json'
# Step 1: Load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

frames = []
for matrix_data in data:
    # Convert matrix of booleans to numpy array
    array = np.array(matrix_data, dtype=np.uint8)
    
    # Create an image from the array
    plt.imshow(array, cmap='gray', vmin=0, vmax=1)
    plt.axis('off')
    
    # Save to a BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    
    # Append the image to the frames list
    buf.seek(0)
    frames.append(Image.open(buf))

# Step 4: Save the frames as an animated GIF
gif_path = './files/animation.gif'
frames[0].save(
    gif_path, 
    save_all=True, 
    append_images=frames[1:], 
    duration=100,  # Duration between frames in milliseconds
    loop=0         # 0 means infinite loop
)