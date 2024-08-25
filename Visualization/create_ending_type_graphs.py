import os
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, Dict, List
from classes import Results, Ruleset

# Define a fixed color map for ending statuses
ENDING_STATUS_COLORS = {
    'FINISHED_WITH_BORDER': 'red',
    'FINISHED_WITH_ALL_DEAD': 'blue',
    'FINISHED_WITH_SAME_AS_PREVIOUS_STATE': 'green',
    'FINISHED_WITH_MAX_EPOCHS': 'purple',
}

def create_ending_type_graphs(
        conditions: Tuple[str, Ruleset],
        repeated_simulations_by_init_perc: Dict[float, List[Results]],
        directory_path: str,
        index: int
) -> None:
    # Ensure the directory exists
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Count occurrences of each ending status per initialization percentage
    ending_status_counts = {}
    all_ending_statuses = set()

    for init_perc, results_list in repeated_simulations_by_init_perc.items():
        ending_status_counts[init_perc] = {}
        for results in results_list:
            status = results.ending_status
            all_ending_statuses.add(status)
            if status not in ending_status_counts[init_perc]:
                ending_status_counts[init_perc][status] = 0
            ending_status_counts[init_perc][status] += 1

    # Prepare data for plotting
    sorted_init_percs = sorted(ending_status_counts.keys())
    sorted_statuses = sorted(all_ending_statuses)
    bar_width = 0.15  # Width of each bar
    indices = np.arange(len(sorted_init_percs))

    # Plotting
    plt.figure(figsize=(12, 8))

    for i, status in enumerate(sorted_statuses):
        counts = [ending_status_counts[init_perc].get(status, 0) for init_perc in sorted_init_percs]
        color = ENDING_STATUS_COLORS.get(status, 'gray')  # Default to gray if not in the color map
        plt.bar(indices + i * bar_width, counts, bar_width, label=status, color=color)

    # Set plot labels and title
    dimension, ruleset = conditions
    plt.xlabel('Initialization Percentage')
    plt.ylabel('Number of Repetitions')
    plt.title(f'Ending Status by Initialization Percentage\nDimension: {dimension}, Ruleset: {ruleset}')
    plt.xticks(indices + bar_width * (len(sorted_statuses) - 1) / 2, sorted_init_percs)
    plt.legend(title='Ending Status')

    # Save plot
    file_path = os.path.join(directory_path, f'ending_type_graph_{index}.png')
    plt.savefig(file_path)
    plt.savefig(file_path)
    plt.close()

    print(f'Saved plot to {file_path}')

