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

#print(sailsd.set(x=5, y=10))

if __name__ == '__main__':
    unittest.main()
