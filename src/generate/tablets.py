import sys
import time
from abc import ABC

from data import *
from generate.angular_separation import angular_separation
from generate.database import Database
from generate.lunar_calendar import vernal_equinox, days_in_range
from generate.planet_events import planet_events


def get_tablet_class(tablet: str):
    tablet = tablet.lower()
    if tablet == "bm32312":
        return BM32312
    if tablet == "bm41222":
        return BM41222
    if tablet == "bm76738":
        return BM76738
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
        for i in range(self.start_day.utc.year, self.end_day.utc.year + 1):
            self.db.save_equinox(vernal_equinox(self.data, i))
        days = days_in_range(self.data, self.start_day, self.end_day,
                             lambda x: self.print_progress("Computing Lunar calendar", x))
        self.db.save_days(days)
        print("")
        return days

    def separation_during_night(self, of: Union[str, Planet], to: Union[str, Planet], intervals: int = 4):
        if type(of) == Planet:
            of = of.name
        if type(to) == Planet:
            to = to.name
        b1 = self.data.get_body(of)
        b2 = self.data.get_body(to)
        for idx, day in enumerate(self.days):
            night_len = day.sunrise.tt - day.sunset.tt
            for i in range(intervals):
                time = self.data.timescale.tt_jd(day.sunset.tt + (i/intervals * night_len))
                res = angular_separation(self.data, b1, b2, time)
                self.db.save_separation(of, to, res, time)
            self.print_progress("Computing separation between {} and {}".format(of, to), idx / len(self.days))
        print("")

    def planet_events(self, planet: Planet):
        events = planet_events(self.data, planet, self.start_day, self.end_day,
                               lambda x: self.print_progress("Computing {} visibility".format(planet.name), x))
        self.db.save_synodic_events(planet.name, events)
        print("")

    def compute(self):
        self.start_time = time.time()
        print("Computing {} for {} to {}".format(type(self).__name__, self.start_year, self.end_year))
        self.start_day = self.data.timescale.tt_jd(vernal_equinox(self.data, self.start_year).tt - 32)
        self.end_day = self.data.timescale.tt_jd(vernal_equinox(self.data, self.end_year + 1).tt + 64)
        self.days = self.calendar()

    def post_compute(self):
        self.db.save_info(type(self).__name__, self.start_year, self.end_year)
        elapsed = time.time() - self.start_time
        print("Completed in", time.strftime("%H:%M:%S", time.gmtime(elapsed)))

    @staticmethod
    def print_progress(prefix: str, progress: float):
        if progress > 0.99:
            progress = 1
        sys.stdout.write("\r{} {:05.2f}%".format(prefix, progress * 100))
        sys.stdout.flush()


class BM32312(Tablet):
    default_start = -701
    default_end = -601

    def compute(self):
        super(BM32312, self).compute()
        # Mercury’s last appearance in the east behind Pisces
        # Mercury’s first appearance in the east in Pisces
        self.planet_events(MERCURY)
        self.separation_during_night(MERCURY, PISCES.central_star)
        # Saturn’s last appearance behind Pisces
        self.planet_events(SATURN)
        self.separation_during_night(SATURN, PISCES.central_star)
        # Mars became stationary in the area of the Lip of the Scorpion
        self.planet_events(MARS)
        # it came close to the bright star of the Scorpion’s head
        self.separation_during_night(MARS, ANTARES)
        # Venus stood in the region of Aries, 10 fingers behind Mars
        self.separation_during_night(VENUS, MARS)
        # Mars was 1 finger to the left of the front? of Aries
        self.separation_during_night(MARS, ARIES.central_star)


class BM41222(Tablet):
    default_start = -726
    default_end = -576

    def compute(self):
        super(BM41222, self).compute()
        # Mercury's first appearance in the west
        self.planet_events(MERCURY)
        # in the area of the Swallow = Pisces
        self.separation_during_night(MERCURY, PISCES.central_star)
        # mars was in [the area?] of the Old Man = Perseus
        self.separation_during_night(MARS, PERSEUS.central_star)
        # to the right of Mercury
        self.separation_during_night(MARS, MERCURY)
        # Mercury stood for ⅔ cubit above? Mars
        # Mercury was in the back of Mars?
        # Mercury stood 1 cubit 4 fingers behind Mars.
        # Mercury was balanced 6 fingers above Mars.
        self.separation_during_night(MERCURY, MARS)
        # Mercury in the area of the Lion
        self.separation_during_night(MERCURY, LEO.central_star)
        #  Mercury, in the area of Pleiades
        self.separation_during_night(MERCURY, ALCYONE)
        # Mars was with Pleiades
        self.separation_during_night(MARS, ALCYONE)
        # Mars was ⅔ cubit above the Chariot [....] = Auriga.
        self.separation_during_night(MARS, AURIGA.central_star)
        # Mars was [....] above α Leonis.
        self.separation_during_night(MARS, REGULUS)
        # with β Virginis
        self.separation_during_night(MARS, BETA_VIRGINIS)


class BM76738(Tablet):
    default_start = -697
    default_end = -583

    def compute(self):
        super(BM76738, self).compute()
        self.planet_events(SATURN)
        self.separation_during_night(SATURN, EPSILON_LEONIS)
        self.separation_during_night(SATURN, REGULUS)
        self.separation_during_night(SATURN, LEO.central_star)
        self.separation_during_night(SATURN, BETA_VIRGINIS)
        self.separation_during_night(SATURN, VIRGO.central_star)
        self.separation_during_night(SATURN, LIBRA.central_star)
        self.separation_during_night(SATURN, ANTARES)
        self.separation_during_night(SATURN, SAGITTARIUS.central_star)
