import json
from classes import parse_json
from create_gif import create_gif

def main():
    with open("grapherConfig.json", 'r') as config:
        configuration = json.load(config)

    gif_delay_seconds = configuration['delaySeconds']

    # Load the most recent output json
    simulations = parse_json('../files')

    # Create gifs
    print('\nStarting GIF creation -------------------------------------------------')
    for i, simulation in enumerate(simulations):
        create_gif(simulation, gif_delay_seconds, i, './generated_gifs')
    print('Finished GIF creation ----------------------------------------------------\n')


if __name__ == "__main__":
    main()
