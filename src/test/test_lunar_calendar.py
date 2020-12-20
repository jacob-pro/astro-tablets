from unittest import TestCase

from skyfield.timelib import CalendarTuple

from lunar_calendar import *
from src.util import *


class Test(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = AstroData()

    # Confirm equinox accurate to 1hr
    # https://stellafane.org/misc/equinox.html (Uses mixed calendar)
    def test_vernal_equinox(self):
        result = vernal_equinox(self.data, 1000)
        expected = self.data.timescale.utc(1000, 3, 14, 23, 11, 47)
        self.assertLessEqual(diff_secs(result, expected), 3600)

        result = vernal_equinox(self.data, 2020)
        expected = self.data.timescale.utc(2020, 3, 20, 3, 49, 35)
        self.assertLessEqual(diff_secs(result, expected), 3600)

    # Altitude at sunset calculated in Starry Night 6.4.4
    def test_altitude_of_moon(self):
        sunset = sunset_and_rise_for_date(self.data, -603, 4, 1).sunset
        angle = altitude_of_moon(self.data, sunset)
        self.assertLessEqual(abs(21.3 - angle.degrees), 1.0)

        sunset = sunset_and_rise_for_date(self.data, 604, 4, 1).sunset
        angle = altitude_of_moon(self.data, sunset)
        self.assertLessEqual(abs(-42.0 - angle.degrees), 1.0)

    # Parker/Dubberstein months in 568 BC
    # Do not expect a 100% match because of using slightly different visibility criteria
    def test_months_for_year(self):
        months = months_for_year(self.data, -567, False)
        self.assertTrue(same_day(months[0].days[0].sunrise.utc, -567, 3, 25))
        self.assertTrue(same_day(months[1].days[0].sunrise.utc, -567, 4, 23))
        # self.assertTrue(same_day(months[2].days[0].sunrise.utc, -567, 5, 23))
        self.assertTrue(same_day(months[3].days[0].sunrise.utc, -567, 6, 21))
        self.assertTrue(same_day(months[4].days[0].sunrise.utc, -567, 7, 20))
        self.assertTrue(same_day(months[5].days[0].sunrise.utc, -567, 8, 19))
        self.assertTrue(same_day(months[6].days[0].sunrise.utc, -567, 9, 17))
        self.assertTrue(same_day(months[7].days[0].sunrise.utc, -567, 10, 17))
        self.assertTrue(same_day(months[8].days[0].sunrise.utc, -567, 11, 16))
        self.assertTrue(same_day(months[9].days[0].sunrise.utc, -567, 12, 16))
        self.assertTrue(same_day(months[10].days[0].sunrise.utc, -566, 1, 15))
        self.assertTrue(same_day(months[11].days[0].sunrise.utc, -566, 2, 13))
        self.assertTrue(same_day(months[12].days[0].sunrise.utc, -566, 3, 15))


def same_day(x: CalendarTuple, year: int, month: int, day: int):
    return x.year == year and x.month == month and x.day == day
