import socket
import math

from .sailsd import Sailsd

#TODO: remove duplicated code with Boat
class Wind(object):
    '''
    Some wind wafting over the sea.

    :param sailsd: an instance of ``sailsd.Sailsd`` to use instead of creating a
                   new instance
    :type sailsd: ``sailsd.Sailsd``
    '''

    _attrs = (
              'wind-speed',
              'wind-angle',
            )

    def __init__(self, sailsd=None):
        self.sailsd = sailsd or Sailsd()
        self.status = 'not connected'

        self.values = {}

        for a in self._attrs:
            self.values.update({a: 0})

        self.update()

    @property
    def speed(self):
        '''
        Speed of wind in meters per second.
        '''
        return self.values.get('wind-speed')

    @speed.setter
    def speed(self, angle):
        self.sailsd.set(wind_speed=angle)

    @property
    def angle(self):
        '''
        Angle of wind direction in radians. A value of 0 is a movement of wind
        from north to south.
        '''
        return self.values.get('wind-angle')

    @angle.setter
    def angle(self, angle):
        self.sailsd.set(wind_angle=angle)

    def update(self):
        '''
        Read attributes from sailsd and update values. For example:
            
            >>> wind = sailsd.Wind()
            >>> wind.update()
            >>> wind.speed
            4.0
            >>> wind.angle
            1.5707963267948966
        '''
        try:
            res = self.sailsd.request(*self._attrs)
        except socket.error:
            self.status = 'not connected'
        else:
            self.status = 'connected'
            self.values.update(res)
