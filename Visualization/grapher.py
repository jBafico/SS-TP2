import json
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio  # Importing imageio for GIF creation
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import io
import re
from pathlib import Path


SECONDS_MULTIPLIER = 1000

def main():
    with open("grapherConfig.json", 'r') as config:
        configuration = json.load(config)

    # Load the most recent output json
    data = load_most_recent_simulation_json('../files')

    for i, simulation in enumerate(data):
        params=simulation['params']
        dimension=params['dimension']

        initializationPercentage = params['initializationPercentage']
        ruleset = params['ruleset']
        amountToRevive = ruleset['amountToRevive']
        neighboursToDie1 = ruleset['neighboursToDie1']
        neighboursToDie2 = ruleset['neighboursToDie2']
        # List to store images for GIF
        images = []

        title= "System: " + dimension + " - Initialization Percentage: " + str(initializationPercentage) + " - Ruleset: [" + str(amountToRevive) + "," + str(neighboursToDie1) + "," + str(neighboursToDie2) + "] "

        if dimension=='2D':
           # Visualize the grid for each evolution
            for evolution_no, evolution_state in simulation['results'].items():
                grid = evolution_state['matrix']
                grid_array = np.array(grid)

                # Create a gradient colormap from green to white
                cmap = LinearSegmentedColormap.from_list("green_gradient", ["white", "green"])

                # Calculate distances from the center
                center = np.array(grid_array.shape) // 2
                distances = np.linalg.norm(np.indices(grid_array.shape).T - center, axis=-1)

                # Normalize distances to [0, 1]
                normalized_distances = distances / np.max(distances)

                # Plot only True values with gradient colors
                colored_grid = np.zeros(grid_array.shape)
                colored_grid[grid_array] = normalized_distances[grid_array]

                fig, ax = plt.subplots()
                ax.imshow(colored_grid, cmap=cmap, vmin=0, vmax=1)

                ax.grid(False)
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_title(title + evolution_no)

                # Save the current plot to an in-memory buffer
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                images.append(imageio.imread(buf))
                buf.close()
                plt.close()

           # Create a GIF from the collected images
            imageio.mimsave('simulation_evolution'+str(i)+'.gif', images, duration=configuration['delaySeconds'] * SECONDS_MULTIPLIER)
        elif dimension=='3D':
            # Loop through each evolution and create a plot for each
            for evolution_no, evolution_state in simulation['results'].items():
                grid = evolution_state['matrix']
                # Assume the key is dynamic and extract the 3D matrix
                grid_array = np.array(grid)

                # Create a 3D plot
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')

                # Define colors for True (green) and False (white)
                colors = np.empty(grid_array.shape, dtype=object)
                colors[grid_array] = 'green'
                colors[~grid_array] = 'white'

                # Set the title
                ax.set_title(title + evolution_no)

                # Plot the cubes
                ax.voxels(grid_array, facecolors=colors, edgecolor='k')

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
            imageio.mimsave('simulation_evolution'+str(i)+'.gif', images, duration= configuration['delaySeconds'] * SECONDS_MULTIPLIER)

            print("GIF created successfully: evolution_progression.gif")



def load_most_recent_simulation_json(directory_path: str):
    # Define the pattern for matching the file names
    pattern = re.compile(r"simulation_\d{8}_\d{6}\.json")

    # Get a list of all files in the directory that match the pattern
    files = [f for f in Path(directory_path).iterdir() if pattern.match(f.name)]

    if not files:
        print("No simulation files found.")
        return None

    # Sort files based on the timestamp in the filename
    most_recent_file = max(files, key=lambda f: f.stem.split('_')[1:])

    # Open and return the JSON data from the file
    with most_recent_file.open('r') as file:
        print(f'Opening file {most_recent_file.name}')
        return json.load(file)

if __name__ == "__main__":
    main()
