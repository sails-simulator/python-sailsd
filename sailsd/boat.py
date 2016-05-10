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

        for a in self.attrs:
            setattr(self, attributify(a), 0)

        # latitude and longitude approximately projected to an x y meter grid
        self.x = 0
        self.y = 0

        self.update()

    def update_xy(self):
        e_radius = 6378000
        self.x = e_radius * (self.longitude / (180 / math.pi))
        self.y = e_radius * (self.latitude / ((180 / math.pi) /
            math.cos(self.latitude * math.pi/180)))

    def update(self):
        '''Read attributes from sailsd and update values'''
        try:
            res = self.sailsd.request(*self.attrs)
        except socket.error:
            self.status = 'not connected'
        else:
            self.status = 'connected'
            for a in self.attrs:
                v = res.get(a)
                setattr(self, attributify(a), v)

            self.update_xy()
