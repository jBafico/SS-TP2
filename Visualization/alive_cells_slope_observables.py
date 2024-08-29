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

from create_steps_until_death_observable import plot_data_with_error_bars
from slope_observable import calculate_slope


base_directory = "./aliveCellsObservable"


def graphic_observables_alive_cells(key, data: Dict[float, List[Results]]):
    # Define the final path for the result.png file
    final_path = f"{base_directory}/{key[0]}_{key[1].amount_to_revive}_{key[1].neighbours_to_die1}_{key[1].neighbours_to_die2}/result.png"
    
    # Ensure the directory exists; if not, create it
    os.makedirs(os.path.dirname(final_path), exist_ok=True)

    resultDicWithSlopes: Dict[float, List[float]] = {}

    for probabilityKey, currentResult in data.items():
        for result in currentResult:
            aliveCells = []
            for evolution in result.evolutions.values():
                aliveCells.append(evolution.alive_cells)
            slope = calculate_slope(aliveCells)
            if not probabilityKey in resultDicWithSlopes:
                resultDicWithSlopes[probabilityKey] = []
            resultDicWithSlopes[probabilityKey].append(slope)
    
    plot_data_with_error_bars(resultDicWithSlopes, final_path)

