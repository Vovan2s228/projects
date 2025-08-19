import numpy as np
import matplotlib.pyplot as plt

"""
In this exercise, you will implement functions to compute find the nearest neighbor in a dataset given any point.
Also, you will classify to which group a new point should belong based on the nearest neighbor. 
The nearest group is defined as the group containing the point closest to the new point (see also the figure in the template).

You have to write the functions yourself. This means that you can not use packages like scikit-learn.

Hint: Below, a script is provided to generate a image of the data. 
      However, this will only show in CodeGrade if you hand in the assignment or run in locally. 
      This is a similar image to the one provided in the template.
"""

def distance(pointA, pointB):
    """
    This calculates the Euclidean distance between two points: https://en.wikipedia.org/wiki/Euclidean_distance
    This is an optional function and is not needed to implement.

    Hint: You can use this as a helper function.

    :param pointA: The first coordinate
    :type pointA: list[float] or np.ndarray[(2,), float]
    :param pointB: The second coordinate
    :type pointB: list[float] or np.ndarray[(2,), float]
    :return: The distance between the two points
    :rtype: float
    """
    pointA = np.array(pointA)
    pointB = np.array(pointB)
    return np.sqrt(np.sum((pointA - pointB)**2))

def nearest_neighbour(data, point):
    """
    This function finds the nearest neighbour of "point" in the "data".

    :param data: All the points (neighbours) that need to be compared to "point".
    :type data: np.ndarray[(n, 2), float]
    :param point: The point of which you want to find the closest neighbour.
    :type point: list[float] or np.ndarray[(2,), float]
    :return: The nearest neighbour and the distance to that neighbour.
    :rtype: tuple[np.ndarray[(2,), float], float]
    """
    point = np.array(point)
    distances = np.sqrt(np.sum((data - point)**2, axis=1))
    min_index = np.argmin(distances)
    return data[min_index], distances[min_index]

def classify_point(data, point):
    """
    This function finds the nearest group based on the nearest neighbour of each group.
    Use `nearest_neighbour` in this function. The groups are labeled using their index.
    So, group 0 is the first group in the list of groups.

    :param data: A list of groups, where each group consists of all the points (neighbours) that need to be compared to "point".
    :type data: list[np.ndarray[(Any, 2), float]]
    :param point: The point of which you want to find the closest group.
    :type point: list[float] or np.ndarray[(2,), float]
    :return: The nearest group (index) and the nearest neighbour.
    :rtype: tuple[int, np.ndarray[(Any, 2), float]]
    """
    best_group = None
    best_distance = 9999999999
    best_neighbour = None

    for i, group in enumerate(data):
        neighbour, d = nearest_neighbour(group, point)
        if d < best_distance:
            best_distance = d
            best_group = i
            best_neighbour = neighbour

    return best_group + 1, best_neighbour


"""
You can find an example below to check if your code works.
"""
if __name__ == "__main__":
    RNG = np.random.default_rng()

    plt.matplotlib.rcParams['figure.figsize'] = [5, 4]  # This changes the size of the plot

    """
    Below you can change the parameters of the demo
    """
    centers = [(3, 8), (5, 3), (8, 6)]  # this changes where approximately the middle of each group is
    n_points = 20  # The number of points of each group
    new_point = (5, 5)  # The coordinate of the new point

    """
    You do not need to change the code below for the demo.
    """
    data = []
    for i, (x, y) in enumerate(centers):
        data.append(np.array(list(zip(RNG.normal(x, 1, n_points), RNG.normal(y, 1, n_points)))))
        plt.plot(data[-1][:,0], data[-1][:,1], 'o', label=f"group {i+1}")

    plt.plot(*nearest_neighbour(data[0], new_point)[0], 'k.', label="nearest point")
    plt.plot(*nearest_neighbour(data[1], new_point)[0], 'k.')
    plt.plot(*nearest_neighbour(data[2], new_point)[0], 'k.')

    nearest_group, nearest_point = classify_point(data, new_point)
    print(f"The nearest neighbour of point {new_point} is {tuple(nearest_point)} which belongs to group {nearest_group}.")

    plt.plot(*new_point, 'x', color='k')
    plt.legend()
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.savefig("nearest_neighbour_plot.png")
