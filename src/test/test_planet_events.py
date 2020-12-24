import pathlib
from unittest import TestCase
from bs4 import BeautifulSoup
from parse import parse

from planet_events import *
from src.util import diff_hours


class Test(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = AstroData()

    # Data from Alcyone Planetary, Stellar and Lunar Visibility
    # Stations from Alcyone Tables
    def test_venus(self):
        start = self.data.timescale.utc(2019, 9, 11)
        end = self.data.timescale.utc(2021, 2, 14)
        venus = self.data.get_body("Venus")
        events = inner_planet_events(self.data, venus, start, end, InnerPlanetArcusVisionis.venus())

        self.assertEqual(events[0].type, InnerPlanetPhenomena.EF)
        self.assertLessEqual(diff_hours(events[0].time, self.data.timescale.utc(2019, 9, 12)), 24)

        self.assertEqual(events[1].type, InnerPlanetPhenomena.ES)
        self.assertLessEqual(diff_hours(events[1].time, self.data.timescale.utc(2020, 5, 13)), 24)

        self.assertEqual(events[2].type, InnerPlanetPhenomena.EL)
        self.assertLessEqual(diff_hours(events[2].time, self.data.timescale.utc(2020, 5, 31)), 24)

        self.assertEqual(events[3].type, InnerPlanetPhenomena.MF)
        self.assertLessEqual(diff_hours(events[3].time, self.data.timescale.utc(2020, 6, 9)), 24)

        self.assertEqual(events[4].type, InnerPlanetPhenomena.MS)
        self.assertLessEqual(diff_hours(events[4].time, self.data.timescale.utc(2020, 6, 25)), 24)

        self.assertEqual(events[5].type, InnerPlanetPhenomena.ML)
        self.assertLessEqual(diff_hours(events[5].time, self.data.timescale.utc(2021, 2, 13)), 24)

    def test_mercury(self):
        start = self.data.timescale.utc(-600, 2, 18)
        end = self.data.timescale.utc(-600, 8, 10)
        mercury = self.data.get_body("Mercury")
        events = inner_planet_events(self.data, mercury, start, end, InnerPlanetArcusVisionis.mercury())

        self.assertEqual(events[0].type, InnerPlanetPhenomena.EF)
        self.assertLessEqual(diff_hours(events[0].time, self.data.timescale.utc(-600, 2, 19)), 24)

        self.assertEqual(events[1].type, InnerPlanetPhenomena.ES)
        self.assertLessEqual(diff_hours(events[1].time, self.data.timescale.utc(-600, 3, 14, 2, 12)), 24)

        self.assertEqual(events[2].type, InnerPlanetPhenomena.EL)
        self.assertLessEqual(diff_hours(events[2].time, self.data.timescale.utc(-600, 3, 17)), 24)

        self.assertEqual(events[3].type, InnerPlanetPhenomena.MS)
        self.assertLessEqual(diff_hours(events[3].time, self.data.timescale.utc(-600, 4, 6, 22, 52)), 24)

        self.assertEqual(events[4].type, InnerPlanetPhenomena.ML)
        self.assertLessEqual(diff_hours(events[4].time, self.data.timescale.utc(-600, 5, 6)), 24)

        self.assertEqual(events[5].type, InnerPlanetPhenomena.EF)
        self.assertLessEqual(diff_hours(events[5].time, self.data.timescale.utc(-600, 6, 2)), 24)

        self.assertEqual(events[6].type, InnerPlanetPhenomena.ES)
        self.assertLessEqual(diff_hours(events[6].time, self.data.timescale.utc(-600, 7, 16, 18, 43)), 24)

        self.assertEqual(events[7].type, InnerPlanetPhenomena.EL)
        self.assertLessEqual(diff_hours(events[7].time, self.data.timescale.utc(-600, 7, 16)), 24)

        self.assertEqual(events[8].type, InnerPlanetPhenomena.MS)
        self.assertLessEqual(diff_hours(events[8].time, self.data.timescale.utc(-600, 8, 8, 22, 51)), 24)

        self.assertEqual(events[9].type, InnerPlanetPhenomena.MF)
        self.assertLessEqual(diff_hours(events[9].time, self.data.timescale.utc(-600, 8, 9)), 24)

    def test_mars_visibility(self):
        expected = self.parse_plsv_outer("plsv_mars.html")
        start = self.data.timescale.utc(-750, 1, 1)
        end = self.data.timescale.utc(-741, 12, 31)
        body = self.data.get_body("Mars")
        events = outer_planet_events(self.data, body, start, end, OuterPlanetArcusVisionis.mars())
        filtered = list(filter(lambda x: x.type != OuterPlanetPhenomena.ST, events))
        for idx, val in enumerate(expected):
            actual = filtered[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 24, msg="Expected {} Got {}".format(val, actual))

    def test_jupiter_visibility(self):
        expected = self.parse_plsv_outer("plsv_jupiter.html")
        start = self.data.timescale.utc(-600, 1, 1)
        end = self.data.timescale.utc(-591, 12, 31)
        body = self.data.get_body("Jupiter")
        events = outer_planet_events(self.data, body, start, end, OuterPlanetArcusVisionis.jupiter())
        filtered = list(filter(lambda x: x.type != OuterPlanetPhenomena.ST, events))
        for idx, val in enumerate(expected):
            actual = filtered[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 30, msg="Expected {} Got {}".format(val, actual))

    def test_saturn_visibility(self):
        expected = self.parse_plsv_outer("plsv_saturn.html")
        start = self.data.timescale.utc(-550, 1, 1)
        end = self.data.timescale.utc(-540, 1, 1)
        body = self.data.get_body("Saturn")
        events = outer_planet_events(self.data, body, start, end, OuterPlanetArcusVisionis.saturn())
        filtered = list(filter(lambda x: x.type != OuterPlanetPhenomena.ST, events))
        for idx, val in enumerate(expected):
            actual = filtered[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 24, msg="Expected {} Got {}".format(val, actual))

    def parse_plsv_outer(self, name: str) -> List[SynodicEvent]:
        path = pathlib.Path(__file__).parent / 'data' / name
        with open(path.as_posix()) as f:
            soup = BeautifulSoup(f, "html.parser")
        table = soup.findAll("table")[1]
        rows = table.findAll("tr")[1:]
        filtered = list(filter(lambda x: len(list(x.children)) == 15, rows))
        expected = []
        for v in filtered:
            name = v.contents[1].string
            date = v.contents[3].string
            time = v.contents[5].string
            if name == "last visibility":
                type = OuterPlanetPhenomena.LA
            elif name == "first visibility":
                type = OuterPlanetPhenomena.FA
            elif name == "acronychal rising":
                type = OuterPlanetPhenomena.AR
            elif name == "cosmical setting":
                continue    # Skip these
            else:
                raise ValueError
            x = parse("{:d}-{:d}-{:d} {:d}:{:d}", "{} {}".format(date, time))
            time = self.data.timescale.utc(*x.fixed)
            expected.append(SynodicEvent(time, type))
        return expected
