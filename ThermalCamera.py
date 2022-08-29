import numpy as np
import serial
import os
import time
import csv


class ThermalCamera:

    def __init__(self):
        self.port = "COM9"
        self.baudrate = 115200
        self.bytesize = 8
        self.stopbits = serial.STOPBITS_ONE
        self.en = 0
        self.s = serial.Serial()

    def init(self, port=None, baudrate=None, bytesize=None, stopbits=None):
        self.s = serial.Serial(port=port or self.port, baudrate=baudrate or self.baudrate,
                               bytesize=bytesize or self.bytesize, stopbits=stopbits or self.stopbits)
        print('Thermal Camera connected')

    def snapShot(self):
        try:
            arr = bytes("!Snapshot\r\n", 'utf-8')
            self.s.write(arr)
        except Exception as e:
            print(f"Error reading TIM40. The error '{e}' occurred")

    def get_image(self, path):
        time.sleep(0.5)
        csv_file = os.listdir(path)
        try:
            with open(os.path.join(path, csv_file[0])) as file:
                reader = csv.reader(file)
                image = [row for row in reader]
                image = np.asfarray([row[0].split(';')[:-1] for row in image])
            if os.path.exists(os.path.join(path, csv_file[0])):
                os.remove(os.path.join(path, csv_file[0]))
            return image
        except:
            print('Error in thermal image')
            return np.zeros((100, 100))

    def get_imageSize(self, lst=False):
        arr = bytes("!ImgTemp\r\n", 'utf-8')
        self.s.write(arr)
        size = str(self.s.read(19))
        if lst:
            return size.replace("b'!ImgTemp(", '').replace(")", "").split(',')
        else:
            return size

    def get_Image(self, width, height, x, y):
        x0, x1 = x - width / 2, x + width / 2
        y0, y1 = y - height / 2, y + height / 2
        arr = bytes(f"?Img({x0},{y0},{x1},{y1})\r\n", 'utf-8')
        self.s.write(arr)
        return str(self.s.read(20))
