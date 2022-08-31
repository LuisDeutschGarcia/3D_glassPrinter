from G02 import *
import numpy as np
import plotly.graph_objects as go

g_code = "G01 X0.0 Y0.0 Z0.0" \
         "G01 X9.0" \
         "G03 Y2.0 X11.0 R2.0" \
         "G01 Y11.0" \
         "G03 X9.0 Y13.0 R2.0" \
         "G01 X0.0" \
         "G03 X-2.0 Y11.0 R2.0" \
         "G01 Y2.0" \
         "G03 X0.0 Y0.0 R2.0"

# g_code =  "G01 X0 Y0" \
#           "G01 Z-0.25" \
#           "G02 X0.15 Y0 R0.075" \
#           "G02 X-0.15 Y0 R0.15" \
#           "G02 X0.3 Y0 R0.225" \
#           "G02 X-0.3 Y0 R0.3" \
#           "G02 X0.45 Y0 R0.375" \
#           "G02 X-0.45 Y0 R0.45" \
#           "G02 X0.6 Y0 R0.525" \
#           "G02 X-0.6 Y0 R0.6" \
#           "G02 X0.75 Y0 R0.675" \
#           "G02 X-0.75 Y0 R0.75" \
#           "G02 X0.9 Y0 R0.825" \
#           "G02 X-0.9 Y0 R0.9" \
#           "G02 X1.05 Y0 R0.975" \
#           "G02 X-1.05 Y0 R1.05" \
#           "G02 X1.125 Y0 R1.0875" \
#           "G02 X-1.125 Y0 R1.125" \
#           "G02 X1.125 Y0 R1.125" \
#           "G02 X0.75 Y-0.375 R0.375" \
#           "G01 Z0.1" \
#           "G01 X0 Y0"  \
#           "G01 Z-0.5" \
#           "G02 X0.15 Y0 R0.075" \
#           "G02 X-0.15 Y0 R0.15" \
#           "G02 X0.3 Y0 R0.225" \
#           "G02 X-0.3 Y0 R0.3" \
#           "G02 X0.45 Y0 R0.375" \
#           "G02 X-0.45 Y0 R0.45" \
#           "G02 X0.6 Y0 R0.525" \
#           "G02 X-0.6 Y0 R0.6" \
#           "G02 X0.75 Y0 R0.675"  \
#           "G02 X-0.75 Y0 R0.75" \
#           "G02 X0.9 Y0 R0.825" \
#           "G02 X-0.9 Y0 R0.9" \
#           "G02 X1.05 Y0 R0.975"  \
#           "G02 X-1.05 Y0 R1.05"  \
#           "G02 X1.125 Y0 R1.0875" \
#           "G02 X-1.125 Y0 R1.125" \
#           "G02 X1.125 Y0 R1.125" \
#           "G02 X0.75 Y-0.375 R0.375"  \
#           "G01 Z0.1" \
#           "G01 X0 Y0" \
#           "G01 Z-0.75" \
#           "G02 X0.15 Y0 R0.075"  \
#           "G02 X-0.15 Y0 R0.15" \
#           "G02 X0.3 Y0 R0.225" \
#           "G02 X-0.3 Y0 R0.3" \
#           "G02 X0.45 Y0 R0.375" \
#           "G02 X-0.45 Y0 R0.45" \
#           "G02 X0.6 Y0 R0.525" \
#           "G02 X-0.6 Y0 R0.6" \
#           "G02 X0.75 Y0 R0.675" \
#           "G02 X-0.75 Y0 R0.75" \
#           "G02 X0.9 Y0 R0.825" \
#           "G02 X-0.9 Y0 R0.9" \
#           "G02 X1.05 Y0 R0.975" \
#           "G02 X-1.05 Y0 R1.05" \
#           "G02 X1.125 Y0 R1.0875" \
#           "G02 X-1.125 Y0 R1.125" \
#           "G02 X1.125 Y0 R1.125" \
#           "G02 X0.75 Y-0.375 R0.375" \
#           "G01 Z0.1" \
#           "G01 X0 Y0" \
#           "G01 Z-0.9" \
#           "G02 X0.15 Y0 R0.075" \
#           "G02 X-0.15 Y0 R0.15" \
#           "G02 X0.3 Y0 R0.225" \
#           "G02 X-0.3 Y0 R0.3" \
#           "G02 X0.45 Y0 R0.375" \
#           "G02 X-0.45 Y0 R0.45" \
#           "G02 X0.6 Y0 R0.525" \
#           "G02 X-0.6 Y0 R0.6" \
#           "G02 X0.75 Y0 R0.675" \
#           "G02 X-0.75 Y0 R0.75" \
#           "G02 X0.9 Y0 R0.825" \
#           "G02 X-0.9 Y0 R0.9" \
#           "G02 X1.05 Y0 R0.975" \
#           "G02 X-1.05 Y0 R1.05" \
#           "G02 X1.125 Y0 R1.0875" \
#           "G02 X-1.125 Y0 R1.125" \
#           "G02 X1.125 Y0 R1.125" \
#           "G02 X0.75 Y-0.375 R0.375" \
#           "G01 Z0.1"


arr_gCode = g_code.split('G')
print(arr_gCode)

x = []
y = []
z = []
command = []
radius = []
for element in arr_gCode:
    try:
        if element != '':
            command.append(element.split(' ')[0])
        if 'R' in element:
            radius.append(float(element.split('R')[1]))
        elif 'R' not in element and element != '':
            radius.append(0)
        if "X" in element and "Y" in element and "Z" in element:
            x.append(float(element.split('X')[1].split(' ')[0]))
            y.append(float(element.split('Y')[1].split(' ')[0]))
            z.append(float(element.split('Z')[1].split(' ')[0]))
        elif "X" in element and "Y" in element:
            x.append(float(element.split('X')[1].split(' ')[0]))
            y.append(float(element.split('Y')[1].split(' ')[0]))
            z.append(z[-1])
        elif "X" in element:
            x.append(float(element.split('X')[1].split(' ')[0]))
            y.append(y[-1])
            z.append(z[-1])
        elif "Y" in element:
            x.append(x[-1])
            y.append(float(element.split('Y')[1].split(' ')[0]))
            z.append(z[-1])
        elif "Z" in element:
            x.append(x[-1])
            y.append(y[-1])
            z.append(float(element.split('Z')[1].split(' ')[0]))
    except:
        pass

print(np.array([[cmd, x, y, z, rad] for cmd, x, y, z, rad in zip(command, x, y, z, radius)]))

coordinates = []
rslt = 10
for c in range(len(command)):
    try:
        coordinates.append([x[c], y[c], z[c]])
        if command[c + 1] == "03":
            i, j = arcInterpolation(x[c], x[c + 1], y[c], y[c + 1], radius[c + 1], resolution=rslt, G02=False)
            for x_c, y_c in zip(i, j):
                coordinates.append([x_c, y_c, z[c]])
        elif command[c + 1] == "02":
            i, j = arcInterpolation(x[c], x[c + 1], y[c], y[c + 1], radius[c + 1], resolution=rslt, G02=True)
            for x_c, y_c in zip(i, j):
                coordinates.append([x_c, y_c, z[c]])
    except:
        pass

coordinates = np.array(coordinates)

fig = go.Figure(data=[go.Scatter3d(x=coordinates[:, 0], y=coordinates[:, 1], z=coordinates[:, 2],
                                   marker=dict(size=6, color=coordinates[:, 2], colorscale='electric'),
                                   line=dict(color='darkblue', width=2))])

# fig = go.Figure(data=[go.Scatter3d(x=coordinates[:, 0], y=coordinates[:, 1], z=coordinates[:, 2],
#                                    mode='markers')])

fig.show()

print("Done")
