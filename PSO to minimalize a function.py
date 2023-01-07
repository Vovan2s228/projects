import numpy as np
import matplotlib.pyplot as plt
# importing libraries


def function(x, y):
    z = (x - np.pi) ** 2 + (y - np.e) ** 2 + np.sin(3 * x+0.75) + np.cos(4 * y - 2.13)  # our function
    return z


def movement(w, c1, c2, V, X, pb, gb_coord, r1, r2):
    V = w * V + c1*r1*(pb - X) + c2*r2*(gb_coord - X)  # function responsible for "movement" of particles
    X += V
    return V, X


def start(n):
    start_pos = np.random.random_sample((2, n)) * 5   # initialisation. Creating random particles with random velocities
    start_vel = np.random.randn(2, n) * 0.1
    return start_pos, start_vel


def first_best(n, start_pos, start_vel):  # function to find the first global and personal best coordinates and values
    gb_value = 99999999
    pb = []
    pb_value = []
    X = []
    V = []
    # reshaping the arrays to avoid an error
    for i in range(len(start_pos[0])):
        X.append([start_pos[0][i], start_pos[1][i]])
    X = np.array(X)
    for i in range(len(start_vel[0])):
        V.append([start_vel[0][i], start_vel[1][i]])
    V = np.array(V)
    # getting the global and personal best coordinates and values
    for i in range(n):
        x = start_pos[0][i]
        y = start_pos[1][i]
        z = function(x, y)
        pb.append([x, y])
        pb_value.append([z])
        if z < gb_value:
            gb_value = np.array([z])
            gb_coord = np.array([x, y])
    pb = np.array(pb)
    pb_value = np.array(pb_value)

    return gb_coord, gb_value, pb, pb_value, X, V


def best(w, c1, c2, gb_coord, gb_value, pb, pb_value, X, V, n):  # function to get the new global coordinates and values after moving particles
    r1 = np.random.rand(1)
    r2 = np.random.rand(1)
    X, V = movement(w, c1, c2, V, X, pb, gb_coord, r1, r2)
    z_value = []
    for i in range(n):
        x = X[i][0]
        y = X[i][1]
        z = function(x, y)
        z_value.append(z)
        if z < float(gb_value):
            gb_value = z
            gb_coord = np.array([x, y])
    z_value = np.array(z_value)
    for i in range(n):
        if float(pb_value[i]) > z_value[i]:
            pb_value[i] = z_value[i]
            pb[i] = X[i]
    return gb_coord, gb_value


def graph(coordinates, values):  # plotting all the particles on a 3d plot
    x_coord = []
    y_coord = []
    for i in range(len(coordinates)):
        x_coord.append(coordinates[i][0])
        y_coord.append(coordinates[i][1])
    plt.figure()
    ax = plt.axes(projection="3d")
    ax.scatter(x_coord, y_coord, values,  c=values, cmap='viridis', linewidth=0.5)
    plt.title("Plot of all particles on the function using PSO")
    # changing the default colors for better looks
    ax.set_facecolor("black")
    [t.set_color('red') for t in ax.xaxis.get_ticklines()]
    [t.set_color('red') for t in ax.xaxis.get_ticklabels()]
    [t.set_color('red') for t in ax.yaxis.get_ticklines()]
    [t.set_color('red') for t in ax.yaxis.get_ticklabels()]
    [t.set_color('red') for t in ax.zaxis.get_ticklines()]
    [t.set_color('red') for t in ax.zaxis.get_ticklabels()]
    ax.spines['bottom'].set_color('red')
    ax.spines['top'].set_color('red')

    plt.show()
    return


def pso():  # inserting the values into the program and making it into one peace
    n, w, c1, c2 = 20, 0.78, 0.18, 0.18  # coefficients: number of particles, inertia weight, cognitive and social coefficients
    start_pos, start_vel = start(n)
    gb_coord, gb_value, pb, pb_value, X, V = first_best(n, start_pos, start_vel)
    gb_coord, gb_value = best(w, c1, c2, gb_coord, gb_value, pb, pb_value, X, V, n)
    return gb_coord, gb_value


def main():  # the main function where PSO is being run
    k = 100  # this coefficient is responsible for the number of iterations of PSO the program runs
    values = []
    coordinates = []
    collection1 = np.array([0, 0])
    collection2 = np.array([0])
    for i in range(k):
        gb_coord, gb_value = pso()
        collection1 = gb_coord + collection1
        collection2 = gb_value + collection2
        values.append(gb_value)
        coordinates.append(gb_coord)
    average_coord = collection1/k
    average_value = collection2/k
    print(f"The approximate coordinates for the global minimum are: {average_coord}")
    print(f"The approximate value of the global minimum is: {average_value}")
    return coordinates, values


# calling the functions
coordinates, values = main()
graph(coordinates, values)


