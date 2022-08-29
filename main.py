import os
import ThermalCamera as TC
import geometries    as gm
import Axis          as ax
import numpy         as np
import pandas        as pd
import Laser
import time

# Declare all the serial ID of the motors
serial_number_x = b'xi-com:\\\\.\\COM5'
serial_number_y = b'xi-com:\\\\.\\COM4'
serial_number_z = b'xi-com:\\\\.\\COM6'
serial_number_a = b'xi-com:\\\\.\\COM7'

# Create COM communication
x = ax.axis(serial_number_x)
y = ax.axis(serial_number_y)
z = ax.axis(serial_number_z)
a = ax.axis(serial_number_a)
ls = Laser.laser()
thermalCamera = TC.ThermalCamera()

# Initialize Axis
x.init()
y.init()
z.init()
a.init()

thermalCamera.init()
ls.init()
ls.enable()
time.sleep(3)

print(f'X Position: {x.axis_getPosition()}')
print(f'Y Position: {y.axis_getPosition()}')
print(f'Z Position: {z.axis_getPosition()}')

# Range of parameters to be used in the Snake test
# variables = [maxPower, minPower, MaxVelocity, minVelocity, number of samples]
variables = [29000, 28000, 500, 250, 8]

maxPower, minPower = variables[0], variables[1]
stepPower = (maxPower - minPower) / variables[4]
cntPower = 0

maxSpeed, minSpeed = variables[2], variables[3]
stepSpeed = (maxSpeed - minSpeed) / variables[4]
cntSpeed = 0

# Snake test parameter
line = 1

power = maxPower
speed = maxSpeed

scale = 1500

coordinates = gm.snake(8) * scale

X, Y, Z = coordinates[:, 0], coordinates[:, 1], coordinates[:, 2]

print(f'Power: {power} [mW]')
print(f'pseudo-gcode:\n {coordinates}')

# Turn on Laser
ls.on(int(power))

# User input to start the sequence of movements
input("Press Enter to continue...")

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

a.axis_movr(-10000, speed=1.44)
path = r'C:\Users\ldeutsc2\Documents\Imager Data'
data = []

for x_coor, y_coor, z_coor in zip(X, Y, Z):
    if (line + 1) % 2 == 0 and line != 1:
        cntPower += stepPower
        cntSpeed += stepSpeed
    ls.on(power - cntPower)
    x.axis_move(int(x_coor.item()), speed=speed - cntSpeed)
    y.axis_move(int(y_coor.item()), speed=speed - cntSpeed)
    z.axis_move(int(z_coor.item()), speed=speed - cntSpeed)
    print(f'X coordinate: {x_coor}. Y coordinate: {y_coor}. Z coordinate: {z_coor}.')
    print(f'Power: {power - cntPower}. Speed: {speed- cntSpeed}.')
    thermalCamera.snapShot()
    x_status = x.axis_getStatus()
    y_status = y.axis_getStatus()
    z_status = z.axis_getStatus()
    temperature = np.max(thermalCamera.get_image(path))
    data.append([x_coor, y_coor, z_coor, power - cntPower, speed - cntSpeed,
                 x_status[0], x_status[1], y_status[0], y_status[1], z_status[0], z_status[1],
                 temperature])
    x.axis_stop(10)
    y.axis_stop(10)
    z.axis_stop(10)

time.sleep(2)
print('Finish process')

x.axis_close()
z.axis_close()
y.axis_close()

a.axis_move(a.axis_getPosition()[0] + 10)
a.axis_close()
#
ls.off()
ls.close()

print("Communication Closed")

columns = ['X', 'Y', 'Z', 'Power', 'Speed',
           'Voltage X', 'Current X', 'Voltage Y', 'Current Y', 'Voltage Z', 'Current Z',
           'Temperature']

save_path = r"C:\Users\ldeutsc2\Desktop\Tests\test.csv"
pd.DataFrame(data, columns=columns).to_csv(save_path)

print("Data Saved")
