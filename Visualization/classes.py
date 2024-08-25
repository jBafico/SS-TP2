from dataclasses import dataclass
from typing import List, Dict
from load_most_recent_simulation import load_most_recent_simulation_json

@dataclass
class Ruleset:
    amount_to_revive: int
    neighbours_to_die1: int
    neighbours_to_die2: int

    # We need it to be hashable
    def __hash__(self):
        return hash((self.amount_to_revive, self.neighbours_to_die1, self.neighbours_to_die2))

    def __eq__(self, other):
        if isinstance(other, Ruleset):
            return (
                    self.amount_to_revive == other.amount_to_revive and
                    self.neighbours_to_die1 == other.neighbours_to_die1 and
                    self.neighbours_to_die2 == other.neighbours_to_die2
            )
        return False

@dataclass
class GlobalParams:
    rulesets: Dict[str, Dict[str, Ruleset]]
    initialization_percentages: List[float]
    max_epochs: int
    m2d: int
    initialization_radius2d: int
    m3d: int
    initialization_radius3d: int
    repetitions: int
    random_initial_conditions: bool

@dataclass
class Params:
    dimension: str
    repetition_id: int
    initialization_percentage: float
    ruleset: Ruleset

@dataclass
class Evolution:
    matrix: List[List[bool]]
    alive_cells: int
    biggest_distance_from_center: float

@dataclass
class Results:
    evolutions: Dict[str, Evolution]
    ending_status: str
    average_biggest_radius_distance: float

@dataclass
class Simulation:
    params: Params
    results: Results

@dataclass
class JsonData:
    global_params: GlobalParams
    simulations: List[Simulation]


def parse_json(directory_path: str) -> JsonData:
    json_data = load_most_recent_simulation_json(directory_path)

    global_params_data = json_data['global_params']

    # Parse rulesets
    rulesets = {
        dimension: {
            variant: Ruleset(
                amount_to_revive=ruleset_data['amountToRevive'],
                neighbours_to_die1=ruleset_data['neighboursToDie1'],
                neighbours_to_die2=ruleset_data['neighboursToDie2']
            )
            for variant, ruleset_data in dimension_rulesets.items()
        }
        for dimension, dimension_rulesets in global_params_data['rulesets'].items()
    }

    global_params = GlobalParams(
        rulesets=rulesets,
        initialization_percentages=global_params_data['initializationPercentages'],
        max_epochs=global_params_data['maxEpochs'],
        m2d=global_params_data['m2D'],
        initialization_radius2d=global_params_data['initializationRadius2D'],
        m3d=global_params_data['m3D'],
        initialization_radius3d=global_params_data['initializationRadius3D'],
        repetitions=global_params_data['repetitions'],
        random_initial_conditions=global_params_data['randomInitialConditions']
    )

    # Parse simulations
    simulations = []
    for simulation_data in json_data['simulations']:
        params_data = simulation_data['params']
        ruleset = params_data['ruleset']

        params = Params(
            dimension=params_data['dimension'],
            repetition_id=params_data['repetition_id'],
            initialization_percentage=params_data['initializationPercentage'],
            ruleset=Ruleset(
                ruleset['amountToRevive'],
                ruleset['neighboursToDie1'],
                ruleset['neighboursToDie2']
            )
        )

        evolutions = {
            key: Evolution(
                matrix=value['matrix'],
                alive_cells=value['aliveCells'],
                biggest_distance_from_center=value['biggestDistanceFromCenter']
            )
            for key, value in simulation_data['results'].items() if key.startswith('evolution_')
        }

        results = Results(
            evolutions=evolutions,
            ending_status=simulation_data['endingStatus'],
            average_biggest_radius_distance=simulation_data['averageBiggestRadiusDistance']
        )

        simulations.append(Simulation(params=params, results=results))

    return JsonData(global_params=global_params, simulations=simulations)
