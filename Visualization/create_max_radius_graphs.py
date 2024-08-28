import matplotlib.pyplot as plt
from typing import Tuple, List, Dict
from classes import Results, Ruleset
import os


def create_max_radius_graphs(
        conditions: Tuple[float, str, Ruleset],
        repeated_simulations: List[Results],
        directory_path: str,
        identifier: str
) -> None:
    # Create a scatter plot
    plt.figure(figsize=(10, 6))

    # Iterate over each repetition's results
    for i, results in enumerate(repeated_simulations):
        epochs = list(range(len(results.evolutions)))
        max_distances = [
            evolution.biggest_distance_from_center
            for key, evolution in sorted(results.evolutions.items())
        ]

        # Scatter plot for this repetition
        plt.scatter(epochs, max_distances, label=f'Repetition {i + 1}')

    # Set plot title and labels
    initialization_percentage, dimension, ruleset = conditions
    plt.title(
        f'Max Distance from Center\nInitialization: {initialization_percentage}, Dimension: {dimension}, Ruleset: {ruleset}')
    plt.xlabel('Epoch Number')
    plt.ylabel('Max Distance from Center')

    # Add legend
    plt.legend()

    # Create the directory if it does not exist
    os.makedirs(directory_path, exist_ok=True)

    # Save plot
    file_path = os.path.join(directory_path, f'max_radius_graph_{identifier}.png')
    plt.savefig(file_path)
    plt.close()

    print(f'Saved plot to {file_path}')
