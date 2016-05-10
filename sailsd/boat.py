import socket
import math

from .sailsd import Sailsd

def attributify(s):
    return s.replace('-', '_')

class Boat(object):
    '''
    A boat sailing on the seas.

    :param sailsd: an instance of `sailsd.Sailsd` to use instead of creating a
                   new instance
    :type sailsd: `sailsd.Sailsd`
    '''
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

    def _update_xy(self):
        e_radius = 6378000
        self.x = e_radius * (self.longitude / (180 / math.pi))
        self.y = e_radius * (self.latitude / ((180 / math.pi) /
            math.cos(self.latitude * math.pi/180)))

    @property
    def latitude(self):
        '''Current latitude of the boat'''
        return self.values.get('latitude')

    @property
    def longitude(self):
        '''Current longitude of the boat'''
        return self.values.get('longitude')

    @property
    def heading(self):
        '''Current heading of the boat, measured in radians from the bow'''
        return self.values.get('heading')

    @property
    def rudder_angle(self):
        '''Angle of the rudder, measured in radians where 0 is a straight rudder'''
        return self.values.get('rudder-angle')

    @rudder_angle.setter
    def rudder_angle(self, angle):
        self.sailsd.set(rudder_angle=angle)

    @property
    def sail_angle(self):
        '''Angle of the sail, measured in radians where 0 is the sail pulled to
        the exact center of the boat'''
        return self.values.get('sail-angle')

    @sail_angle.setter
    def sail_angle(self, angle):
        self.sailsd.set(sail_angle=angle)

    @property
    def speed(self):
        '''Current speed of the boat, measured in meters per second'''
        return self.values.get('speed')

    def update(self):
        '''Read attributes from sailsd and update all values'''
        try:
            res = self.sailsd.request(*self.attrs)
        except socket.error:
            self.status = 'not connected'
        else:
            self.status = 'connected'
            self.values.update(res)

            self._update_xy()
