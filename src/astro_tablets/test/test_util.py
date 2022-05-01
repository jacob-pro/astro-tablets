from unittest import TestCase

from astro_tablets.util import *


class UtilTest(TestCase):

    def test_change_in_longitude(self):
        self.assertEqual(change_in_longitude(350, 360), +10)
        self.assertEqual(change_in_longitude(360, 360), +0)
        self.assertEqual(change_in_longitude(360, 350), -10)
        self.assertEqual(change_in_longitude(360, 10), +10)
        self.assertEqual(change_in_longitude(10, 360), -10)
        self.assertEqual(change_in_longitude(40, 50), +10)
        self.assertEqual(change_in_longitude(358, 2), +4)
        self.assertEqual(change_in_longitude(2, 358), -4)
        self.assertEqual(change_in_longitude(2, 4), +2)
        self.assertEqual(change_in_longitude(10, 60), +50)
        self.assertEqual(change_in_longitude(60, 10), -50)
