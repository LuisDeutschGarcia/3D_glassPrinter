import serial
import time


class laser:

    def __init__(self):
        self.port = "COM3"
        self.baudrate = 9600
        self.bytesize = 8
        self.stopbits = serial.STOPBITS_ONE
        self.en = 0
        self.s = serial.Serial()

    def init(self, port=None, baudrate=None, bytesize=None, stopbits=None):
        self.s = serial.Serial(port=port or self.port, baudrate=baudrate or self.baudrate,
                               bytesize=bytesize or self.bytesize, stopbits=stopbits or self.stopbits)
        print('Laser connected')

    def enable(self):
        try:
            arr = "01o1;\r"
            arr = [ord(c) for c in arr]
            self.s.write(arr)
            self.en = 1
        except Exception as e:
            print(f"Error Enabling laser. The error '{e}' occurred")

    def on(self, value):
        if self.en == 0:
            print("The laser is not enabled")
        else:
            try:
                arr = "01o2;\r"
                arr = [ord(c) for c in arr]
                self.s.write(arr)
                arr = f"01p0;{value}\r"
                arr = [ord(c) for c in arr]
                self.s.write(arr)
            except Exception as e:
                print(f"Error turning on the laser. The error '{e}' occurred")

    def off(self):
        try:
            print("Turning off Laser")
            arr = "01o0;\r"
            arr = [ord(c) for c in arr]
            self.s.write(arr)
            self.en = 0
        except Exception as e:
            print(f"Error Turning off the laser. The error '{e}' occurred")

    def close(self):
        self.s.close()
