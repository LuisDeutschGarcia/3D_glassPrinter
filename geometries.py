import numpy as np
import plotly.express as px
import plotly.graph_objects as go


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

def specific_spiral(plot=False):
    radius = 6
    circle = np.array([[radius * np.cos(angle), radius * np.sin(angle), 0] for angle in np.arange(0, 2 * np.pi, 0.05)])
    x, y, z = list(circle[:,0]), list(circle[:,1]), list(circle[:,2])

    sample = 400
    z_s = list(np.linspace(0, 10, sample * 2) * -2)
    r_s = (np.linspace(0, 10, sample)) + radius
    theta = np.linspace(0,8 * np.pi, sample)
    cnt = 0
    for i in range(len(theta)):
        x.append(r_s[i] * np.cos(theta[i]))
        y.append(r_s[i] * np.sin(theta[i]))
        z.append(z_s[i])
        cnt += 1

    r_s = (np.linspace(10, 0, sample)) + radius

    for i in range(len(theta)):
        x.append(r_s[i] * np.cos(theta[i]))
        y.append(r_s[i] * np.sin(theta[i]))
        z.append(z_s[cnt])
        cnt += 1

    sprl = np.array([[X,Y,Z] for X,Y,Z in zip(x,y,z)])

    if plot:
        fig = px.scatter_3d(x=x, y=y, z=z)
        fig.show()

    return sprl

def lens(plot=False):
    radius = 2
    circle = np.array([[radius * np.cos(angle), radius * np.sin(angle), 0] for angle in np.arange(0, 2 * np.pi, 0.3)])
    x, y, z = list(circle[:, 0]), list(circle[:, 1]), list(circle[:, 2])

    sample = 200
    z_s = np.linspace(0, 8, sample) * - 1
    r_s = (np.linspace(0, 5, sample)) + radius
    theta = np.linspace(0, 8 * np.pi, sample)
    cnt = 0
    vl = 0
    for i in range(len(theta)):
        x.append(r_s[i] * np.cos(theta[i] - vl))
        y.append(r_s[i] * np.sin(theta[i] - vl))
        z.append(z_s[i])
        cnt += 1

    x = np.array(x)
    y = np.array(y)

    x = x - x[0]
    y = y - y[0]

    sprl = np.array([[X, Y, Z] for X, Y, Z in zip(x, y, z)])


    if plot:
        fig = px.scatter_3d(x=x, y=y, z=z)
        fig.show()

    return sprl

def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x))

def lens2(plot=False):

    theta = np.radians(np.linspace(0, 360 * 5, 1000))
    r = theta
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    x = normalize(x)
    y = normalize(y)

    x_new = list(x)
    y_new = list(y)

    for x_1, y_1 in zip(x[::-1], y[::-1]):
        x_new.append(x_1)
        y_new.append(y_1)

    z = np.zeros(len(x_new))

    x = x_new - x_new[0]
    y = y_new - y_new[0]

    sprl = np.array([[X, Y, Z] for X, Y, Z in zip(x, y, z)])

    if plot:
        fig = px.scatter_3d(x=x, y=y, z=z)
        fig.show()

    return sprl

def spiral(plot=False):
    # circle = np.array([[3 * np.cos(angle), 3 * np.sin(angle),0] for angle in np.arange(0, 2 * np.pi,0.05)])

    sample = 250
    theta = np.linspace(0, 20 * np.pi, sample)
    z_s = np.linspace(0, 20, sample) * 2
    r_s = (z_s / 8)
    x_s = r_s * np.sin(theta) * 2
    y_s = r_s * np.cos(theta) * 2

    spiral = np.array([[x, y, z] for x, y, z in zip(x_s, y_s, z_s)])[:100, :]

    if plot:
        fig = px.scatter_3d(x=x_s, y=y_s, z=z_s)
        fig.show()

    return spiral


def cilindrical_spiral(plot=False):
    sample = 250
    theta = np.linspace(0, 15 * np.pi, sample)
    z_s = np.linspace(0, 40, sample) * -1
    x_s = 5 * np.sin(theta) * 1.5
    y_s = 5 * np.cos(theta) * 1.5
    if plot:
        fig = px.scatter_3d(x=x_s, y=y_s, z=z_s)
        fig.show()

    return np.array([[x, y, z] for x, y, z in zip(x_s, y_s, z_s)])[:100, :]


def cube(height=1, plot=False):
    coordinates = np.array([[8, 0, 0],
                            [8, -8, 0],
                            [0, -8, 0],
                            [0, 0, 0]])

    X, Y, Z = coordinates[:, 0], coordinates[:, 1], coordinates[:, 2]

    if plot:
        fig = px.scatter_3d(x=X, y=Y, z=Z)
        fig.show()

    return np.array([[x, y, z + i * height] for i in range(10) for x, y, z in zip(X, Y, Z)])



def downSampling(coordinates, rate = 0.7):

    downsample = int(rate * len(coordinates))
    rows = np.sort(np.ndarray.flatten(np.random.randint(0, len(coordinates), size=(downsample, 1))))
    coordinates = coordinates[rows]
    new = [[0, 0, 0]]
    for element in coordinates:
        new.append(element)

    return np.array(new)
