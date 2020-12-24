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

    def test_mercury(self):
        expected_visibity = self.parse_plsv_inner("plsv_mercury.html")
        start = self.data.timescale.utc(-610, 1, 1)
        end = self.data.timescale.utc(-600, 12, 31)
        body = self.data.get_body("Mercury")
        events = inner_planet_events(self.data, body, start, end, InnerPlanetArcusVisionis.mercury())

        visibilities = list(filter(lambda x: x.type not in [InnerPlanetPhenomena.MS, InnerPlanetPhenomena.ES], events))
        for idx, val in enumerate(expected_visibity):
            actual = visibilities[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 30, msg="Expected {} Got {}".format(val, actual))

        stations = list(filter(lambda x: x.type in [InnerPlanetPhenomena.MS, InnerPlanetPhenomena.ES], events))
        expected_stations = [       # Data from Alcyone Astronomical Tables 3.0
            SynodicEvent(self.data.timescale.utc(-610, 1, 17, 10, 5), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.utc(-610, 2, 8, 17, 49), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.utc(-610, 5, 20, 0, 49), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.utc(-610, 6, 13, 4, 57), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.utc(-610, 9, 14, 8, 45), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.utc(-610, 10, 4, 22, 4), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.utc(-610, 12, 31, 23, 15), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.utc(-609, 1, 22, 13, 14), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.utc(-609, 4, 30, 21, 1), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.utc(-609, 5, 24, 21, 18), InnerPlanetPhenomena.MS),
        ]
        for idx, val in enumerate(expected_stations):
            actual = stations[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 24, msg="Expected {} Got {}".format(val, actual))

    def test_venus(self):
        expected_visibity = self.parse_plsv_inner("plsv_venus.html")
        start = self.data.timescale.utc(-610, 1, 1)
        end = self.data.timescale.utc(-601, 12, 31)
        body = self.data.get_body("Venus")
        events = inner_planet_events(self.data, body, start, end, InnerPlanetArcusVisionis.venus())

        visibilities = list(filter(lambda x: x.type not in [InnerPlanetPhenomena.MS, InnerPlanetPhenomena.ES], events))
        for idx, val in enumerate(expected_visibity):
            actual = visibilities[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 30, msg="Expected {} Got {}".format(val, actual))

        stations = list(filter(lambda x: x.type in [InnerPlanetPhenomena.MS, InnerPlanetPhenomena.ES], events))
        expected_stations = [       # Data from Alcyone Astronomical Tables 3.0
            SynodicEvent(self.data.timescale.utc(-610, 6, 24, 0, 37), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.utc(-610, 8, 5, 21, 17), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.utc(-608, 2, 2, 6, 24), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.utc(-608, 3, 15, 12, 4), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.utc(-607, 9, 5, 0, 9), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.utc(-607, 10, 16, 12, 39), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.utc(-605, 4, 12, 15, 51), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.utc(-605, 5, 25, 19, 7), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.utc(-604, 11, 18, 21, 1), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.utc(-604, 12, 29, 18, 16), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.utc(-602, 6, 21, 16, 18), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.utc(-602, 8, 3, 13, 38), InnerPlanetPhenomena.MS)
        ]
        for idx, val in enumerate(expected_stations):
            actual = stations[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 24, msg="Expected {} Got {}".format(val, actual))

    def test_mars(self):
        expected = self.parse_plsv_outer("plsv_mars.html")
        start = self.data.timescale.utc(-750, 1, 1)
        end = self.data.timescale.utc(-741, 12, 31)
        body = self.data.get_body("Mars")
        events = outer_planet_events(self.data, body, start, end, OuterPlanetArcusVisionis.mars())
        visibilities = list(filter(lambda x: x.type != OuterPlanetPhenomena.ST, events))
        for idx, val in enumerate(expected):
            actual = visibilities[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 24, msg="Expected {} Got {}".format(val, actual))

    def test_jupiter(self):
        expected = self.parse_plsv_outer("plsv_jupiter.html")
        start = self.data.timescale.utc(-600, 1, 1)
        end = self.data.timescale.utc(-591, 12, 31)
        body = self.data.get_body("Jupiter")
        events = outer_planet_events(self.data, body, start, end, OuterPlanetArcusVisionis.jupiter())
        visibilities = list(filter(lambda x: x.type != OuterPlanetPhenomena.ST, events))
        for idx, val in enumerate(expected):
            actual = visibilities[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 30, msg="Expected {} Got {}".format(val, actual))

    def test_saturn(self):
        expected = self.parse_plsv_outer("plsv_saturn.html")
        start = self.data.timescale.utc(-550, 1, 1)
        end = self.data.timescale.utc(-540, 1, 1)
        body = self.data.get_body("Saturn")
        events = outer_planet_events(self.data, body, start, end, OuterPlanetArcusVisionis.saturn())
        visibilities = list(filter(lambda x: x.type != OuterPlanetPhenomena.ST, events))
        for idx, val in enumerate(expected):
            actual = visibilities[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 24, msg="Expected {} Got {}".format(val, actual))

    def parse_plsv_inner(self, name: str) -> List[SynodicEvent]:
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
            if name == "evening visibility ends":
                type = InnerPlanetPhenomena.EL
            elif name == "morning visibility begins":
                type = InnerPlanetPhenomena.MF
            elif name == "morning visibility ends":
                type = InnerPlanetPhenomena.ML
            elif name == "evening visibility begins":
                type = InnerPlanetPhenomena.EF
            else:
                raise ValueError
            x = parse("{:d}-{:d}-{:d} {:d}:{:d}", "{} {}".format(date, time))
            time = self.data.timescale.utc(*x.fixed)
            expected.append(SynodicEvent(time, type))
        return expected

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
