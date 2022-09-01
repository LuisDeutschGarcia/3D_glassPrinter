import re
from G02 import *
import numpy as np
import plotly.graph_objects as go

path = r'C:\Users\luisd\Downloads\TecLogo_0004.ngc'

g_code = np.array(open(path, 'r').read().split('\n'))

for element in g_code:
    print(element)

def get_point(char,s):
    res = re.split('([-+]?\d+\.\d+)|([-+]?\d+)', s.strip())
    res_f = [r.strip() for r in res if r is not None and r.strip() != '']
    return float(res_f[res_f.index(char)+1])

command, X, Y, Z, I, J = [], [], [], [], [], []

for element in g_code:
    try:
        if "G01" in element or "G02" in element or "G03" in element:
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
                X.append(Y[-1])
                Z.append(Z[-1])
            elif "Z" in element:
                Z.append(get_point('Z', element))
                X.append(Y[-1])
                Y.append(Z[-1])
    except:
        print("Exception",element)

coordinates = np.array([[x,y,z] for x,y,z in zip(X,Y,Z)])
# print(coordinates)

fig = go.Figure(data=[go.Scatter3d(x=coordinates[:, 0], y=coordinates[:, 1], z=coordinates[:, 2],
                                   marker=dict(size=6, color="darkblue", colorscale='electric'),
                                   line=dict(color='slategray', width=2))])

# fig = go.Figure(data=[go.Scatter3d(x=coordinates[:, 0], y=coordinates[:, 1], z=coordinates[:, 2],
#                                    mode='markers')])

fig.show()

# for element in g_code:
#     try:
#         if 'G' in element:
#             # print("Inside G")
#             command.append(get_point('G',element))
#             if 'J' in element and 'I' in element:
#                 I.append(get_point('I',element))
#                 J.append(get_point('J', element))
#             elif not('J' in element and 'I' in element):
#                 I.append(0)
#                 J.append(0)
#             if "X" in element and "Y" in element and "Z" in element:
#                 X.append(get_point('X', element))
#                 Y.append(get_point('Y', element))
#                 Z.append(get_point('Z', element))
#             if "X" in element and "Y" in element:
#                 X.append(get_point('X', element))
#                 Y.append(get_point('Y', element))
#                 Z.append(Z[-1])
#             if "X" in element:
#                 X.append(get_point('X', element))
#                 Y.append(Y[-1])
#                 Z.append(Z[-1])
#             if "Y" in element:
#                 Y.append(get_point('Y', element))
#                 X.append(Y[-1])
#                 Z.append(Z[-1])
#             if "Z" in element:
#                 Z.append(get_point('Z', element))
#                 X.append(Y[-1])
#                 Y.append(Z[-1])
#     except:
#         pass

# print(X)
#
# coordinates = np.array( [[cmd, x, y, z, i, j] for cmd, x, y, z, i, j in zip(command, X, Y, Z, I, J )])
# print(coordinates)