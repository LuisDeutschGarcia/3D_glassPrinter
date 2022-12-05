import socket
import time


class IPG_Laser():

    def __init__(self, IP = "192.168.3.230", PORT = 10001):
        self.client = None
        self.IP = IP
        self.PORT = PORT

    def init(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.IP, self.PORT))
            print(f'Laser connected. IP connection {self.IP}')
        except:
            print('Error conection, try with another IP')

    def on(self, power):
        power = (power + 49.526) / 5.8014
        self.client.send(bytes("SDC " + str(power) + "\r", 'ascii'))
        time.sleep(0.5)
        msg = self.client.recv(1024).decode('ascii')
        print(f"Response: {msg}")

    def enable(self):
        self.client.send(bytes("SDC 5.0\r", 'ascii'))
        self.client.send(bytes("EMON\r", 'ascii'))
        time.sleep(3)
        msg = self.client.recv(1024).decode('ascii')
        print(f"Data: {msg}")

    def read_power(self):
        self.client.send(bytes("ROP\r", 'ascii'))
        time.sleep(0.5)
        msg = self.client.recv(1024).decode('ascii')
        print(f"Data: {msg}")

    def off(self):
        self.client.send(bytes("EMOFF\r", 'ascii'))
        time.sleep(0.5)
        msg = self.client.recv(1024).decode('ascii')

    def debug(self):
        self.client.send(bytes("RERR\r", 'ascii'))
        time.sleep(0.5)
        msg = self.client.recv(1024).decode('ascii')
        print(msg)

if __name__ == '__main__':
    laser = IPG_Laser()
    laser.init()
    laser.debug()
