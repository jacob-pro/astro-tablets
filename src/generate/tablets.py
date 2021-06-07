import sys
import time
from abc import ABC

from data import *
from generate.angular_separation import angular_separation
from generate.database import Database
from generate.eclipse import lunar_eclipses_in_range
from generate.lunar_calendar import vernal_equinox, days_in_range
from generate.planet_events import planet_events
from generate.risings_settings import risings_and_settings


def get_tablet_class(tablet: str):
    tablet = tablet.lower()
    if tablet == "bm32312":
        return BM32312
    if tablet == "bm41222":
        return BM41222
    if tablet == "bm76738":
        return BM76738
    if tablet == "bm35115":
        return BM35115
    if tablet == "bm32234":
        return BM32234
    if tablet == "bm38462":
        return BM38462
    if tablet == "vat4956":
        return VAT4956
    if tablet == "bm33066":
        return BM33066
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

    def lunar_eclipses(self, position_bodies: List[str] = []):
        print("Computing lunar eclipses")
        eclipses = lunar_eclipses_in_range(self.data, self.start_day, self.end_day)
        self.db.save_lunar_eclipses(eclipses)
        for body in position_bodies:
            b1 = self.data.get_body(MOON)
            b2 = self.data.get_body(body)
            for idx, e in enumerate(eclipses):
                res = angular_separation(self.data, b1, b2, e.closest_approach_time)
                self.db.save_separation(MOON, body, res, e.closest_approach_time)
                self.print_progress("Computing separation between {} and {}".format(MOON, body), idx / len(eclipses))
            print("")
        return eclipses

    def risings_settings(self, body: str):
        print("Computing risings and settings for {}".format(body))
        rs = risings_and_settings(self.data, body, self.start_day, self.end_day)
        self.db.save_risings_settings(body, rs)

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


class BM35115(Tablet):
    default_start = -720
    default_end = -581

    def compute(self):
        super(BM35115, self).compute()
        # (Moon) behind α Scorpii [it was eclipsed.]
        self.lunar_eclipses([ANTARES])


class BM32234(Tablet):
    default_start = -640
    default_end = -490

    def compute(self):
        super(BM32234, self).compute()
        # in front of Libra it was eclipsed.
        # Behind the rump of Aries it was eclipsed.
        # in front of η Tauri it was eclipsed.
        self.lunar_eclipses([LIBRA.central_star, ARIES.central_star, ALCYONE])
        # Mars was 2 cubits in front of α Scorpii.
        self.separation_during_night(MARS, ANTARES)
        # Saturn rose in Capricorn
        self.separation_during_night(SATURN, CAPRICORNUS.central_star)


class BM38462(Tablet):
    default_start = -655
    default_end = -525

    def compute(self):
        super(BM38462, self).compute()
        self.lunar_eclipses()


class VAT4956(Tablet):
    default_start = -620
    default_end = -510

    def compute(self):
        super(VAT4956, self).compute()
        # Sîn (Moon) appeared behind the Bull of Heaven (Taurus)
        # the Bull of Heaven (Taurus),
        self.separation_during_night(MOON, TAURUS.central_star)
        # Kajjamānu (Saturn) was in front of the Swallow (Pisces)
        self.separation_during_night(SATURN, PISCES.central_star)
        # Sîn (Moon) stood 1 cubit in front of the Rear Foot of the Lion (β Virginis)
        self.separation_during_night(MOON, BETA_VIRGINIS)
        # Sagmegar (Jupiter) ‘rose to daylight’ (AR)
        self.planet_events(JUPITER)
        #  NA (sunrise to moonset) was 4.
        self.risings_settings(MOON)
        # Sîn (Moon) appeared below the Rear Bright Star of the Large Twins (β Geminorum)
        self.separation_during_night(MOON, BETA_GEMINORUM)
        # Ṣalbaṭānu (Mars) entered the Crab (Praesepe)
        self.separation_during_night(MARS, FORTY_TWO_CANCRI)
        # Šiḫṭu (Mercury) [rose] in the west behind the [Little] Twins [...] (Gemini)
        self.separation_during_night(MERCURY, GEMINI.central_star)
        self.planet_events(MERCURY)
        # Dilbat (Venus) was ‘balanced’ 1 cubit 4 fingers above the King (Regulus)
        self.separation_during_night(VENUS, REGULUS)
        # Sîn (Moon) appeared behind the Crab (Cancer)
        # and the Crab (Cancer) were inside {inside} the ‘fold’.
        self.separation_during_night(MOON, CANCER.central_star)
        # Ṣalba-ṭānu (Mars) and Šiḫṭu (Mercury) were 4 cubits in front of the K[ing ...] (Regulus)
        # Ṣalbaṭānu (Mars) was 2/3 of a cubit ˹above˺ [the King ...] (Regulus)
        self.separation_during_night(MARS, REGULUS)
        self.separation_during_night(MERCURY, REGULUS)
        # Šiḫṭu (Mercury) passed below Ṣalbaṭānu (Mars)
        self.separation_during_night(MARS, MERCURY)
        # Sagmegar (Jupiter) was above Lisi (Antares)
        self.separation_during_night(JUPITER, ANTARES)
        #  Dilbat (Venus) was in the west, opposite the Tail of the Li[on ...] (θ Leonis)
        self.separation_during_night(VENUS, THETA_LEONIS)
        # Sîn (Moon) passed towards the east 1 cubit ‹above/below› the Bright Star at the Tip of the Lion’s Foot. (Leo)
        # #  Sîn (Moon) was surrounded by a ‘fold’ (Halo); the Lion (Leo)
        self.separation_during_night(MOON, LEO.central_star)
        # Sîn (Moon) stood 2 1/2 cubits below the Northern Part of the Scales (β Librae)
        self.separation_during_night(MOON, BETA_LIBRAE)
        # Sîn (Moon) was ‘balanced’ 3 1/2 cubits above Lisi (Antares).
        self.separation_during_night(MOON, ANTARES)
        #  An eclipse of Sîn (Moon) which passed by
        self.lunar_eclipses()
        # Dilbat (Venus) was below the Middle Star of the Horn of the Goat [...] (β Capricorni)
        self.separation_during_night(VENUS, BETA_CAPRICORNI)
        # Sîn (Moon) appeared in the Swallow (Pisces)
        self.separation_during_night(MOON, PISCES.central_star)
        # Sagmegar (Jupiter) was behind the Elbow of Pabi[lsag by ... cubits ...] (Sagittarius)
        self.separation_during_night(JUPITER, SAGITTARIUS.central_star)
        # Dilbat (Venus) was ‘balanced’ 1/2 cubit below the Goat-Fish. (Capricorn)
        self.separation_during_night(VENUS, CAPRICORNUS.central_star)
        # Sîn (Moon) was surrounded by a ‘fold’ (Halo), the Bristle (Pleiades), ...,
        # the Chariot (Auriga) [stood within the ‘fold’ ...]
        # Sîn (Moon) was ‘balanced’ 4 cubits below the Stars (Pleiades).
        self.separation_during_night(MOON, ALCYONE)
        self.separation_during_night(MOON, AURIGA.central_star)
        # King (Regulus) was ‘balanced’ 1 cubit below Sîn (Moon)
        self.separation_during_night(REGULUS, MOON)
        #  Sîn (Moon) appeared behind the Hired Man (Aries)
        self.separation_during_night(MOON, ARIES.central_star)
        # was in front of the Band of the Swallow (Pisces), 1/2 cubit below Dilbat (Venus), Šiḫṭu (Mercury)
        # passing 8 fingers to the east, when it appeared it was bright and high. 1 U[Š ... Kajjamānu (Saturn)] was
        # ‘balanced’ 6 fingers above Šiḫṭu (Mercury) and 3 fingers below Dilbat (Venus)
        self.separation_during_night(VENUS, MERCURY)
        # Dilbat (Venus) and Šiḫṭu (Mercury) entered the Band of the Swallow (Pisces)
        self.separation_during_night(VENUS, PISCES.central_star)
        self.separation_during_night(MERCURY, PISCES.central_star)


class BM33066(Tablet):
    default_start = -590
    default_end = -460

    def compute(self):
        super(BM33066, self).compute()
        # Lunar Sixes
        self.risings_settings(MOON)
        # Synodic Phenomena
        self.planet_events(JUPITER)
        self.separation_during_night(JUPITER, VIRGO.central_star)
        self.separation_during_night(JUPITER, LIBRA.central_star)
        self.planet_events(VENUS)
        self.separation_during_night(VENUS, LEO.central_star)
        self.separation_during_night(VENUS, CANCER.central_star)
        self.separation_during_night(VENUS, PISCES.central_star)
        self.separation_during_night(VENUS, AURIGA.central_star)
        self.planet_events(SATURN)
        self.separation_during_night(SATURN, VIRGO.central_star)
        self.planet_events(MARS)
        self.separation_during_night(MARS, GEMINI.central_star)
        self.separation_during_night(MARS, LEO.central_star)
        self.separation_during_night(MARS, REGULUS)
        #  Year 7, month VII, the 1st, the moon became visible 3 cubits behind Mercury.
        self.separation_during_night(MOON, MERCURY)
        #  Month VI, the 24th, Venus was 1 +[x cubits?] above Mars.
        self.separation_during_night(VENUS, MARS)
        #  Month VII, the 23rd, last part of the night, Jupiter was 3 cubits above the moon.
        self.separation_during_night(JUPITER, MOON)
        #  Month VII, the 29th, last part of the night, Venus on the north side [came near?] 2 fingers to Ju[piter].
        self.separation_during_night(VENUS, JUPITER)
        #  Month VII, the 12th, Saturn was 1 cubit in front of Jupiter.
        self.separation_during_night(SATURN, JUPITER)
        #  Month VII, the 11th, Mars came near to Jupiter 2 fingers.
        self.separation_during_night(MARS, JUPITER)
        #  Month VIII, the 2nd, Saturn passed 8 fingers above Venus.
        self.separation_during_night(SATURN, VENUS)
        #  Month X, the 5th, Mercury was ½ cubit behind Venus.
        self.separation_during_night(MERCURY, VENUS)
        # Lunar Eclipses
        self.lunar_eclipses()
