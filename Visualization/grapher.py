import json
from classes import parse_json
from create_gif import create_gif

def main():
    with open("grapherConfig.json", 'r') as config:
        configuration = json.load(config)

    gif_delay_seconds = configuration['delaySeconds']

    # Load the most recent output json
    json_data = parse_json('../files')

    # Create gifs
    print('\nStarting GIF creation -------------------------------------------------')
    for i, simulation in enumerate(json_data.simulations):
        create_gif(simulation, gif_delay_seconds, i, './generated_gifs')
    print('Finished GIF creation ----------------------------------------------------\n')

    # Group simulations by repetitions
    for simulation in json_data.simulations:
        pass

    # Create graphs to analyze alive cells in each evolution
    print('\nStarting alive cells graphs -------------------------------------------')

    print('Finished alive cells graphs ----------------------------------------------\n')


if __name__ == "__main__":
    main()
