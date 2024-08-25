import json
from classes import parse_json, Results, Ruleset
from create_gif import create_gif
from create_alive_cells_graph import create_alive_cells_graph
from collections import defaultdict
from typing import Dict, List, Tuple


def main():
    with open("grapherConfig.json", 'r') as config:
        configuration = json.load(config)

    gif_delay_seconds = configuration['delaySeconds']
    generate_gifs = configuration['generateGifs']
    generate_graphs = configuration['generateGraphs']

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

    # Create graphs to analyze alive cells in each evolution
    if generate_graphs:
        # Group simulations that have the same dimensions, initializationPercentage and ruleset
        grouped_results: Dict[Tuple[float, str, Ruleset], List[Results]] = defaultdict(list)
        for simulation in json_data.simulations:
            params = simulation.params
            results = simulation.results
            key = (params.initialization_percentage, params.dimension, params.ruleset)
            grouped_results[key].append(results)

        print('\nStarting alive cells graphs -------------------------------------------')
        index = 0
        for conditions, repetitions in grouped_results.items():
            index += 1
            create_alive_cells_graph(conditions, repetitions, './alive_cells_graph', index)
        print('Finished alive cells graphs ---------------------------------------------\n')


if __name__ == "__main__":
    main()
