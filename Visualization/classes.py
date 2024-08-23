from typing import List, Dict

from load_most_recent_simulation import load_most_recent_simulation_json


# Define the classes corresponding to the JSON structure
class Ruleset:
    def __init__(self, amount_to_revive: int, neighbours_to_die1: int, neighbours_to_die2: int):
        self.amount_to_revive = amount_to_revive
        self.neighbours_to_die1 = neighbours_to_die1
        self.neighbours_to_die2 = neighbours_to_die2


class Params:
    def __init__(self, m: int, initialization_radius: int, initialization_percentage: float,
                 random_initial_conditions: bool, max_epochs: int, dimension: str,
                 ruleset: Ruleset, repetition_id: int):
        self.m = m
        self.initialization_radius = initialization_radius
        self.initialization_percentage = initialization_percentage
        self.random_initial_conditions = random_initial_conditions
        self.max_epochs = max_epochs
        self.dimension = dimension
        self.ruleset = ruleset
        self.repetition_id = repetition_id


class Evolution:
    def __init__(self, matrix: List[List[bool]], alive_cells: int, biggest_distance_from_center: float):
        self.matrix = matrix
        self.alive_cells = alive_cells
        self.biggest_distance_from_center = biggest_distance_from_center


class Results:
    def __init__(self, evolutions: Dict[str, Evolution], ending_status: str):
        self.evolutions = evolutions
        self.ending_status = ending_status


class Simulation:
    def __init__(self, params: Params, results: Results):
        self.params = params
        self.results = results

    @staticmethod
    def from_json(json_data: dict) -> 'Simulation':
        params_data = json_data['params']
        ruleset_data = params_data['ruleset']

        ruleset = Ruleset(
            amount_to_revive=ruleset_data['amountToRevive'],
            neighbours_to_die1=ruleset_data['neighboursToDie1'],
            neighbours_to_die2=ruleset_data['neighboursToDie2']
        )

        params = Params(
            m=params_data['m'],
            initialization_radius=params_data['initializationRadius'],
            initialization_percentage=params_data['initializationPercentage'],
            random_initial_conditions=params_data['randomInitialConditions'],
            max_epochs=params_data['maxEpochs'],
            dimension=params_data['dimension'],
            ruleset=ruleset,
            repetition_id=params_data['repetition_id']
        )

        evolutions = {
            key: Evolution(
                matrix=value['matrix'],
                alive_cells=value['aliveCells'],
                biggest_distance_from_center=value['biggestDistanceFromCenter']
            )
            for key, value in json_data['results'].items() if key.startswith('evolution_')
        }

        results = Results(
            evolutions=evolutions,
            ending_status=json_data['endingStatus']
        )

        return Simulation(params=params, results=results)

def parse_json(directory_path: str) -> List[Simulation]:
    simulations = []
    json_data = load_most_recent_simulation_json(directory_path)

    for simulation in json_data:
        simulations.append(Simulation.from_json(simulation))

    return simulations