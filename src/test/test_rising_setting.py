from unittest import TestCase

from data import *
from generate.planet_events import *
from generate.risings_settings import risings_and_settings, RiseSetType
from util import diff_mins


class RisingSettingTest(TestCase):
    TEST_MINS = 2

    @classmethod
    def setUpClass(cls):
        cls.data = AstroData()

    # Data from Starry Night Pro Plus 6.4.3
    def test_moon(self):
        start = self.data.timescale.ut1(-600, 1, 1)
        end = self.data.timescale.ut1(-600, 1, 6)
        rs = risings_and_settings(self.data, MOON, start, end)

        self.assertEqual(rs[0].type, RiseSetType.RISE)
        self.assertLessEqual(diff_mins(self.data.timescale.ut1(-600, 1, 1, 6, 22), rs[0].time), self.TEST_MINS)

        self.assertEqual(rs[1].type, RiseSetType.SET)
        self.assertLessEqual(diff_mins(self.data.timescale.ut1(-600, 1, 1, 16, 31), rs[1].time), self.TEST_MINS)

        self.assertEqual(rs[2].type, RiseSetType.RISE)
        self.assertLessEqual(diff_mins(self.data.timescale.ut1(-600, 1, 2, 6, 56), rs[2].time), self.TEST_MINS)

        self.assertEqual(rs[3].type, RiseSetType.SET)
        self.assertLessEqual(diff_mins(self.data.timescale.ut1(-600, 1, 2, 17, 29), rs[3].time), self.TEST_MINS)

        self.assertEqual(rs[4].type, RiseSetType.RISE)
        self.assertLessEqual(diff_mins(self.data.timescale.ut1(-600, 1, 3, 7, 26), rs[4].time), self.TEST_MINS)

        self.assertEqual(rs[5].type, RiseSetType.SET)
        self.assertLessEqual(diff_mins(self.data.timescale.ut1(-600, 1, 3, 18, 26), rs[5].time), self.TEST_MINS)

        self.assertEqual(rs[6].type, RiseSetType.RISE)
        self.assertLessEqual(diff_mins(self.data.timescale.ut1(-600, 1, 4, 7, 53), rs[6].time), self.TEST_MINS)

        self.assertEqual(rs[7].type, RiseSetType.SET)
        self.assertLessEqual(diff_mins(self.data.timescale.ut1(-600, 1, 4, 19, 22), rs[7].time), self.TEST_MINS)

        self.assertEqual(rs[8].type, RiseSetType.RISE)
        self.assertLessEqual(diff_mins(self.data.timescale.ut1(-600, 1, 5, 8, 18), rs[8].time), self.TEST_MINS)

        self.assertEqual(rs[9].type, RiseSetType.SET)
        self.assertLessEqual(diff_mins(self.data.timescale.ut1(-600, 1, 5, 20, 17), rs[9].time), self.TEST_MINS)

