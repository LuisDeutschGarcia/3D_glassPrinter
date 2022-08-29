import numpy as np
import plotly.express as px


def snake(no_lines=8, plot=False):
    x_s = [0, 8]
    y_s = [0, 0]
    for i in range(no_lines * 2):
        if x_s[-1] == x_s[-2]:
            if x_s[-1] == 0:
                x_s.append(8)
            else:
                x_s.append(0)
        else:
            x_s.append(x_s[-1])

        for i in range(no_lines * 2):
            if y_s[-1] == y_s[-2]:
                y_s.append(y_s[-1] - 3)
            else:
                y_s.append(y_s[-1])

    if plot:
        fig = px.scatter_3d(x=x_s, y=y_s, z=[0] * len(x_s))
        fig.show()

    return np.array([[x, y, z] for x, y, z in zip(x_s, y_s, [0] * no_lines * 2)])


def spiral(plot=False):
    theta = np.linspace(0, 4 * np.pi, 75)
    z_s = np.linspace(0, 1, 75)
    r_s = (z_s ** 2 + 1) / 2
    x_s = r_s * np.sin(theta)
    y_s = r_s * np.cos(theta)

    if plot:
        fig = px.scatter_3d(x=x_s, y=y_s, z=z_s)
        fig.show()

    return np.array([[x, y, z] for x, y, z in zip(x_s, y_s, z_s)])


def cube(height = 1, plot=False):
    coordinates = np.array([[8, 0, 0],
                            [8, -8, 0],
                            [0, -8, 0],
                            [0, 0, 0]])

    X, Y, Z = coordinates[:, 0], coordinates[:, 1], coordinates[:, 2]

    if plot:
        fig = px.scatter_3d(x=X, y=Y, z=Z)
        fig.show()

    return np.array([[x, y, z + i * height] for i in range(10) for x, y, z in zip(X, Y, Z)])


def tecLogo():
    coordinates = np.array([[0.56, -0.96, 0.],
                            [0.98, -1.37, 0.],
                            [1.68, -1.98, 0.],
                            [2.04, -2.28, 0.],
                            [2.96, -2.77, 0.],
                            [3.56, -2.94, 0.],
                            [4., -3., 0.],
                            [4., -5., 0.],
                            [6., -5., 0.],
                            [6., -3., 0.],
                            [6.48, -2.92, 0.],
                            [6.98, -2.74, 0.],
                            [7.74, -2.36, 0.],
                            [8.26, -2.02, 0.],
                            [9., -1.38, 0.],
                            [9.44, -1., 0.],
                            [10., 0., 0.],
                            [0.52, 3.06, 0.],
                            [4.25, 8.37, 0.],
                            [1.46, 2.03, 0.],
                            [6.59, 8.73, 0.],
                            [3.04, 0.72, 0.],
                            [7.36, 6.75, 0.],
                            [5.56, 0.72, 0.],
                            [9.65, 7.16, 0.],
                            [7.72, 0.63, 0.],
                            [9.7, 3.87, 0.]])

    return coordinates
