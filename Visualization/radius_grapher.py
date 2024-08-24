

import json
from classes import parse_json, Evolution
from create_gif import create_gif
from radius_scatter import create_scatter_plot
import os

def main():

    json_data = parse_json('../files')


    pathData = "./radiusDistanceGraphs"
    if not os.path.exists(pathData):
        os.makedirs(pathData)



    for simulation in json_data.simulations:
        radiusList = []
        for index, evolution in enumerate(simulation.results.evolutions.values()):
            radiusList.append(evolution.biggest_distance_from_center)
        create_scatter_plot(radiusList, f"{pathData}/simulation_{simulation.params.dimension}_{index}")
    
    

if __name__ == "__main__":
    main()
