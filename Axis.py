from ctypes import *
import time
import os
import sys
import platform
import tempfile
import re
from Init_file import *

class axis:
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.flag_virtual = 0
        self.device_id = None

    def init(self):

        print("Library loaded")
        sbuf = create_string_buffer(64)
        lib.ximc_version(sbuf)

        # Set bindy (network) keyfile. Must be called before any call to "enumerate_devices" or "open_device" if you
        # wish to use network-attached controllers. Accepts both absolute and relative paths, relative paths are resolved
        # relative to the process working directory. If you do not need network devices then "set_bindy_key" is optional.
        # In Python make sure to pass byte-array object to this function (b"string literal").
        result = lib.set_bindy_key(os.path.join(ximc_dir, "win32", "keyfile.sqlite").encode("utf-8"))
        if result != Result.Ok:
            lib.set_bindy_key("keyfile.sqlite".encode("utf-8"))  # Search for the key file in the current directory.

        self.device_id = lib.open_device(self.serial_number)
        print( f"Device connected: {self.serial_number}")

        lib.command_zero(self.device_id)

    def axis_move(self, position, speed=500, accel=10000, decel=10000):
        mvst = move_settings_t()
        mvst.Speed, mvst.Accel, mvst.Decel = int(speed), int(accel), int(decel)
        lib.set_move_settings(self.device_id, byref(mvst))
        lib.command_move(self.device_id, position, 0)
        # lib.command_wait_for_stop(self.device_id, 100)

    def axis_movr(self, position, speed=500, accel=10000, decel=10000):
        mvst = move_settings_t()
        mvst.Speed, mvst.Accel, mvst.Decel = int(speed), int(accel), int(decel)
        lib.set_move_settings(self.device_id, byref(mvst))
        lib.command_movr(self.device_id, position, 0)
        # lib.command_wait_for_stop(self.device_id, 100)

    def axis_getPosition(self, verbose=False):
        axis_pos = get_position_t()
        if verbose: print(axis_pos.Position, axis_pos.uPosition)
        return [axis_pos.Position, axis_pos.uPosition]

    def axis_getStatus(self, verbose=False):
        axis_status = status_t()
        lib.get_status(self.device_id, byref(axis_status))
        if verbose :
            print(f"Power supply Voltage: {axis_status.Upwr}\n"
                  f"Engine current: {axis_status.Ipwr}\n"
                  f"Motor Shaft Speed: {axis_status.CurSpeed}\n"
                  f"Current Encoder Position: {axis_status.EncPosition}\n"
                  f"USB current: {axis_status.Iusb}\n"
                  f"USB voltage [mV]: {axis_status.Uusb}.\n")
        return [axis_status.Upwr, axis_status.Ipwr]

    def axis_close(self):
        lib.close_device(byref(cast(self.device_id, POINTER(c_int))))

    def axis_stop(self, time = 100):
        lib.command_wait_for_stop(self.device_id, time)
