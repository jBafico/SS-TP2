import json
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio  # Importing imageio for GIF creation
from matplotlib.colors import ListedColormap


SECONDS_MULTIPLIER = 1000


with open("grapherConfig.json",'r') as config:
    configuration = json.load(config)

# Load JSON data from a file
with open('../../files/simulationOutput.json', 'r') as file:
    data = json.load(file)

# Define the color mapping
def get_color(value):
    return 1 if value else 0

# Custom colormap: 0 -> white, 1 -> green
cmap = ListedColormap(['white', 'green'])

# List to store images for GIF
images = []

# Visualize the grid for each evolution
for evolution in data['results']:
    for key, grid in evolution.items():
        # Convert the grid to a numpy array for easy manipulation
        grid_array = np.array(grid)

        # Plot the grid
        fig, ax = plt.subplots()
        ax.imshow(grid_array, cmap=cmap, vmin=0, vmax=1)

        # Hide grid lines
        ax.grid(False)

        # Hide axes ticks
        ax.set_xticks([])
        ax.set_yticks([])

        # Set the title
        ax.set_title(key)

        # Save the current figure to an image in memory
        plt.savefig("temp_image.png")
        images.append(imageio.imread("temp_image.png"))

        # Close the plot to avoid display during the process
        plt.close()

# Create a GIF from the collected images
imageio.mimsave('simulation_evolution.gif', images, duration=configuration['delaySeconds'] * SECONDS_MULTIPLIER)
