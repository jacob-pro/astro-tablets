from unittest import TestCase

from skyfield.starlib import Star

from astro_tablets.constants import MERCURY, MOON
from astro_tablets.generate.angular_separation import *
from astro_tablets.generate.lunar_calendar import sunset_and_rise_for_date


class AngularSeparationTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = AstroData()

    # Starry Night 6.4.4
    def test_angular_separation(self):
        time = sunset_and_rise_for_date(self.data, 2020, 12, 17)[0]

        moon = self.data.get_body(MOON)
        mercury = self.data.get_body(MERCURY)

        sep, pos = angular_separation(self.data, moon, mercury, time)
        self.assertLessEqual(abs(sep.degrees - 39.1), 1.0)
        self.assertEqual(pos, EclipticPosition.BEHIND)

        sep, pos = angular_separation(self.data, mercury, moon, time)
        self.assertEqual(pos, EclipticPosition.AHEAD)
        self.assertLessEqual(abs(sep.degrees - 39.1), 1.0)

        dablin = Star.from_dataframe(self.data.stars.loc[100345])
        sep, pos = angular_separation(self.data, moon, dablin, time)
        self.assertEqual(pos, EclipticPosition.BELOW)
        self.assertLessEqual(abs(sep.degrees - 8.9), 1.0)

        sep, pos = angular_separation(self.data, dablin, moon, time)
        self.assertEqual(pos, EclipticPosition.ABOVE)
        self.assertLessEqual(abs(sep.degrees - 8.9), 1.0)

        fomalhaut = Star.from_dataframe(self.data.stars.loc[113368])
        sep, pos = angular_separation(self.data, fomalhaut, mercury, time)
        self.assertEqual(pos, EclipticPosition.BEHIND)
        self.assertLessEqual(abs(sep.degrees - 70.45), 1.0)

        sep, pos = angular_separation(self.data, mercury, fomalhaut, time)
        self.assertEqual(pos, EclipticPosition.AHEAD)
        self.assertLessEqual(abs(sep.degrees - 70.45), 1.0)
