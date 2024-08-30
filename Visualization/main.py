import json
from alive_cells_slope_observables import graphic_observables_alive_cells
from classes import parse_json, Results, Ruleset
from create_gif import create_gif
from create_alive_cells_graph import create_alive_cells_graph
from create_max_radius_graphs import create_max_radius_graphs
from create_ending_type_graphs import create_ending_type_graphs
from collections import defaultdict
from typing import Dict, List, Tuple
from create_steps_until_death_observable import create_steps_until_death_observable
from slope_observable import create_directories_from_keys, graphic_observables


def main():
    with open("grapherConfig.json", 'r') as config:
        configuration = json.load(config)

    gif_delay_seconds = configuration['delaySeconds']
    generate_gifs = configuration['generateGifs']
    generate_alive_cells_graphs = configuration['generateAliveCellsGraphs']
    generate_max_radius_graphs = configuration['generateMaxRadiusGraphs']
    generate_ending_type_graphs = configuration['generateEndingTypeGraphs']
    generate_individual_max_radius_graphs = configuration['generateIndividualMaxRadiusGraphs']
    generate_steps_until_end_graphs = configuration['generateStepsUntilEndObservable']
    generate_slopes_observables = configuration['generateSlopesObservables']
    generate_alive_cells_observables = configuration["aliveCellsObservables"]

    # Load the most recent output json
    print('\nParsing the json ----------------------------------------------------------')
    json_data = parse_json('../files')
    print('Finished parsing the json ---------------------------------------------------\n')

    # Group simulations that have the same dimensions, initializationPercentage and ruleset
    print('Creating simulations by repetitions array -----------------------------------')
    simulations_by_repetitions: Dict[Tuple[float, str, Ruleset], List[Results]] = defaultdict(list)
    for simulation in json_data.simulations:
        params = simulation.params
        results = simulation.results
        key = (params.initialization_percentage, params.dimension, params.ruleset)
        simulations_by_repetitions[key].append(results)
    print('Finished creating simulations by repetitions array --------------------------\n')

    # Create graphs to analyze alive cells in each evolution
    if generate_alive_cells_graphs:
        print('\nStarting alive cells graphs -------------------------------------------')
        for conditions, repetitions in simulations_by_repetitions.items():
            create_alive_cells_graph(repetitions, './alive_cells_graphs', get_tuple_str(conditions))
        print('Finished alive cells graphs ---------------------------------------------\n')

    # Generate graphs to analyze the furthest alive cell from the middle in each evolution
    if generate_max_radius_graphs:
        print('\nStarting max radius graphs --------------------------------------------')
        for conditions, repetitions in simulations_by_repetitions.items():
            create_max_radius_graphs(repetitions, './max_radius_graphs', get_tuple_str(conditions))
        print('Finished max radius graphs ----------------------------------------------\n')

    if generate_individual_max_radius_graphs:
        print('\nStarting individual max radius graphs ---------------------------------')
        for conditions, repetitions in simulations_by_repetitions.items():
            repetition_no = 1
            for repetition in repetitions:
                repetition_no += 1
                create_max_radius_graphs([repetition], './individual_max_radius_graphs', f"{get_tuple_str(conditions)}_{repetition_no}")
        print('Finished individual max radius graphs -----------------------------------\n')

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
        for conditions, repetitions_by_init_percentage in grouped_results_2.items():
            create_ending_type_graphs(conditions, repetitions_by_init_percentage, './ending_type_graphs', get_tuple_str(conditions))
        print('Finished ending type graphs ---------------------------------------------\n')

    if generate_steps_until_end_graphs:
        print('\nStarting observables by steps------------------------------------------')
        for conditions, repetitions_by_init_percentage in grouped_results_2.items():
            create_steps_until_death_observable(conditions, repetitions_by_init_percentage)
        print("\nFinished observables by steps------------------------------------------")

    if generate_slopes_observables:
        print('\nStarting observables by steps-------------------------------------------')
        create_directories_from_keys(grouped_results_2)
        for conditions, repetitions_by_init_percentage in grouped_results_2.items():
            graphic_observables(conditions, repetitions_by_init_percentage)
        print("\nFinished observables by steps-------------------------------------------")
    
    if generate_alive_cells_observables:
        print('\nStarting observables by alive cells---------------------------------------')
        for conditions, repetitions_by_init_percentage in grouped_results_2.items():
            graphic_observables_alive_cells(conditions, repetitions_by_init_percentage)
        print("\nFinished observables by steps-------------------------------------------")


    # Create gifs
    if generate_gifs:
        index = 0
        print('\nStarting GIF creation -------------------------------------------------')
        for conditions, repetitions in simulations_by_repetitions.items():
            index += 1
            result = repetitions[0]  # We only grab the first repetition
            identifier = get_tuple_str(conditions)
            initialization_percentage = conditions[0]
            dimension = conditions[1]
            if initialization_percentage != 0.5 or dimension != '3D':
                continue
            create_gif(result, dimension, gif_delay_seconds, identifier, index, './generated_gifs')
        print('Finished GIF creation ---------------------------------------------------\n')



def get_tuple_str(to_convert: Tuple[float, str, Ruleset] | Tuple[str, Ruleset]) -> str:
    if len(to_convert) == 2:
        return f'{to_convert[0]}_{to_convert[1]}'
    elif len(to_convert) == 3:
        return f'{to_convert[1]}_{to_convert[2]}_{to_convert[0]}'
    else:
        raise ValueError("Expected a tuple of length 2 or 3.")


if __name__ == "__main__":
    main()
