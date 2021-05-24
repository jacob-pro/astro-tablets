from unittest import TestCase

from generate.eclipse import *
from util import TimeValue, diff_mins


class EclipseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = AstroData()

    def test_lunar_eclipse(self):
        t0 = self.data.timescale.ut1(-631, 5, 1)
        t1 = self.data.timescale.ut1(-600, 6, 1)
        eclipses = lunar_eclipses_in_range(self.data, t0, t1)

        for e in eclipses:
            print("start", TimeValue(e.start_time.tt).string(self.data.timescale), "end",
                  TimeValue(e.end_time.tt).string(self.data.timescale), "max",
                  TimeValue(e.base.time.tt).string(self.data.timescale), "length",
                  diff_mins(e.start_time, e.end_time))

