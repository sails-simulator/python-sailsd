import socket
import math

from .sailsd import Sailsd

def attributify(s):
    return s.replace('-', '_')

class Boat(object):
    attrs = (
              'latitude',
              'longitude',
              'heading',
              'rudder-angle',
              'sail-angle',
              'speed',
            )

    def __init__(self, sailsd=None):
        self.sailsd = sailsd or Sailsd()
        self.status = 'not connected'

        self.values = {}

        for a in self.attrs:
            self.values.update({a: 0})

        # latitude and longitude approximately projected to an x y meter grid
        self.x = 0
        self.y = 0

        self.update()

    def update_xy(self):
        e_radius = 6378000
        self.x = e_radius * (self.longitude / (180 / math.pi))
        self.y = e_radius * (self.latitude / ((180 / math.pi) /
            math.cos(self.latitude * math.pi/180)))

    @property
    def latitude(self):
        return self.values.get('latitude')

    @property
    def longitude(self):
        return self.values.get('longitude')

    @property
    def heading(self):
        return self.values.get('heading')

    @property
    def rudder_angle(self):
        return self.values.get('rudder-angle')

    @rudder_angle.setter
    def rudder_angle(self, angle):
        self.sailsd.set(rudder_angle=angle)

    @property
    def sail_angle(self):
        return self.values.get('sail-angle')

    @sail_angle.setter
    def sail_angle(self, angle):
        self.sailsd.set(sail_angle=angle)

    @property
    def speed(self):
        return self.values.get('speed')

    def update(self):
        '''Read attributes from sailsd and update values'''
        try:
            res = self.sailsd.request(*self.attrs)
        except socket.error:
            self.status = 'not connected'
        else:
            self.status = 'connected'
            self.values.update(res)

            self.update_xy()
