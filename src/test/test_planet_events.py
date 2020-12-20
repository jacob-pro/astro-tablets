from unittest import TestCase

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

    def test_mars(self):
        start = self.data.timescale.utc(646, 9, 19)
        end = self.data.timescale.utc(648, 7, 16)
        mars = self.data.get_body("Mars")
        events = outer_planet_events(self.data, mars, start, end, OuterPlanetArcusVisionis.mars())

        self.assertEqual(events[0].type, OuterPlanetPhenomena.FA)
        self.assertLessEqual(diff_hours(events[0].time, self.data.timescale.utc(646, 9, 20)), 24)

        self.assertEqual(events[1].type, OuterPlanetPhenomena.ST)

        self.assertEqual(events[2].type, OuterPlanetPhenomena.AR)
        self.assertLessEqual(diff_hours(events[2].time, self.data.timescale.utc(647, 9, 17)), 24)

        self.assertEqual(events[3].type, OuterPlanetPhenomena.ST)

        self.assertEqual(events[4].type, OuterPlanetPhenomena.LA)
        self.assertLessEqual(diff_hours(events[4].time, self.data.timescale.utc(648, 7, 15)), 24)

    def test_saturn(self):
        start = self.data.timescale.utc(1000, 6, 7)
        end = self.data.timescale.utc(1001, 5, 15)
        saturn = self.data.get_body("Saturn")
        events = outer_planet_events(self.data, saturn, start, end, OuterPlanetArcusVisionis.saturn())

        self.assertEqual(events[0].type, OuterPlanetPhenomena.FA)
        self.assertLessEqual(diff_hours(events[0].time, self.data.timescale.utc(1000, 6, 8)), 24)

        self.assertEqual(events[1].type, OuterPlanetPhenomena.ST)

        self.assertEqual(events[2].type, OuterPlanetPhenomena.AR)
        self.assertLessEqual(diff_hours(events[2].time, self.data.timescale.utc(1000, 11, 11)), 24)

        self.assertEqual(events[3].type, OuterPlanetPhenomena.ST)

        self.assertEqual(events[4].type, OuterPlanetPhenomena.LA)
        self.assertLessEqual(diff_hours(events[4].time, self.data.timescale.utc(1001, 5, 14)), 24)

    def test_jupiter(self):
        start = self.data.timescale.utc(1501, 4, 15)
        end = self.data.timescale.utc(1502, 4, 19)
        jupiter = self.data.get_body("Jupiter")
        events = outer_planet_events(self.data, jupiter, start, end, OuterPlanetArcusVisionis.jupiter())

        self.assertEqual(events[0].type, OuterPlanetPhenomena.FA)
        self.assertLessEqual(diff_hours(events[0].time, self.data.timescale.utc(1501, 4, 16)), 24)

        self.assertEqual(events[1].type, OuterPlanetPhenomena.ST)

        self.assertEqual(events[2].type, OuterPlanetPhenomena.AR)
        self.assertLessEqual(diff_hours(events[2].time, self.data.timescale.utc(1501, 10, 5)), 24)

        self.assertEqual(events[3].type, OuterPlanetPhenomena.ST)

        self.assertEqual(events[4].type, OuterPlanetPhenomena.LA)
        self.assertLessEqual(diff_hours(events[4].time, self.data.timescale.utc(1502, 4, 18)), 24)


