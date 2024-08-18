import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



with open("../files/simulationOutput3D.json","r") as outputData:
    data = json.load(outputData)

with open("./grapher3dmomentViewerConfig.json","r") as configFile:
    configData = json.load(configFile)



index = configData['index']

evolution = data[index][f"evolution_{index}"]

# Convert the boolean matrix to a NumPy array
evolution_array = np.array(evolution)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define colors for True (green) and False (white)
colors = np.empty(evolution_array.shape, dtype=object)
colors[evolution_array] = 'green'
colors[~evolution_array] = 'white'

# Plot the cubes
ax.voxels(evolution_array, facecolors=colors, edgecolor='k')

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()