

import json
from classes import parse_json, Evolution, Ruleset, Results
from collections import defaultdict
from create_gif import create_gif
from radius_scatter import create_scatter_plot
from typing import Dict, List, Tuple
import os


base_directory = "./radiusDistanceGraphs"

def create_directories_from_keys(grouped_results: Dict[Tuple[float, str, Ruleset], List[Results]]):
    os.makedirs(base_directory, exist_ok=True)

    for key in grouped_results.keys():
        # Convert the tuple into a valid directory name
        dir_name = f"{key[0]}_{key[1]}_{key[2].amount_to_revive}_{key[2].neighbours_to_die1}_{key[2].neighbours_to_die2}"
        # Replace invalid characters in the directory name (if any)
        dir_name = dir_name.replace(' ', '_').replace('/', '_')
        # Create the directory
        full_path = os.path.join(base_directory, dir_name)
        os.makedirs(full_path, exist_ok=True)
    


def main():

    json_data = parse_json('../files')


    grouped_results: Dict[Tuple[float, str, Ruleset], List[Results]] = defaultdict(list)
    for simulation in json_data.simulations:
        params = simulation.params
        results = simulation.results
        key = (params.initialization_percentage, params.dimension, params.ruleset)
        grouped_results[key].append(results)

    create_directories_from_keys(grouped_results)


    
    for key, resultList in grouped_results.items():
        for index, result in enumerate(resultList):
            radiusList = []
            for evolutionValue in result.evolutions.values():
                radiusList.append(evolutionValue.biggest_distance_from_center)
            
            # Construct the directory path
            dir_name = f"{key[0]}_{key[1]}_{key[2].amount_to_revive}_{key[2].neighbours_to_die1}_{key[2].neighbours_to_die2}".replace(' ', '_').replace('/', '_')
            output_path = os.path.join(base_directory, dir_name, f"simulation_{index}")
            
            # Create scatter plot with the constructed path
            create_scatter_plot(key,result.ending_status,radiusList, output_path)
    

if __name__ == "__main__":
    main()
