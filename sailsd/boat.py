import socket
import math
from functools import wraps

from .sailsd import Sailsd


E_RADIUS = 6378000


class Boat(object):
    '''
    A merry sailing boat sailing on the seas.

    :param sailsd: an instance of ``sailsd.Sailsd`` to use instead of creating a
                   new instance
    :param auto_update: whether to automatically request updated values on each
                        attribute request. Setting this to True makes using
                        ``update()`` redundant.
    :type auto_update: bool

    Some example usage:

        >>> boat = sailsd.Boat()
        >>> boat.rudder_angle = 0.1
        >>> boat.update()
        >>> boat.heading
        0.758290214606183
        >>> boat.speed
        4.6089232392605135
        >>> boat.latitude, boat.longitude
        (0.0009904288095353697, 0.0009966210180718897)
    '''
    _attrs = (
              'latitude',
              'longitude',
              'heading',
              'rudder-angle',
              'sail-angle',
              'speed',
            )

    def __init__(self, sailsd=None, auto_update=False):
        self.sailsd = sailsd or Sailsd()
        self.status = 'not connected'

        self.auto_update = auto_update

        self.values = {}

        for a in self._attrs:
            self.values.update({a: 0})

        self.update()

    def _auto_update(f):
        @wraps(f)
        def dec(self) :
            if self.auto_update:
                self.update()
            return f(self)
        return dec

    @property
    @_auto_update
    def x(self):
        '''Longitude approximately projected to an x y meter grid'''
        return E_RADIUS * (self.longitude / (180 / math.pi))

    @property
    @_auto_update
    def y(self):
        '''Latitude approximately projected to an x y meter grid'''
        return E_RADIUS * (self.latitude / ((180 / math.pi) /
            math.cos(self.latitude * math.pi/180)))

    @property
    @_auto_update
    def latitude(self):
        '''Current latitude of the boat'''
        return self.values.get('latitude')

    @property
    @_auto_update
    def longitude(self):
        '''Current longitude of the boat'''
        return self.values.get('longitude')

    @property
    @_auto_update
    def heading(self):
        '''Current heading of the boat, measured in radians from the bow'''
        return self.values.get('heading')

    @property
    @_auto_update
    def rudder_angle(self):
        '''Angle of the rudder, measured in radians where 0 is a straight rudder'''
        return self.values.get('rudder-angle')

    @rudder_angle.setter
    def rudder_angle(self, angle):
        self.sailsd.set(rudder_angle=angle)

    @property
    @_auto_update
    def sail_angle(self):
        '''Angle of the sail, measured in radians where 0 is the sail pulled to
        the exact center of the boat'''
        return self.values.get('sail-angle')

    @sail_angle.setter
    def sail_angle(self, angle):
        self.sailsd.set(sail_angle=angle)

    @property
    @_auto_update
    def speed(self):
        '''Current speed of the boat, measured in meters per second'''
        return self.values.get('speed')

    def update(self):
        '''
        Read attributes from sailsd and update all values. For example:

            >>> boat = sailsd.Boat()
            >>> boat.update()
            >>> boat.latitude
            100.00292426652119

        This should be run just before reading values to ensure they are up to
        date.
            '''
        try:
            res = self.sailsd.request(*self._attrs)
        except socket.error:
            self.status = 'not connected'
        else:
            self.status = 'connected'
            self.values.update(res)
