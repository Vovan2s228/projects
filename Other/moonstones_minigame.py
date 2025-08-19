# Importing libraries
import numpy as np
import random


# Main function. Here all functions mix in one program
def main():
    moon_size, moonstone_number, moon = get_moon()
    print(moon)
    coordinates = find_moonstones(moon)
    x_pos = 0
    y_pos = 0
    path_coord = [[0, 0]]
    path_coord = path(coordinates, x_pos, y_pos, path_coord)
    print(f"Path by coordinates: {path_coord}")
    print(f"The shortest path to get all stones is {len(path_coord) - 1} steps")
    moon = draw_path(path_coord, moon, coordinates)
    print("Here is the path: ")
    print(moon)


# Function to create the moon and moonstones
def get_moon():
    moon_size = input("On what moon size do you want your robot to search (5, 6, 7 or 8)? ")
    moonstone_number = input("How many moonstones are you looking for? ")
    try:
        moon_size = int(moon_size)
        moonstone_number = int(moonstone_number)
        if moon_size in [5, 6, 7, 8] and 0 < moonstone_number < moon_size ** 2:
            moon = np.zeros((moon_size, moon_size))
            while moon[0, 0] == 1 or ((moon == 1).sum() < moonstone_number):
                moon[0, 0] = 0
                moon[random.randint(0, moon_size - 1), random.randint(0, moon_size - 1)] = 1
            return moon_size, moonstone_number, moon
        else:
            print("Oops! You either entered an invalid input or asked to find more moonstones than possible")
            return get_moon()

    except:
        print("Your input is invalid!")
        return get_moon()


# Function to get the coordinates of moonstones on moon
def find_moonstones(moon):
    coordinates = []
    for i, j in enumerate(moon):  # enumerate() returns a tuple with the counter and value, which means we don't need to create another counter
        for k, n in enumerate(j):  # since this is an array, it has a list of lists, so for each row we need to check each element of this row
            if n == 1:
                coordinates += [[k, i]]  # creates a list of lists with coordinates
    print(f"Moonstone coordinates: {coordinates}")
    return coordinates


# This function calculates and returns the best path for our robot to go
def path(coordinates, x_pos, y_pos, path_coord):
    a = 0
    b = 0
    for n in range(len(coordinates)):  # a for loop to check the closest moonstone from the moonstone the robot is currently on
        distances = []
        for i in coordinates:
            distances += [int(abs(i[0] - a) + abs(i[1] - b))]  # creates a list of distances from any moonstone to the moonstone with coordinates (a,b)
        min_sum_index = distances.index(min(distances))  # finds the minimal distance
        closest_moonstone = coordinates[min_sum_index]  # finds the corresponding moonstone to its coordinates
        a, b = closest_moonstone[0], closest_moonstone[1]

        while a != x_pos:  # while loops that "move" the robot around and create a list of coordinates the robot has passed
            if a > x_pos:
                x_pos += 1
            else:
                x_pos += -1
            path_coord += [[x_pos, y_pos]]
        while b != y_pos:
            if b > y_pos:
                y_pos += 1
            else:
                y_pos += -1
            path_coord += [[x_pos, y_pos]]
        coordinates.pop(min_sum_index)  # deletes the moonstones that the robot has passed from the coordinates list

    return path_coord


# Function that shows the path on the array
def draw_path(path_coord, moon, coordinates):
    for i in path_coord:
        moon[i[1], i[0]] = 1  # adds a 1 everywhere where the robot has walked
    return moon


if __name__ == "__main__":  # allows the program to only be executed if a user runs it directly
    main()
