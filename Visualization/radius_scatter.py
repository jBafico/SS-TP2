import numpy as np
import matplotlib.pyplot as plt

def create_scatter_plot(data, filename=None):
    """
    Creates a scatter plot from the given data array.

    Parameters:
        data (array-like): An array of float or integer values.
        filename (str, optional): If provided, the scatter plot will be saved to this file.

    Returns:
        None: The function generates a scatter plot.
    """
    # Convert the data to a NumPy array (if not already)
    data = np.array(data)

    # Create an array for the x-axis (e.g., indices of data points)
    x = np.arange(len(data))

    # Create the scatter plot
    plt.scatter(x, data, color='blue', marker='o', label='Data Points')

    # Customize the plot
    plt.title("Scatter Plot")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.legend()

    # Display the plot or save it to a file
    if filename:
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

