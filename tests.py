from Gcode_Interpreter import *
from skimage.measure import block_reduce
import matplotlib.pyplot as plt
import plotly.express as px
import geometries as gm
import ThermalCamera as TC
import numpy as np
import Axis as ax
import Laser
import time
import os
import csv
import cv2

def plot(X,Y,Z):

    fig = go.Figure(data=[go.Scatter3d(x=X, y=Y, z=Z,
                                       marker=dict(size=6, color="darkblue", colorscale='electric'),
                                       line=dict(color='slategray', width=2))])
    fig.show()

# serial_number_x = b'xi-com:\\\\.\\COM5'
# x = ax.axis(serial_number_x)
# x.init()
#
# x.axis_move(position=-9000, speed=500)
# print( x.axis_getStatus() )
# print( x.axis_getStatus() )
# print( x.axis_getStatus() )
#
# x.axis_close()


# Test Power and Velocity
# for x_coor, y_coor, z_coor in zip(X, Y, Z):
#     if (line + 1) % 2 == 0 and line != 1:
#         cntPower += stepPower
#         cntSpeed += stepSpeed
#     ls.on(power - cntPower)
#     x.axis_move(int(x_coor.item()), speed=speed - cntSpeed)
#     y.axis_move(int(y_coor.item()), speed=speed - cntSpeed)
#     z.axis_move(int(z_coor.item()), speed=speed - cntSpeed)
#     print(f'X coordinate: {x_coor}. Y coordinate: {y_coor}. Z coordinate: {z_coor}.')
#     print(f'Power: {power - cntPower}. Speed: {speed - cntSpeed}.')
#     x.axis_stop(10)
#     y.axis_stop(10)
#     z.axis_stop(10)
#     line += 1
#
# time_start = time.time()
# path = r'C:\Users\ldeutsc2\Desktop\Gcodes\TecLogo_3.txt'
# coordinates = gCode_interpreter(None, path = path, verbose=False) * 1
# coordinates = np.rot90(coordinates)
# coordinates = gm.downSampling(coordinates, 0.1)
# coordinates = gm.lens2()
#
# # print(f'Finished in: {time.time() - time_start}')
#
#
# coordinates = gm.lens() * 5
#
# fig = go.Figure(data=[go.Scatter3d(x=coordinates[:, 0], y=coordinates[:, 1], z=coordinates[:, 2],
#                                            marker=dict(size=6, color="darkblue", colorscale='electric'),
#                                            line=dict(color='slategray', width=2))])
# fig.show()
#
# for x, y, z in coordinates:
#     print(f'G01 X{x} Y{y} Z{z}')



# text = (    'G01 X8.0\n'
#             'G01 Y8.0\n'
#             'G01 X0.0\n'
#             'G01 Y1.0\n'
#             'G01 X7.0\n'
#             'G01 Y7.0\n'
#             'G01 X1.0\n'
#             'G01 Y2.0\n'
#             'G01 X6.0\n'
#             'G01 Y6.0\n'
#             'G01 X2.0\n'
#             'G01 Y3.0\n'
#             'G01 X5.0\n'
#             'G01 Y5.0\n'
#             'G01 X3.0\n'
#             'G01 Y4.0\n'
#             'G01 X4.0\n').split('\n')
#
# cnt = 1
# print('G01 X0.0 Y0.0 Z0.0')
# for j in range(30):
#       print(f'G01 Z{float(-1 * j)}')
#       for i, element in enumerate(text):
#             if cnt % 2 == 0 and int(i) != 0:
#                   print(text[i * -1])
#             elif cnt % 2 != 0:
#                   print(element)
#       if cnt % 2 == 0:
#             print('G01 X8.0\n'
#                   'G01 Y0.0\n'
#                   'G01 X0.0\n')
#       cnt +=1
#
# print('-----------------------------------------------------------------')
#
# coordinates = gm.specific_spiral(False)

# for element in coordinates:
#     print(f'G01 X{round(element[0], 4)} Y{round(element[1], 4)} Z{round(element[2], 4)}')

# speed_m = 4.5
# speed = int((speed_m * 100) / (np.pi * 13.54))
# uSpeed = int(((speed_m * 100) / (np.pi * 13.54) - speed) * 256)
# print(f'Speed {speed}, uSpeed {uSpeed}')

# x = ax.axis(b'xi-com:\\\\.\\COM5')
# y = ax.axis(b'xi-com:\\\\.\\COM4')
# z = ax.axis(b'xi-com:\\\\.\\COM6')
#
# x.init()
# y.init()
# z.init()
#
# g_code = 'G01 X0.0 Y0.0 Z0.0 \n' \
#          'G01 X15.0  \n' \
#          'G01 X10.0  \n' \
#          'G01 X-5.0  \n' \
#          'G01 X0.0  \n'
#
#
# coordinates = gCode_interpreter(g_code)[:,:3] * 1000
# speed = 5000
#
# X, Y, Z = coordinates[:, 0], coordinates[:, 1], coordinates[:, 2]
#
# time_start = time.time()
# cnt = 0
# for x_coor, y_coor, z_coor in zip(X, Y, Z):
#     # print(f'Speed {speed}, acceleration {acc}, deacceleration {deccel}, cnt {cnt}')
#     print(f'X: {x_coor}, Y: {y_coor}, Z: {z_coor}')
#     x.axis_move(int(x_coor.item()), speed=speed)
#     y.axis_move(int(y_coor.item()), speed=speed)
#     z.axis_move(int(z_coor.item()), speed=speed)
#     cnt += 0
#
#
# print(f'Finish in: {time.time() - time_start}')
#
# x.axis_close()
# z.axis_close()
# y.axis_close()

G_code = "G01 X21.42 Y16.98 Z0.0\n" \
         "G01 X20.46 Y14.44\n" \
         "G01 X18.06 Y14.44\n" \
         "G01 X19.98 Y12.98\n" \
         "G01 X18.88 Y10.16\n" \
         "G01 X21.43 Y11.90\n" \
         "G01 X23.78 Y10.12\n" \
         "G01 X22.84 Y12.865\n" \
         "G01 X25.06 Y14.44\n" \
         "G01 X22.31 Y14.4\n" \
         "G01 X21.42 Y16.98\n"

coordinates = gCode_interpreter(G_code, verbose=False)[:,:3]

scale = 0.3

X = (coordinates[:,0] - coordinates[0,0]) * scale * 10
Y = (coordinates[:,1] - coordinates[0,1]) * scale * 10
Z = coordinates[:,2]

plot(X,Y,Z)

for x,y in zip(X,Y):
    print(f'G01 X{x} Y{y}')
