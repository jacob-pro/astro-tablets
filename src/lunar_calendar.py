from collections import namedtuple

from skyfield import almanac
from skyfield.timelib import Time, GREGORIAN_START, compute_calendar_date
from skyfield.units import Angle
from typing import *

from constants import LUNAR_VISIBILITY
from data import AstroData


def vernal_equinox(data: AstroData, year: int) -> Time:
    """
    For a given year find the date of the vernal equinox
    """
    before = data.timescale.julian_calendar_cutoff
    data.timescale.julian_calendar_cutoff = None
    t0 = data.timescale.utc(year, 3, 16)
    t1 = data.timescale.utc(year, 3, 26)
    data.timescale.julian_calendar_cutoff = before
    times, types = almanac.find_discrete(t0, t1, almanac.seasons(data.ephemeris))
    assert len(times) == 1
    assert almanac.SEASON_EVENTS[(types[0])] == 'Vernal Equinox'
    return times[0]


BabylonianDay = namedtuple('BabylonianDay', 'sunset sunrise')


def sunset_and_rise_for_date(data: AstroData, year: int, month: int, day: int) -> BabylonianDay:
    """
    For a given date find the time of sunset in Babylon
    """
    t0 = data.timescale.utc(year, month, day, 12)
    t1 = data.timescale.tt_jd(t0.tt + 1)
    times, types = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(data.ephemeris, data.babylon))
    assert len(times) == 2
    assert types[0] == 0  # 0 = Sunset
    assert types[1] == 1  # 1 = Sunrise
    return BabylonianDay(times[0], times[1])


def altitude_of_moon(data: AstroData, t0: Time) -> Angle:
    """
    For a given time find the altitude of the moon visible from Babylon
    """
    moon = data.ephemeris['moon']
    babylon = data.ephemeris['earth'] + data.babylon
    apparent = babylon.at(t0).observe(moon).apparent()
    alt, az, distance = apparent.altaz()
    return alt


class LunarMonth(object):

    def __init__(self):
        self.days = []  # type: List[BabylonianDay]
        self.nisan_candidate = False


def months_for_year(data: AstroData, year: int, intercalary: bool) -> List[LunarMonth]:
    """
    For a given year return a list of possible Lunar Months
    The earliest months will be possible candidates for Nisan (if they fall within 30 days of equinox)
    11 or 12 additional months will be computed following the last possible Nisan
    """
    equinox = vernal_equinox(data, year)
    position = data.timescale.tt_jd(int(equinox.tt - 31))
    end_nisan_search = data.timescale.tt_jd(int(equinox.tt + 30))
    non_nisan_month_count = 0
    prev_alt = float("inf")
    results = []  # type: List[LunarMonth]
    current_month = None
    non_nisan_limit = 12 if intercalary else 11
    while True:
        # Sunset for this day
        cal_date = compute_calendar_date(position.tt, GREGORIAN_START)
        day = sunset_and_rise_for_date(data, *cal_date)
        alt = altitude_of_moon(data, day.sunset)
        # If first visibility
        if alt.degrees >= LUNAR_VISIBILITY > prev_alt:
            if non_nisan_month_count >= non_nisan_limit:
                break
            x = LunarMonth()
            x.days.append(day)
            x.nisan_candidate = day.sunset.tt < end_nisan_search.tt
            if not x.nisan_candidate:
                non_nisan_month_count += 1
            results.append(x)
            current_month = x
        elif current_month is not None:
            current_month.days.append(day)
            pass
        # Next day
        position = data.timescale.tt_jd(int(position.tt + 1))
        prev_alt = alt.degrees
    assert 2 <= len(list(filter(lambda x: (x.nisan_candidate == True), results))) <= 3
    for x in results:
        assert 29 <= len(x.days) <= 30
    return results
