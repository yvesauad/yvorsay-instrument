# standard libraries
from nion.utils import Event
from nion.utils import Observable

import threading
import numpy
import socket

GREEN = (numpy.ones((25, 35), dtype=numpy.uint32)) * 2000000000
RED = (numpy.ones((25, 35), dtype=numpy.uint32)) * 4000000000

class serverDevice(Observable.Observable):
    def __init__(self):
        self.property_changed_event = Event.Event()

        self.__colorLaser = RED
        self.__colorPM01 = RED
        self.__colorPM02 = RED
        self.__colorPS = RED
        self.__colorArd = RED

    def init(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('127.0.0.1', 65432))
        self.s.sendall('bc'.encode())
        data = self.s.recv(512)

        if data == b'bc':
            return True
        else:
            return False

    def loop(self):
        threading.Timer(0.02, self.read, args=(),).start()

    def read(self):
        self.color_laser=self.color_pm01=self.color_pm02=self.color_ps=self.color_ard='red'
        data = self.s.recv(512)
        if b'get_hardware_wl' in data:
            self.color_laser='green'
        elif b'query' in data:
            self.color_ps='green'
        elif b'pw_' in data:
            self.color_pm01='gren'
        self.loop()

    @property
    def color_laser(self):
        return self.__colorLaser

    @color_laser.setter
    def color_laser(self, value):
        if value=='red':
            self.__colorLaser = RED
        else:
            self.__colorLaser = GREEN
        self.property_changed_event.fire("color_laser")

    @property
    def color_pm01(self):
        return self.__colorPM01

    @color_pm01.setter
    def color_pm01(self, value):
        if value == 'red':
            self.__colorPM01 = RED
        else:
            self.__colorPM01 = GREEN
        self.property_changed_event.fire('color_pm01')

    @property
    def color_pm02(self):
        return self.__colorPM02

    @color_pm02.setter
    def color_pm02(self, value):
        if value=='red':
            self.__colorPM02 = RED
        else:
            self.__colorPM02 = GREEN
        self.property_changed_event.fire('color_pm02')

    @property
    def color_ps(self):
        return self.__colorPS

    @color_ps.setter
    def color_ps(self, value):
        if value=='red':
            self.__colorPS = RED
        else:
            self.__colorPS = GREEN
        self.property_changed_event.fire('color_ps')

    @property
    def color_ard(self):
        return self.__colorArd

    @color_ard.setter
    def color_ard(self, value):
        if value=='red':
            self.__colorArd = RED
        else:
            self.__colorArd = GREEN
        self.property_changed_event.fire('color_ard')