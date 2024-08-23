import json
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio  # Importing imageio for GIF creation
from matplotlib.colors import LinearSegmentedColormap
import io
from classes import parse_json

SECONDS_MULTIPLIER = 1000

def main():
    with open("grapherConfig.json", 'r') as config:
        configuration = json.load(config)

    # Load the most recent output json
    simulations = parse_json('../files')

    for i, simulation in enumerate(simulations):
        params = simulation.params
        dimension = simulation.params.dimension
        ruleset = params.ruleset

        # List to store images for GIF
        images = []

        title= "System: " + dimension + " - Initialization Percentage: " + str(params.initialization_percentage) + " - Ruleset: [" + str(ruleset.amount_to_revive) + "," + str(ruleset.neighbours_to_die1) + "," + str(ruleset.neighbours_to_die2) + "] "

        if dimension=='2D':
           # Visualize the grid for each evolution
            for evolution_no, evolution_state in simulation.results.evolutions.items():
                grid = evolution_state
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
            print("in 3d")
            # Loop through each evolution and create a plot for each
            for evolution_no, evolution_state in simulation.results.evolutions.items():
                grid = evolution_state['matrix']
                grid_array = np.array(grid)

                # Create a gradient colormap from green to white
                #cmap = LinearSegmentedColormap.from_list("red_green_gradient", ["red", "green"])

                cmap = LinearSegmentedColormap.from_list("green_gradient", ["white", "green"])

                # Calculate distances from the center
                center = np.array(grid_array.shape) // 2
                distances = np.linalg.norm(np.indices(grid_array.shape).T - center, axis=-1)

                # Normalize distances to [0, 1]
                normalized_distances = distances / np.max(distances)

                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')

                # Assign RGBA colors based on distance and True/False values
                colors = np.zeros(grid_array.shape + (4,), dtype=float)  # RGBA colors
                colors[grid_array] = cmap(normalized_distances[grid_array])
                colors[~grid_array, 3] = 0  # Set alpha to 0 for false values

                ax.set_title(title + evolution_no)
                ax.voxels(grid_array, facecolors=colors, edgecolor='k')

                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                images.append(imageio.imread(buf))
                buf.close()
                plt.close()

            # Create a GIF from the images stored in memory
            imageio.mimsave('simulation_evolution'+str(i)+'.gif', images, duration= configuration['delaySeconds'] * SECONDS_MULTIPLIER)

            print("GIF created successfully: evolution_progression.gif")


if __name__ == "__main__":
    main()
