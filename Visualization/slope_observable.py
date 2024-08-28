import json
from classes import parse_json, Results, Ruleset
from create_gif import create_gif
from create_alive_cells_graph import create_alive_cells_graph
from create_max_radius_graphs import create_max_radius_graphs
from create_ending_type_graphs import create_ending_type_graphs
from collections import defaultdict
from typing import Dict, List, Tuple
import os
import numpy as np
import matplotlib.pyplot as plt


base_directory = "./observablesWithSlope"


def create_directories_from_keys(grouped_results: Dict[Tuple[str, Ruleset], List[Results]]):
    os.makedirs(base_directory, exist_ok=True)

    for key in grouped_results.keys():
        # Convert the tuple into a valid directory name
        dir_name = f"{key[0]}_{key[1].amount_to_revive}_{key[1].neighbours_to_die1}_{key[1].neighbours_to_die2}"
        # Replace invalid characters in the directory name (if any)
        dir_name = dir_name.replace(' ', '_').replace('/', '_')
        # Create the directory
        full_path = os.path.join(base_directory, dir_name)
        os.makedirs(full_path, exist_ok=True)


def calculate_slope(arr):
    # Generate x coordinates (indexes) based on the length of the array
    x = np.arange(len(arr))
    
    # y coordinates are the values in the array
    y = np.array(arr)
    
    # Calculate the means of x and y
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    
    # Calculate the slope (m) using the formula
    numerator = np.sum((x - mean_x) * (y - mean_y))
    denominator = np.sum((x - mean_x) ** 2)
    slope = numerator / denominator
    
    return slope

def graphic_observables(key ,data : Dict[float, List[Results]]):

    final_path = f"{base_directory}/{key[0]}_{key[1].amount_to_revive}_{key[1].neighbours_to_die1}_{key[1].neighbours_to_die2}/result.png"

    resultDicWithSlopes: Dict[float, List[float]] = {}


    for probabilityKey, currentResult in data.items():
        for result in currentResult:
            biggestRadiuses = []
            for evolution in result.evolutions.values():
                biggestRadiuses.append(evolution.biggest_distance_from_center)
            slope = calculate_slope(biggestRadiuses)
            if not probabilityKey in resultDicWithSlopes:
                resultDicWithSlopes[probabilityKey] = []
            resultDicWithSlopes[probabilityKey].append(slope)
    
    plot_data_with_error_bars(resultDicWithSlopes,final_path)


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
        ax.errorbar(i, means[i], yerr=std_devs[i], fmt='o', capsize=5, label=str(title))

    # Customize the plot
    ax.set_xticks(np.arange(len(titles)))
    ax.set_xticklabels(titles, rotation=45, ha='right')
    ax.set_xlabel("Porcentaje de inicializaciòn")
    ax.set_ylabel("Distancia")

    # Save the plot to the specified file
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


        



# def main():

#     json_data = parse_json('../files')


#     #ruleset + dimension => probabilidad + lista de resultados
#     grouped_results: Dict[Tuple[str, Ruleset], Dict[float,List[Results]]] = {}

    
#     for simulation in json_data.simulations:
#         key = (simulation.params.dimension,simulation.params.ruleset)
#         if not key in grouped_results:
#             grouped_results[key] = {}
#         if not simulation.params.initialization_percentage in grouped_results[key]:
#             grouped_results[key][simulation.params.initialization_percentage] = []
#         grouped_results[key][simulation.params.initialization_percentage].append(simulation.results)


#     create_directories_from_keys(grouped_results)


#     for key, data in grouped_results.items():
#             graphic_observables(key,data)


    
    




# if __name__ == "__main__":
#     main()
