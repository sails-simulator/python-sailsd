import unittest

from sailsd import Sailsd

sailsd = Sailsd()

class TestSailsdAPI(unittest.TestCase):
    def test_version(self):
        r = sailsd.request('version')
        self.assertTrue('version' in r)

    def test_latitude(self):
        r = sailsd.request('latitude')
        self.assertTrue('latitude' in r)

    def test_multiple(self):
        r = sailsd.request('latitude', 'longitude')
        self.assertTrue('latitude' in r)
        self.assertTrue('longitude' in r)

    def test_invalid_attribute(self):
        r = sailsd.request('ddlongitude', 'latituddde')
        self.assertTrue(len(r) == 0)

    def test_sail_angle(self):
        r = sailsd.request('sail-angle')
        self.assertTrue('sail-angle' in r)
        self.assertTrue(isinstance(r.get('sail-angle'), float))

    def test_heading(self):
        r = sailsd.request('heading')
        self.assertTrue('heading' in r)
        self.assertTrue(isinstance(r.get('heading'), float))

    def test_rudder_angle(self):
        r = sailsd.request('rudder-angle')
        self.assertTrue('rudder-angle' in r)
        self.assertTrue(isinstance(r.get('rudder-angle'), float))

    def test_request_all(self):
        attrs = ['version',
                 'latitude',
                 'longitude',
                 'sail-angle',
                 'heading',
                 'rudder-angle',
                ]
        r = sailsd.request(*attrs)
        self.assertTrue(all([a in r for a in attrs]))

class TestSailsdAPIWrite(unittest.TestCase):
    def test_set_latitude(self):
        r = sailsd.set(latitude=100)
        #r = sailsd.set(latitude=100, thing=100, longitude=100)
        r = sailsd.request('latitude')

    def test_set_latitude_and_longitude(self):
        r = sailsd.set(latitude=100, longitude=100)
        r = sailsd.request('latitude', 'longitude')

    def test_set_sail_angle(self):
        r = sailsd.set(sail_angle=100)
        r = sailsd.request('sail-angle')

    def test_set_rudder_angle(self):
        r = sailsd.set(rudder_angle=10)
        r = sailsd.request('rudder-angle')
        r = sailsd.set(rudder_angle=-10)
        r = sailsd.request('rudder-angle')

if __name__ == '__main__':
    unittest.main()
