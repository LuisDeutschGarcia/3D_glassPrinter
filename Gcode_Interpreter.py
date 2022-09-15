import re
import numpy as np
import plotly.graph_objects as go

def get_point(char,s):
    res = re.split('([-+]?\d+\.\d+)|([-+]?\d+)', s.strip())
    res_f = [r.strip() for r in res if r is not None and r.strip() != '']
    return float(res_f[res_f.index(char)+1])


def arcInterpolation_3(x1, x2, y1, y2, R, I, J, resolution = 50, G02=True):
    Chord = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    if R == 0:
        Xc, Yc = x1 + I, y1 + J
        R = np.sqrt((x1 - Xc) ** 2 + (y1 - Yc) ** 2)
        IJ = True
    else:
        Xchord = (x2 + x1) / 2
        Ychord = (y2 + y1) / 2
        slope = np.sqrt(R ** 2 - (Chord / 2) ** 2)
        Run = (np.abs(x1 - x2) / 2 * slope) / (Chord / 2)
        Rise = (np.abs(y2 - y1) / 2 * Run) / (np.abs(x1 - x2) / 2)
        IJ = False

    alpha = np.arccos(1 - (Chord ** 2) / (2 * (R ** 2)))
    beta = alpha / resolution

    if not (IJ):
        if (G02 == True and (x1 < x2 and y1 < y2)) or (G02 == False and (x1 > x2 and y1 > y2)):
            Xc = Xchord + Rise
            Yc = Ychord - Run
        elif (G02 == True and (x1 < x2 and y1 > y2)) or (G02 == False and (x1 > x2 and y1 < y2)):
            Xc = Xchord - Rise
            Yc = Ychord - Run
        elif (G02 == True and (x1 > x2 and y1 > y2)) or (G02 == False and (x1 < x2 and y1 < y2)):
            Xc = Xchord - Rise
            Yc = Ychord + Run
        elif (G02 == True and (x1 > x2 and y1 < y2)) or (G02 == False and (x1 < x2 and y1 > y2)):
            Xc = Xchord + Rise
            Yc = Ychord + Run
        elif (G02 == True and (x1 == x2 and y1 < y2)) or (G02 == False and (x1 == x2 and y1 > y2)):
            Xc = Xchord + slope
            Yc = Ychord
        elif (G02 == True and (x1 == x2 and y1 > y2)) or (G02 == False and (x1 == x2 and y1 < y2)):
            Xc = Xchord - slope
            Yc = Ychord
        elif (G02 == True and (x1 < x2 and y1 == y2)) or (G02 == False and (x1 > x2 and y1 == y2)):
            Xc = Xchord
            Yc = Ychord - slope
        elif (G02 == True and (x1 > x2 and y1 == y2)) or (G02 == False and (x1 < x2 and y1 == y2)):
            Xc = Xchord
            Yc = Ychord + slope

    Xdiff = x1 - Xc
    Ydiff = y1 - Yc

    w = np.pi - np.arcsin(Ydiff / R) if Xdiff >= 0 else np.arcsin(Ydiff / R)

    if G02:
        arc = np.array([[Xc - R * np.cos(w + (beta * n)),
                         Yc + R * np.sin(w + (beta * n))] for n in range(0, resolution + 1)])
    else:
        arc = np.array([[Xc - R * np.cos(w - (beta * n)),
                         Yc + R * np.sin(w - (beta * n))] for n in range(0, resolution + 1)])

    return arc[:, 0], arc[:, 1]

def gCode_interpreter(g_code, path = None, verbose=False):

    command, X, Y, Z, R, I, J, P, F, S = [], [], [], [], [], [], [], [], [], []

    if path != None:
        g_code = np.array(open(path, 'r').read().split('\n'))
    else:
        g_code = np.array(g_code.split('\n'))

    for element in g_code:
        try:
            if "G01" in element or "G02" in element or "G03" in element:
                command.append(element.split(' ')[0])
                if 'R' in element:
                    R.append(get_point("R", element))
                elif 'R' not in element and element != '':
                    R.append(0)
                if 'I' in element:
                    I.append(get_point("I", element))
                elif 'I' not in element and element != '':
                    I.append(0)
                if 'J' in element:
                    J.append(get_point("J", element))
                elif 'J' not in element and element != '':
                    J.append(0)
                if 'P' in element:
                    P.append(get_point("P", element))
                elif 'P' not in element and element != '':
                    try:
                        P.append(P[-1])
                    except:
                        P.append(0)
                if 'F' in element:
                    F.append(get_point("F", element))
                elif 'F' not in element and element != '':
                    try:
                        F.append(F[-1])
                    except:
                        F.append(0)
                if 'S' in element:
                    S.append(get_point("S", element))
                elif 'S' not in element and element != '':
                    try:
                        S.append(S[-1])
                    except:
                        S.append(0)
                if "X" in element and "Y" in element and "Z" in element:
                    X.append(get_point("X", element))
                    Y.append(get_point("Y", element))
                    Z.append(get_point("Z", element))
                elif "X" in element and "Y" in element:
                    X.append(get_point('X', element))
                    Y.append(get_point('Y', element))
                    Z.append(Z[-1])
                elif "X" in element:
                    X.append(get_point('X', element))
                    Y.append(Y[-1])
                    Z.append(Z[-1])
                elif "Y" in element:
                    Y.append(get_point('Y', element))
                    X.append(X[-1])
                    Z.append(Z[-1])
                elif "Z" in element:
                    Z.append(get_point('Z', element))
                    X.append(X[-1])
                    Y.append(Y[-1])
        except:
            print(f"Exeception in: {element}")

    # print(command, X, Y, Z, I, J, R, S, P, F)

    rslt = 60
    coordinates = []
    for c in range(len(command)):
        try:
            coordinates.append([X[c], Y[c], Z[c], P[c], F[c], S[c]])
            if command[c + 1] == "G03":
                i, j = arcInterpolation_3(X[c], X[c + 1], Y[c], Y[c + 1], R[c + 1], I[c + 1], J[c + 1], resolution=rslt,
                                          G02=False)
                for x_c, y_c in zip(i, j):
                    coordinates.append([x_c, y_c, Z[c], P[c], F[c], S[c]])
            if command[c + 1] == "G02":
                i, j = arcInterpolation_3(X[c], X[c + 1], Y[c], Y[c + 1], R[c + 1], I[c + 1], J[c + 1], resolution=rslt,
                                          G02=True)
                for x_c, y_c in zip(i, j):
                    # print(P[c], F[c], S[c])
                    coordinates.append([x_c, y_c, Z[c], P[c], F[c], S[c]])
        except:
            pass

    coordinates = np.array(coordinates)
    coordinates = coordinates[~np.isnan(coordinates).any(axis=1),:]


    if verbose:
        fig = go.Figure(data=[go.Scatter3d(x=coordinates[:, 0], y=coordinates[:, 1], z=coordinates[:, 2],
                                           marker=dict(size=6, color="darkblue", colorscale='electric'),
                                           line=dict(color='slategray', width=2))])
        fig.show()

    return coordinates
