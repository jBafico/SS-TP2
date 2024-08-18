import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import imageio
import io


with open("./grapher3dconfig.json",'r') as configFile:
    configData = json.load(configFile)

# Load JSON data from the specified file
with open("../files/simulationOutput3D.json", "r") as outputData:
    data = json.load(outputData)

# List to store images
images = []

# Loop through each evolution and create a plot for each
for i, evolution_data in enumerate(data):
    # Assume the key is dynamic and extract the 3D matrix
    key = list(evolution_data.keys())[0]
    evolution_array = np.array(evolution_data[key])

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Define colors for True (green) and False (white)
    colors = np.empty(evolution_array.shape, dtype=object)
    colors[evolution_array] = 'green'
    colors[~evolution_array] = 'white'

    # Plot the cubes
    ax.voxels(evolution_array, facecolors=colors, edgecolor='k')

    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Save the current plot to an in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    images.append(imageio.imread(buf))
    buf.close()
    plt.close()

# Create a GIF from the images stored in memory
imageio.mimsave('evolution_progression3d.gif', images, duration= configData['delaySeconds'] * 1000)

print("GIF created successfully: evolution_progression.gif")
