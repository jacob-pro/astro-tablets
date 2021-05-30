from unittest import TestCase

from generate.eclipse import *
from util import TimeValue


class EclipseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = AstroData()

    def test_lunar_eclipse(self):
        t0 = self.data.timescale.ut1(-631, 5, 1)
        t1 = self.data.timescale.ut1(-600, 9, 1)
        eclipses = lunar_eclipses_in_range(self.data, t0, t1)

        for e in eclipses:
            print(TimeValue(e.closest_approach_time.tt).string(self.data.timescale),
                  e.type,
                  e.phases())

