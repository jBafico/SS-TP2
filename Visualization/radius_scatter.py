import numpy as np
import matplotlib.pyplot as plt
from classes import Ruleset
from collections import defaultdict
from typing import Dict, List, Tuple

def create_scatter_plot(rules: Tuple[float, str, Ruleset], ending_status, data, filename=None):
    """
    Creates a scatter plot from the given data array.

    Parameters:
        data (array-like): An array of float or integer values.
        filename (str, optional): If provided, the scatter plot will be saved to this file.

    Returns:
        None: The function generates a scatter plot.
    """
    # Convert the data to a NumPy array (if not already)
    data = np.array(data)

    # Create an array for the x-axis (e.g., indices of data points)
    x = np.arange(len(data))

    # Create the scatter plot
    plt.scatter(x, data, color='blue', marker='o', label='Data Points')

    # Generate the data for the title
    title_data = [
        f"probability: {rules[0]}",
        f"dimension: {rules[1]}",
        f"Ending Status: {ending_status}"
    ]

    title_sub_data = [f"amountRevive: {rules[2].amount_to_revive}",f"neighborsToDie1: {rules[2].neighbours_to_die1}",f"neighborsToDie2: {rules[2].neighbours_to_die2}"]

    # Customize the plot
    plt.title(f"Longest radius distance to center evolution\n" + "|".join(title_data) + "\n" + "|".join(title_sub_data), fontsize=8)
    plt.xlabel("Epoch")
    plt.ylabel("Longest radius distance")
    plt.legend()

    # Set x-axis to only show integer values
    # plt.xticks(np.arange(min(x), max(x) + 1, 1))

    # Display the plot or save it to a file
    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()
