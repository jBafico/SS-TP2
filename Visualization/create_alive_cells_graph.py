import os
import matplotlib.pyplot as plt
from typing import List, Tuple
from classes import Ruleset, Results


def create_alive_cells_graph(
        conditions: Tuple[float, str, Ruleset],
        repeated_simulations: List[Results],
        directory_path: str,
        identifier: str
) -> None:
    plt.figure(figsize=(10, 6))

    # Define a list of colors, one for each repetition
    colors = [
        'blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray',
        'olive', 'cyan', 'magenta', 'yellow', 'black', 'lime', 'navy',
        'teal', 'maroon', 'gold', 'lightblue', 'darkgreen'
    ]

    # Iterate over each repetition and plot with a different color
    for idx, results in enumerate(repeated_simulations):
        epochs = []
        alive_cells_counts = []

        # Iterate over each evolution in the current repetition
        for key in sorted(results.evolutions.keys(), key=lambda x: int(x.split('_')[1])):
            evolution = results.evolutions[key]
            epochs.append(int(key.split('_')[1]))  # Extract the epoch number from the key
            alive_cells_counts.append(evolution.alive_cells)

        # Plot the data for the current repetition
        plt.plot(epochs, alive_cells_counts, label=f'Repetition {idx + 1}', color=colors[idx])

    # Extract information from conditions for the title
    initialization_percentage, dimension, ruleset = conditions
    title = f'Alive Cells Progression | {dimension} | Init %: {initialization_percentage} | Ruleset: {ruleset}'

    plt.xlabel('Epoch')
    plt.ylabel('Alive Cells')
    plt.title(title)
    plt.legend(loc='best')

    # Create the directory if it does not exist
    os.makedirs(directory_path, exist_ok=True)

    # Save the figure with a unique filename
    file_path = os.path.join(directory_path, f'alive_cells_progression_{identifier}.png')
    plt.savefig(file_path)
    plt.close()

    print(f'Saved plot to {file_path}')
