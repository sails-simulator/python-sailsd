from .sailsd import Sailsd

class Boat(object):
    attrs = (
              'latitude',
              'longitude',
              'heading',
              'rudder-angle',
              'sail-angle',
            )

    def __init__(self, sailsd=None):
        self.sailsd = sailsd or Sailsd()
        self.latitude = 0
        self.longitude = 0
        self.update()

    def update(self):
        '''Read attributes from sailsd and update values'''
        res = self.sailsd.request(*self.attrs)
        for a in self.attrs:
            v = res.get(a)
            setattr(self, a, v)

        self.x = self.longitude
        self.y = self.latitude
