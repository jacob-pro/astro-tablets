import pathlib
from unittest import TestCase

from bs4 import BeautifulSoup
from parse import parse
from skyfield.timelib import CalendarTuple

from lunar_calendar import *
from src.util import *


class Test(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = AstroData()

    def test_vernal_equinox(self):
        expected = self.data.timescale.utc(-600, 3, 27, 7, 29)
        self.assertLessEqual(diff_hours(vernal_equinox(self.data, -600), expected), 6)

        expected = self.data.timescale.utc(-599, 3, 27, 13, 17)
        self.assertLessEqual(diff_hours(vernal_equinox(self.data, -599), expected), 6)

        expected = self.data.timescale.utc(-598, 3, 27, 19, 4)
        self.assertLessEqual(diff_hours(vernal_equinox(self.data, -598), expected), 6)

        expected = self.data.timescale.utc(1000, 3, 14, 23, 11, 47)
        self.assertLessEqual(diff_secs(vernal_equinox(self.data, 1000), expected), 3600)

        expected = self.data.timescale.utc(2020, 3, 20, 3, 49, 35)
        self.assertLessEqual(diff_secs(vernal_equinox(self.data, 2020), expected), 3600)

    # Altitude at sunset calculated in Starry Night 6.4.4
    def test_altitude_of_moon(self):
        sunset = sunset_and_rise_for_date(self.data, -603, 4, 1)[0]
        angle = altitude_of_moon(self.data, sunset)
        self.assertLessEqual(abs(21.3 - angle.degrees), 1.0)

        sunset = sunset_and_rise_for_date(self.data, 604, 4, 1)[0]
        angle = altitude_of_moon(self.data, sunset)
        self.assertLessEqual(abs(-42.0 - angle.degrees), 1.0)

    # Parker/Dubberstein months in 568 BC
    # Do not expect a 100% match because of using slightly different visibility criteria
    def test_days_in_range_pd(self):
        days = days_in_range(self.data, self.data.timescale.utc(-567, 3, 1), self.data.timescale.utc(-566, 3, 30))
        months = list(filter(lambda x: x.first_visibility is True, days))
        self.assertTrue(same_day(months[0].sunrise.utc, -567, 3, 25))
        self.assertTrue(same_day(months[1].sunrise.utc, -567, 4, 23))
        # self.assertTrue(same_day(months[2].sunrise.utc, -567, 5, 23))
        self.assertTrue(same_day(months[3].sunrise.utc, -567, 6, 21))
        self.assertTrue(same_day(months[4].sunrise.utc, -567, 7, 20))
        self.assertTrue(same_day(months[5].sunrise.utc, -567, 8, 19))
        self.assertTrue(same_day(months[6].sunrise.utc, -567, 9, 17))
        self.assertTrue(same_day(months[7].sunrise.utc, -567, 10, 17))
        self.assertTrue(same_day(months[8].sunrise.utc, -567, 11, 16))
        self.assertTrue(same_day(months[9].sunrise.utc, -567, 12, 16))
        self.assertTrue(same_day(months[10].sunrise.utc, -566, 1, 15))
        self.assertTrue(same_day(months[11].sunrise.utc, -566, 2, 13))
        self.assertTrue(same_day(months[12].sunrise.utc, -566, 3, 15))

    def test_days_in_range_(self):
        expected = self.parse_plsv_moon("plsv_moon.html")
        days = days_in_range(self.data, self.data.timescale.utc(-580, 1, 1), self.data.timescale.utc(-579, 12, 31))
        months = list(filter(lambda x: x.first_visibility is True, days))
        for idx, val in enumerate(expected):
            actual = months[idx].sunset
            self.assertLessEqual(diff_hours(val, actual), 24)

    def parse_plsv_moon(self, name: str) -> List[Time]:
        path = pathlib.Path(__file__).parent / 'data' / name
        with open(path.as_posix()) as f:
            soup = BeautifulSoup(f, "html.parser")
        table = soup.findAll("table")[1]
        rows = table.findAll("tr")[1:]
        filtered = list(filter(lambda x: len(list(x.children)) == 17, rows))
        expected = []
        for v in filtered:
            name = v.contents[1].string
            date = v.contents[3].string
            time = v.contents[5].string
            if name == "first visibility":
                x = parse("{:d}-{:d}-{:d} {:d}:{:d}", "{} {}".format(date, time))
                time = self.data.timescale.utc(*x.fixed)
                expected.append(time)
        return expected



def same_day(x: CalendarTuple, year: int, month: int, day: int):
    return x.year == year and x.month == month and x.day == day
