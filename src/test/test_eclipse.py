from unittest import TestCase

from generate.eclipse import *


class EclipseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = AstroData()

    def test_lunar_eclipse(self):
        t0 = self.data.timescale.ut1(-631, 5, 1)
        t1 = self.data.timescale.ut1(-631, 6, 1)
        lunar_eclipses_in_range(self.data, t0, t1)

