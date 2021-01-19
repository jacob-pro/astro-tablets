import pathlib
from unittest import TestCase
from bs4 import BeautifulSoup
from parse import parse

from data import *
from generate.planet_events import *
from util import diff_hours


class PlanetEventsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = AstroData()

    def test_mercury(self):
        expected_visibity = self.parse_plsv_inner("plsv_mercury.html")
        start = self.data.timescale.ut1(-610, 1, 1)
        end = self.data.timescale.ut1(-600, 12, 31)
        body = self.data.get_body(MERCURY)
        events = inner_planet_events(self.data, body, start, end, InnerPlanetArcusVisionis.mercury())

        visibilities = list(filter(lambda x: x.type not in [InnerPlanetPhenomena.MS, InnerPlanetPhenomena.ES], events))
        for idx, val in enumerate(expected_visibity):
            actual = visibilities[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 24.5, msg="Expected {} Got {}".format(val, actual))

        stations = list(filter(lambda x: x.type in [InnerPlanetPhenomena.MS, InnerPlanetPhenomena.ES], events))
        expected_stations = [       # Data from Alcyone Astronomical Tables 3.0
            SynodicEvent(self.data.timescale.ut1(-610, 1, 17, 10, 5), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.ut1(-610, 2, 8, 17, 49), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.ut1(-610, 5, 20, 0, 49), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.ut1(-610, 6, 13, 4, 57), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.ut1(-610, 9, 14, 8, 45), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.ut1(-610, 10, 4, 22, 4), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.ut1(-610, 12, 31, 23, 15), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.ut1(-609, 1, 22, 13, 14), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.ut1(-609, 4, 30, 21, 1), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.ut1(-609, 5, 24, 21, 18), InnerPlanetPhenomena.MS),
        ]
        for idx, val in enumerate(expected_stations):
            actual = stations[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 24, msg="Expected {} Got {}".format(val, actual))

    def test_venus(self):
        expected_visibity = self.parse_plsv_inner("plsv_venus.html")
        start = self.data.timescale.ut1(-610, 1, 1)
        end = self.data.timescale.ut1(-601, 12, 31)
        body = self.data.get_body(VENUS)
        events = inner_planet_events(self.data, body, start, end, InnerPlanetArcusVisionis.venus())

        visibilities = list(filter(lambda x: x.type not in [InnerPlanetPhenomena.MS, InnerPlanetPhenomena.ES], events))
        for idx, val in enumerate(expected_visibity):
            actual = visibilities[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 24.5, msg="Expected {} Got {}".format(val, actual))

        stations = list(filter(lambda x: x.type in [InnerPlanetPhenomena.MS, InnerPlanetPhenomena.ES], events))
        expected_stations = [       # Data from Alcyone Astronomical Tables 3.0
            SynodicEvent(self.data.timescale.ut1(-610, 6, 24, 0, 37), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.ut1(-610, 8, 5, 21, 17), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.ut1(-608, 2, 2, 6, 24), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.ut1(-608, 3, 15, 12, 4), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.ut1(-607, 9, 5, 0, 9), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.ut1(-607, 10, 16, 12, 39), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.ut1(-605, 4, 12, 15, 51), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.ut1(-605, 5, 25, 19, 7), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.ut1(-604, 11, 18, 21, 1), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.ut1(-604, 12, 29, 18, 16), InnerPlanetPhenomena.MS),
            SynodicEvent(self.data.timescale.ut1(-602, 6, 21, 16, 18), InnerPlanetPhenomena.ES),
            SynodicEvent(self.data.timescale.ut1(-602, 8, 3, 13, 38), InnerPlanetPhenomena.MS)
        ]
        for idx, val in enumerate(expected_stations):
            actual = stations[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 24, msg="Expected {} Got {}".format(val, actual))

    def test_mars(self):
        expected = self.parse_plsv_outer("plsv_mars.html")
        start = self.data.timescale.ut1(-750, 1, 1)
        end = self.data.timescale.ut1(-741, 12, 31)
        body = self.data.get_body(MARS)
        events = outer_planet_events(self.data, body, start, end, OuterPlanetArcusVisionis.mars())
        visibilities = list(filter(lambda x: x.type != OuterPlanetPhenomena.ST, events))
        for idx, val in enumerate(expected):
            actual = visibilities[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 24.5, msg="Expected {} Got {}".format(val, actual))

        stations = list(filter(lambda x: x.type == OuterPlanetPhenomena.ST, events))
        expected_stations = [       # Data from Alcyone Astronomical Tables 3.0
            self.data.timescale.ut1(-750, 12, 31, 20, 21),
            self.data.timescale.ut1(-749, 3, 22, 3, 35),
            self.data.timescale.ut1(-747, 2, 11, 6, 33),
            self.data.timescale.ut1(-747, 4, 28, 19, 57),
            self.data.timescale.ut1(-745, 4, 11, 3, 33),
            self.data.timescale.ut1(-745, 6, 17, 9, 21),
            self.data.timescale.ut1(-743, 6, 29, 0, 59),
            self.data.timescale.ut1(-743, 8, 28, 21, 34),
        ]
        for idx, val in enumerate(expected_stations):
            actual = stations[idx]
            self.assertLessEqual(diff_hours(val, actual.time), 24, msg="Expected {} Got {}".format(val, actual))

    def test_jupiter(self):
        expected = self.parse_plsv_outer("plsv_jupiter.html")
        start = self.data.timescale.ut1(-600, 1, 1)
        end = self.data.timescale.ut1(-591, 12, 31)
        body = self.data.get_body(JUPITER)
        events = outer_planet_events(self.data, body, start, end, OuterPlanetArcusVisionis.jupiter())
        visibilities = list(filter(lambda x: x.type != OuterPlanetPhenomena.ST, events))
        for idx, val in enumerate(expected):
            actual = visibilities[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 24.5, msg="Expected {} Got {}".format(val, actual))

        stations = list(filter(lambda x: x.type == OuterPlanetPhenomena.ST, events))
        expected_stations = [       # Data from Alcyone Astronomical Tables 3.0
            self.data.timescale.ut1(-600, 6, 8, 2, 29),
            self.data.timescale.ut1(-600, 10, 4, 21, 26),
            self.data.timescale.ut1(-599, 7, 15, 18, 41),
            self.data.timescale.ut1(-599, 11, 10, 13, 46),
            self.data.timescale.ut1(-598, 8, 21, 3, 53),
            self.data.timescale.ut1(-598, 12, 16, 23, 39)
        ]
        for idx, val in enumerate(expected_stations):
            actual = stations[idx]
            self.assertLessEqual(diff_hours(val, actual.time), 24, msg="Expected {} Got {}".format(val, actual))

    def test_saturn(self):
        expected = self.parse_plsv_outer("plsv_saturn.html")
        start = self.data.timescale.ut1(-550, 1, 1)
        end = self.data.timescale.ut1(-540, 1, 1)
        body = self.data.get_body(SATURN)
        events = outer_planet_events(self.data, body, start, end, OuterPlanetArcusVisionis.saturn())
        visibilities = list(filter(lambda x: x.type != OuterPlanetPhenomena.ST, events))
        for idx, val in enumerate(expected):
            actual = visibilities[idx]
            self.assertEqual(val.type, actual.type, msg="Expected {} Got {}".format(val, actual))
            self.assertLessEqual(diff_hours(val.time, actual.time), 24, msg="Expected {} Got {}".format(val, actual))

        stations = list(filter(lambda x: x.type == OuterPlanetPhenomena.ST, events))
        expected_stations = [       # Data from Alcyone Astronomical Tables 3.0
            self.data.timescale.ut1(-550, 1, 17, 15, 43),
            self.data.timescale.ut1(-550, 6, 7, 1, 59),
            self.data.timescale.ut1(-549, 1, 29, 7, 43),
            self.data.timescale.ut1(-549, 6, 19, 6, 16),
            self.data.timescale.ut1(-548, 2, 9, 21, 0),
            self.data.timescale.ut1(-548, 6, 30, 6, 1),
            self.data.timescale.ut1(-547, 2, 20, 10, 0),
            self.data.timescale.ut1(-547, 7, 12, 2, 21),
        ]
        for idx, val in enumerate(expected_stations):
            actual = stations[idx]
            self.assertLessEqual(diff_hours(val, actual.time), 24, msg="Expected {} Got {}".format(val, actual))


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
            time = self.data.timescale.ut1(*x.fixed)
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
            time = self.data.timescale.ut1(*x.fixed)
            expected.append(SynodicEvent(time, type))
        return expected
