from PIL import ImageTk
from PIL import Image as image
from tkinter import filedialog
from Gcode_Interpreter import *

import plotly.graph_objects as go
import ThermalCamera as TC
import tkinter as tk
import geometries as gm
import Axis as ax
import threading
import logging
import socket
import Laser
import time


def load_image(path, scale):
    im = image.open(path)
    im = im.resize((round(im.size[0] * scale), round(im.size[1] * scale)))
    return ImageTk.PhotoImage(im)


class ToggleButton:
    def __init__(self, parent, pos_X=0, pos_Y=0, width=15, height=0.5):
        self.toggleButton = tk.Button(parent, text="OFF", height=height, width=width, command=self.simpleToggle)
        self.toggleButton.place(x=pos_X, y=pos_Y)

        self.status = self.toggleButton.config('text')[-1]

    def simpleToggle(self):
        if self.toggleButton.config('text')[-1] == 'ON':
            self.toggleButton.config(text='OFF')
            self.status = self.toggleButton.config('text')[-1]
        else:
            self.toggleButton.config(text='ON')
            self.status = self.toggleButton.config('text')[-1]


class App:
    def __init__(self, parent):
        parent.title("3D Glas Printer")
        parent.geometry("1000x650")

        self.img_Logo = load_image(r"Images/NotreDameLogo.png", 0.07)
        self.power = 0
        self.firstRun = 0
        self.runMotors = False
        self.coordinates = None
        self.path = None
        self.scale = 1000
        self.speed = float(325)
        self.feed_rate = float(1)

        # Declare all the serial motor IDs
        self.x = ax.axis(b'xi-com:\\\\.\\COM5')
        self.y = ax.axis(b'xi-com:\\\\.\\COM4')
        self.z = ax.axis(b'xi-com:\\\\.\\COM6')
        self.a = ax.axis(b'xi-com:\\\\.\\COM7')

        # Laser
        self.ls = Laser.laser()

        # Thermal Camera
        self.thermalCamera = TC.ThermalCamera()

        # Create Server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(("localhost", 9999))

        self.init_device()
        self.widgets(parent)
        self.motorsThread = threading.Thread(target=self.motorRun)
        self.laserThread = threading.Thread(target=self.activateLaser).start()

    def init_device(self):

        # Create COM communication
        self.thermalCamera = TC.ThermalCamera()

        self.x.init()
        self.y.init()
        self.z.init()
        self.a.init()
        self.ls.init()

        time.sleep(2)
        print("Device communication successfully")

    def widgets(self, app):

        # Toggles
        self.toggle_Laser = ToggleButton(app, 50, 135, 7, 1)

        # Text Box
        self.txtBox_Power = tk.Text(app, height=1, width=6)
        self.txtBox_Gcode = tk.Text(app, height=20, width=60)
        self.txtBox_FeedRate = tk.Text(app, height=1, width=6)
        self.txtBox_SpeedAxis = tk.Text(app, height=1, width=6)

        self.txtBox_Gcode.place(x=50, y=250)
        self.txtBox_Power.place(x=120, y=135)
        self.txtBox_FeedRate.place(x=180, y=135)
        self.txtBox_SpeedAxis.place(x=240, y=135)

        self.txtBox_SpeedAxis.insert(tk.END, str(self.speed))
        self.txtBox_FeedRate.insert(tk.END, str(self.feed_rate))
        self.txtBox_Power.insert(tk.END, str(0.0))

        # Labels
        self.label_title = tk.Label(app, text="3D GLASS PRINTER", font=('CopperplateGothicLight 20'))
        self.label_image = tk.Label(app, image=self.img_Logo)
        self.label_importGcode = tk.Label(app, text="Import G Code:", font=('Arial 12'))

        self.label_title.place(x=380, y=30)
        self.label_image.place(x=900, y=10)
        self.label_importGcode.place(x=50, y=100)

        # Buttons
        self.button_importGCODE = tk.Button(app, text='Open', command=self.setTextInput, width=10)
        self.button_start = tk.Button(app, text='Start printing', command=self.startPrinting, height=3, width=18)
        self.button_stop = tk.Button(app, text='Stop process', command=self.stopProcess, height=3, width=18)
        self.button_saveGcode = tk.Button(app, text='Save G_Code', command=self.saveGCODE, width=15)
        self.button_visualize = tk.Button(app, text='Visualize G Code', command=self.visualization, width=15)
        self.button_loadGcode = tk.Button(app, text='Load G-code', command=self.loadGcode, width=15)

        self.button_importGCODE.place(x=170, y=100)
        self.button_start.place(x=50, y=180)
        self.button_stop.place(x=250, y=180)
        self.button_saveGcode.place(x=50, y=600)
        self.button_visualize.place(x=200, y=600)
        self.button_loadGcode.place(x=350, y=600)

    def setTextInput(self):
        self.path = filedialog.askopenfilename()
        g_code = open(self.path, 'r').read()
        self.txtBox_Gcode.delete(1.0, "end")
        self.txtBox_Gcode.insert(1.0, g_code)
        self.coordinates = gCode_interpreter(g_code, verbose=False) * self.scale
        return None

    def loadGcode(self):
        g_code = self.txtBox_Gcode.get("1.0", "end-1c")
        self.coordinates = gCode_interpreter(g_code, verbose=False) * self.scale
        self.coordinates = gm.downSampling(self.coordinates, 0.1)
        fig = go.Figure(data=[go.Scatter3d(x=self.coordinates[:, 0], y=self.coordinates[:, 1],
                                           z=self.coordinates[:, 2], marker=dict(size=6,
                                           color="darkblue", colorscale='electric'),
                                           line=dict(color='slategray', width=2))])
        fig.show()
        print("G Code loaded")

    def startPrinting(self):
        print("Starting Printer")
        if self.firstRun == 0 and self.coordinates is not None:
            self.runMotors = True
            self.firstRun += 1
            self.motorsThread.start()
        elif self.coordinates is not None and self.firstRun > 0:
            print(f"Restarting printing process")
            self.runMotors = True
            self.firstRun += 1
        else:
            print("There are no G Code in the system")

    def motorRun(self):
        while True:
            if self.coordinates is not None:
                X, Y, Z = self.coordinates[:, 0], self.coordinates[:, 1], self.coordinates[:, 2]
                cnt = 0
            while self.runMotors:
                print(f'X: {X[cnt]}, Y: {Y[cnt]}, Z: {Z[cnt]}')
                self.a.axis_move(-10000, speed=self.feed_rate)
                self.x.axis_move(int(X[cnt].item()), speed=self.speed)
                self.y.axis_move(int(Y[cnt].item()), speed=self.speed)
                self.z.axis_move(int(Z[cnt].item()), speed=self.speed)
                self.x.axis_stop(10)
                self.y.axis_stop(10)
                self.z.axis_stop(10)

                if cnt >= len(X) - 1:
                    self.runMotors = False
                    self.coordinates = None
                    cnt = 0
                cnt += 1

            if cnt <= len(X):
                # self.coordinates = np.array([[x, y, z] for x, y, z in zip(X[cnt:], Y[cnt:], Z[cnt:])])
                X, Y, Z = X[cnt:], Y[cnt:], Z[cnt:]

    def activateLaser(self):
        while True:
            if self.toggle_Laser.status == 'ON':
                self.ls.enable()
                print('Enable')
                time.sleep(3)
                try:
                    while self.toggle_Laser.status == 'ON':
                        power_Box = int(self.txtBox_Power.get("1.0", "end-1c"))
                        feed_rate = float(self.txtBox_FeedRate.get("1.0", "end-1c"))
                        speed = float(self.txtBox_SpeedAxis.get("1.0", "end-1c"))
                        if self.power != power_Box:
                            self.ls.on(power_Box)
                            self.power = power_Box
                            print(self.power)
                        if self.feed_rate != feed_rate:
                            self.feed_rate = feed_rate
                            print(f'Feed Rate = {self.feed_rate}')
                        if self.speed != speed:
                            self.speed = speed
                            print(f'Speed = {self.speed}')
                        time.sleep(0.5)
                except:
                    pass
            else:
                self.ls.off()

    def stopProcess(self):
        self.runMotors = False
        print("Motors Stop")
        return None

    def saveGCODE(self):
        print(self.path)

    def visualization(self):
        g_code = self.txtBox_Gcode.get("1.0", "end-1c")
        gCode_interpreter(g_code, verbose=True)


if __name__ == "__main__":
    root = tk.Tk()
    obj = App(root)
    root.mainloop()
