from Gcode_Interpreter import *
import ThermalCamera as TC
import geometries    as gm
import Axis          as ax
import numpy         as np
import threading
import logging
import socket
import Laser
import time

# Create Server to send information about the printer
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))

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

# Enable Laser
ls.enable()
time.sleep(3)


def run_Motors(coordinates):
    X, Y, Z = coordinates[:, 0], coordinates[:, 1], coordinates[:, 2]

    for x_coor, y_coor, z_coor in zip(X, Y, Z):
        a.axis_move(-10000, speed=1.0)
        x.axis_move(int(x_coor.item()), speed=speed)
        y.axis_move(int(y_coor.item()), speed=speed)
        z.axis_move(int(z_coor.item()), speed=speed)
        x.axis_stop(10)
        y.axis_stop(10)
        z.axis_stop(10)

    a.axis_move(a.axis_getPosition()[0] + 10)


def run_Laser():
    ls.on(ls.power)
    while True:
        if power != ls.power:
            ls.on(ls.power)
        time.sleep(0.5)


def get_Info():
    while True:
        tm = time.time()
        # thermalCamera.snapShot()
        # temperature = np.max(thermalCamera.get_image())
        temperature = None
        x_status = x.axis_getStatus()
        y_status = y.axis_getStatus()
        z_status = z.axis_getStatus()
        message = str([x.position, y.position, z.position, ls.power, speed,
                       x_status[0], x_status[1], y_status[0], y_status[1], z_status[0], z_status[1],
                       temperature])
        server.sendto(message.encode(), ("localhost", 8999))
        # print('Information sent!!')
        # print(f"Execution time: {time.time() - tm}")
        time.sleep(0.2)


path = r'C:\Users\ldeutsc2\Desktop\Gcodes\Cube.txt'
scale = 1000
coordinates = gCode_interpreter(path, verbose=False) * scale
# coordinates = gm.downSampling(gCode_interpreter(path, verbose=False), 0.1) * scale
# coordinates = gm.specific_spiral() * scale

print(f"Current Laser Power: {ls.power}")
ls.power = int(input("Input Laser Power"))
power = ls.power
print(f"Laser Power changed to {ls.power} mW")
speed = 325

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    # Initialization of the Motors Thread
    motorThread = threading.Thread(target=run_Motors, args=(coordinates,))

    # Initialization of the Laser Thread
    laserThread = threading.Thread(target=run_Laser, args=())
    laserThread.daemon = True

    # Initialization of the Information Thread
    infoThread = threading.Thread(target=get_Info, args=())
    infoThread.daemon = True

    # Start the execution of the threads
    logging.info("Main     : create and start motor thread")
    laserThread.start()

    input("Press Enter to continue...")
    logging.info("Main     : create and start motor thread")
    motorThread.start()

    logging.info("Main     : create and start motor thread")
    infoThread.start()

    # Wait for the motor thread to finish then all threads will be killed.
    motorThread.join()

    # Show to the user that the motors have stopped
    logging.info("Main     : motor thread has finished")

    x.axis_close()
    z.axis_close()
    y.axis_close()
    a.axis_close()
    ls.off()
    ls.close()

    logging.info("Main     : Communication Closed")
    print('Finish')
