import json
from classes import parse_json, Results, Ruleset
from create_gif import create_gif
from create_alive_cells_graph import create_alive_cells_graph
from create_max_radius_graphs import create_max_radius_graphs
from create_ending_type_graphs import create_ending_type_graphs
from collections import defaultdict
from typing import Dict, List, Tuple


def main():
    with open("grapherConfig.json", 'r') as config:
        configuration = json.load(config)

    gif_delay_seconds = configuration['delaySeconds']
    generate_gifs = configuration['generateGifs']
    generate_alive_cells_graphs = configuration['generateAliveCellsGraphs']
    generate_max_radius_graphs = configuration['generateMaxRadiusGraphs']
    generate_ending_type_graphs = configuration['generateEndingTypeGraphs']

    # Load the most recent output json
    print('\nParsing the json ----------------------------------------------------------')
    json_data = parse_json('../files')
    print('Finished parsing the json ---------------------------------------------------\n')

    # Create gifs
    if generate_gifs:
        print('\nStarting GIF creation -------------------------------------------------')
        for i, simulation in enumerate(json_data.simulations):
            create_gif(simulation, gif_delay_seconds, i, './generated_gifs')
        print('Finished GIF creation ---------------------------------------------------\n')

    # Group simulations that have the same dimensions, initializationPercentage and ruleset
    grouped_results: Dict[Tuple[float, str, Ruleset], List[Results]] = defaultdict(list)
    for simulation in json_data.simulations:
        params = simulation.params
        results = simulation.results
        key = (params.initialization_percentage, params.dimension, params.ruleset)
        grouped_results[key].append(results)

    # Create graphs to analyze alive cells in each evolution
    if generate_alive_cells_graphs:
        print('\nStarting alive cells graphs -------------------------------------------')
        index = 0
        for conditions, repetitions in grouped_results.items():
            index += 1
            create_alive_cells_graph(conditions, repetitions, './alive_cells_graphs', index)
        print('Finished alive cells graphs ---------------------------------------------\n')

    # Generate graphs to analyze the furthest alive cell from the middle in each evolution
    if generate_max_radius_graphs:
        print('\nStarting alive cells graphs -------------------------------------------')
        index = 0
        for conditions, repetitions in grouped_results.items():
            index += 1
            create_max_radius_graphs(conditions, repetitions, './max_radius_graphs', index)
        print('Finished alive cells graphs ---------------------------------------------\n')

    # Group data that has the same dimension and ruleset
    grouped_results_2: Dict[Tuple[str, Ruleset], Dict[float, List[Results]]] = defaultdict(dict)
    for simulation in json_data.simulations:
        params = simulation.params
        results = simulation.results
        key = params.dimension, params.ruleset
        initialization_percentage = params.initialization_percentage
        grouped_results_2[key].setdefault(initialization_percentage, []).append(results)

    # Generate graphs to analyze how each simulation ends
    if generate_ending_type_graphs:
        print('\nStarting ending type graphs -------------------------------------------')
        index = 0
        for conditions, repetitions_by_init_percentage in grouped_results_2.items():
            index += 1
            create_ending_type_graphs(conditions, repetitions_by_init_percentage, './ending_type_graphs', index)
        print('Finished ending type graphs ---------------------------------------------\n')

if __name__ == "__main__":
    main()
