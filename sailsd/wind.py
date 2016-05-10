import socket
import math

from .sailsd import Sailsd

#TODO: remove duplicated code with Boat
class Wind(object):
    attrs = (
              'wind-speed',
              'wind-angle',
            )

    def __init__(self, sailsd=None):
        self.sailsd = sailsd or Sailsd()
        self.status = 'not connected'

        self.values = {}

        for a in self.attrs:
            self.values.update({a: 0})

        self.update()

    @property
    def speed(self):
        return self.values.get('wind-speed')

    @speed.setter
    def speed(self, angle):
        self.sailsd.set(wind_speed=angle)

    @property
    def angle(self):
        return self.values.get('wind-angle')

    @angle.setter
    def angle(self, angle):
        self.sailsd.set(wind_angle=angle)

    def update(self):
        '''Read attributes from sailsd and update values'''
        try:
            res = self.sailsd.request(*self.attrs)
        except socket.error:
            self.status = 'not connected'
        else:
            self.status = 'connected'
            self.values.update(res)
