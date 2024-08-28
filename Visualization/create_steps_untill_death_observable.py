


from typing import Dict, List, Tuple

from matplotlib import pyplot as plt
import numpy as np

from classes import Results, Ruleset
import os
from matplotlib.ticker import FuncFormatter





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
    ax.set_xlabel("Porcentajes de inicializaciòn")
    ax.set_ylabel("Evolulciones")


    # Save the plot to the specified fi
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()



base_directory = "./untillDeathObservables"
def create_steps_untill_death_observable(conditions: Tuple[str, Ruleset], data : Dict[float, List[Results]]):
    subDirectory = f"{conditions[0]}_{conditions[1].amount_to_revive}_{conditions[1].neighbours_to_die1}_{conditions[1].neighbours_to_die2}"

    floatDict : Dict[float, List[int]] = {}
    for currentProbability, currentResult in data.items():
        stepsForCurrentProbability = []
        for result in currentResult:
            stepsForCurrentProbability.append(len(result.evolutions) - 1) # -1 porque no contamos el paso 0
        floatDict[currentProbability] = stepsForCurrentProbability


    current_path = f"{base_directory}/{subDirectory}"
    os.makedirs(current_path, exist_ok=True)
    plot_data_with_error_bars(floatDict,f"{current_path}/result.png")



