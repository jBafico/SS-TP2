

import json
from classes import parse_json, Evolution
from create_gif import create_gif
from radius_scatter import create_scatter_plot
from typing import Dict, List

import os
import numpy as np
import matplotlib.pyplot as plt

def plot_data_with_error_bars(data, output_path):
    """
    Creates a scatter plot with error bars for each title in the provided dictionary
    and saves the plot to a file at the specified output path.

    Parameters:
        data (Dict[str, List[float]]): A dictionary mapping titles (str) to lists of floats.
        output_path (str): The file path where the plot will be saved (including file extension, e.g., 'plot.png').

    Returns:
        None: The function generates and saves the plot to the specified file.
    """
    titles = list(data.keys())
    means = []
    std_devs = []

    # Calculate means and standard deviations for each title
    for title, values in data.items():
        means.append(np.mean(values))
        std_devs.append(np.std(values))

    # Create the plot
    fig, ax = plt.subplots()

    # Plot each title's mean with error bars
    for i, title in enumerate(titles):
        ax.errorbar(i, means[i], yerr=std_devs[i], fmt='o', capsize=5, label=title)

    # Customize the plot
    ax.set_xticks(np.arange(len(titles)))
    ax.set_xticklabels(titles, rotation=45, ha='right')
    ax.set_title("Data with Mean and Error Bars for Each Title")
    ax.set_xlabel("Initialization Percentages")
    ax.set_ylabel("Radius values")
    ax.legend(loc='upper right')

    # Save the plot to the specified file
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()









def main():

    json_data = parse_json('../files')


    pathData = "./radiusAvgPerInitPercentage"
    if not os.path.exists(pathData):
        os.makedirs(pathData)




    # Type hint for a dictionary that maps float to list of floats
    percentages_to_avg_radius_2d : Dict[str, List[float]] = {}
    percentages_to_avg_radius_3d : Dict[str, List[float]] = {}



    for current_percentage in json_data.global_params.initialization_percentages:
        percentages_to_avg_radius_2d[str(current_percentage)] = []
        percentages_to_avg_radius_3d[str(current_percentage)] = []


    for simulation in json_data.simulations:
        for evolution in simulation.results.evolutions.values():
            if simulation.params.dimension == "2D":
                percentages_to_avg_radius_2d[str(simulation.params.initialization_percentage)].append(evolution.biggest_distance_from_center)
            else:
                percentages_to_avg_radius_3d[str(simulation.params.initialization_percentage)].append(evolution.biggest_distance_from_center)


    plot_data_with_error_bars(percentages_to_avg_radius_2d,f"{pathData}/2D.png")

    

if __name__ == "__main__":
    main()
