from classes import Simulation
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio  # Importing imageio for GIF creation
from matplotlib.colors import LinearSegmentedColormap
import io
import os

SECONDS_MULTIPLIER = 1000


def create_gif(simulation: Simulation, delay_seconds: int, simulation_no: int, directory_path: str):
    print(f'Creating GIF no. {simulation_no}')

    params = simulation.params
    dimension = simulation.params.dimension
    ruleset = params.ruleset

    # If directory doesn't exist, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Determine subdirectory based on dimension
    subdirectory = os.path.join(directory_path, dimension)
    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)

    # List to store images for GIF
    images = []

    title = "System: " + dimension + " - Initialization Percentage: " + str(
        params.initialization_percentage) + " - Ruleset: [" + str(ruleset.amount_to_revive) + "," + str(
        ruleset.neighbours_to_die1) + "," + str(ruleset.neighbours_to_die2) + "] "

    if dimension == '2D':
        # Visualize the grid for each evolution

        for evolution_no, evolution_state in simulation.results.evolutions.items():
            grid = evolution_state.matrix
            grid_array = np.array(grid)

            # Create a gradient colormap from blue to red
            cmap = LinearSegmentedColormap.from_list("blue_red_gradient", ["blue", "red"])

            # Calculate distances from the center
            center = np.array(grid_array.shape) // 2
            distances = np.linalg.norm(np.indices(grid_array.shape).T - center, axis=-1)

            # Normalize distances to [0, 1]
            normalized_distances = distances / np.max(distances)

            # Initialize a white background grid
            colored_grid = np.ones((*grid_array.shape, 3))  # White background (R=1, G=1, B=1)

            # Apply the gradient only to True values
            for i in range(grid_array.shape[0]):
                for j in range(grid_array.shape[1]):
                    if grid_array[i, j]:
                        color_value = cmap(normalized_distances[i, j])
                        colored_grid[i, j] = color_value[:3]  # Extract RGB values

            fig, ax = plt.subplots()
            ax.imshow(colored_grid)

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

        # Save the GIF in the subdirectory
        gif_path = os.path.join(subdirectory, f'simulation_evolution_{simulation_no}.gif')
        imageio.mimsave(gif_path, images, duration=delay_seconds * SECONDS_MULTIPLIER)
        
    elif dimension == '3D':
        # Loop through each evolution and create a plot for each
        for evolution_no, evolution_state in simulation.results.evolutions.items():
            grid = evolution_state.matrix
            grid_array = np.array(grid)

            # Create a gradient colormap from green to white
            cmap = LinearSegmentedColormap.from_list("blue_red_gradient", ["white", "red"])

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

        # Save the GIF in the subdirectory
        gif_path = os.path.join(subdirectory, f'simulation_evolution_{simulation_no}.gif')
        imageio.mimsave(gif_path, images, duration=delay_seconds * SECONDS_MULTIPLIER)