from abc import ABC
from typing import *

from angular_separation import angular_separation
from constants import OuterPlanetArcusVisionis, InnerPlanetArcusVisionis
from data import AstroData
from database import Database
from lunar_calendar import vernal_equinox, days_in_range
from planet_events import outer_planet_events, inner_planet_events


def get_tablet_class(tablet: str):
    if tablet == "bm32312":
        return BM32312
    raise ValueError("Unknown tablet name")


class Tablet(ABC):
    default_start = None
    default_end = None

    def __init__(self, data: AstroData, db: Database, start_year: Union[None, int], end_year: Union[None, int]):
        self.data = data
        self.db = db
        self.start_year = self.default_start if start_year is None else start_year
        self.end_year = self.default_end if end_year is None else end_year
        self.__validate__()

    def __validate__(self):
        assert self.start_year is not None
        assert self.end_year is not None
        if self.start_year > self.end_year:
            raise ValueError("Start year must be LEQ to end year")

    def calendar(self):
        print("Computing Lunar calendar...")
        for i in range(self.start_day.utc.year, self.end_day.utc.year + 1):
            self.db.save_equinox(vernal_equinox(self.data, i))
        days = days_in_range(self.data, self.start_day, self.end_day)
        self.db.save_days(days)
        return days

    def separation(self, of: str, to: str):
        print("Computing separation between {} and {}...".format(of, to))
        current = self.start_day
        b1 = self.data.get_body(of)
        b2 = self.data.get_body(to)
        while current.tt <= self.end_day.tt:
            res = angular_separation(self.data, b1, b2, current)
            self.db.save_separation(of, to, res, current)
            delta = 1.0 / 24.0
            current = self.data.timescale.tt_jd(current.tt + delta)

    def mercury(self):
        print("Computing Mercury visibility...")
        events = inner_planet_events(self.data, self.data.get_body("Mercury"), self.start_day, self.end_day,
                                     InnerPlanetArcusVisionis.mercury())
        self.db.save_synodic_events("Saturn", events)

    def mars(self):
        print("Computing Mars visibility...")
        events = outer_planet_events(self.data, self.data.get_body("Mars"), self.start_day, self.end_day,
                                     OuterPlanetArcusVisionis.mars())
        self.db.save_synodic_events("Mars", events)

    def saturn(self,):
        print("Computing Saturn visibility...")
        events = outer_planet_events(self.data, self.data.get_body("Saturn"), self.start_day, self.end_day,
                                     OuterPlanetArcusVisionis.saturn())
        self.db.save_synodic_events("Saturn", events)

    def compute(self):
        print("Computing {} for {} to {}".format(type(self).__name__, self.start_year, self.end_year))
        self.start_day = self.data.timescale.tt_jd(vernal_equinox(self.data, self.start_year).tt - 32)
        self.end_day = self.data.timescale.tt_jd(vernal_equinox(self.data, self.end_year + 1).tt + 32)
        self.days = self.calendar()


class BM32312(Tablet):
    default_start = -701
    default_end = -601

    def compute(self):
        super(BM32312, self).compute()
        # Mercury’s last appearance in the east behind Pisces
        # Mercury’s first appearance in the east in Pisces
        self.mercury()
        self.separation("Mercury", "58 Piscium")
        # Saturn’s last appearance behind Pisces
        self.saturn()
        self.separation("Saturn", "58 Piscium")
        # Mars became stationary in the area of the Lip of the Scorpion
        self.mars()
        # it came close to the bright star of the Scorpion’s head
        self.separation("Mars", "Antares")
        # Venus stood in the region of Aries, 10 fingers behind Mars
        self.separation("Venus", "Mars")
        # Mars was 1 finger to the left of the front? of Aries
        self.separation("Mars", "Nu Arietis")
