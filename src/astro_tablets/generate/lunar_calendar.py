from dataclasses import dataclass
from typing import List, Tuple

from skyfield import almanac
from skyfield.timelib import GREGORIAN_START, Time, compute_calendar_date
from skyfield.units import Angle

from astro_tablets.constants import LUNAR_VISIBILITY
from astro_tablets.data import MOON, AstroData
from astro_tablets.util import PROGRESS_CALLBACK

VERNAL_EQUINOX = "vernal_equinox"


def vernal_equinox(data: AstroData, year: int) -> Time:
    """
    For a given year find the date of the vernal equinox
    """
    before = data.timescale.julian_calendar_cutoff
    data.timescale.julian_calendar_cutoff = None
    t0 = data.timescale.ut1(year, 3, 16)
    t1 = data.timescale.ut1(year, 3, 26)
    data.timescale.julian_calendar_cutoff = before
    times, types = almanac.find_discrete(t0, t1, almanac.seasons(data.ephemeris))
    assert len(times) == 1
    assert almanac.SEASON_EVENTS[(types[0])] == "Vernal Equinox"
    return times[0]


def sunset_and_rise_for_date(
    data: AstroData, year: int, month: int, day: int
) -> Tuple[Time, Time]:
    """
    For a given date find the time of sunset in Babylon
    """
    t0 = data.timescale.ut1(year, month, day, 12)
    t1 = data.timescale.tt_jd(t0.tt + 1)
    times, types = almanac.find_discrete(
        t0, t1, almanac.sunrise_sunset(data.ephemeris, data.babylon_topos)
    )
    assert len(times) == 2
    assert types[0] == 0  # 0 = Sunset
    assert types[1] == 1  # 1 = Sunrise
    return times[0], times[1]


def altitude_of_moon(data: AstroData, t0: Time) -> Angle:
    """
    For a given time find the altitude of the moon visible from Babylon
    """
    moon = data.get_body(MOON)
    apparent = data.get_babylon().at(t0).observe(moon).apparent()
    alt, az, distance = apparent.altaz()
    return alt


@dataclass
class BabylonianDay:
    sunset: Time
    sunrise: Time
    first_visibility: bool


def days_in_range(
    data: AstroData, start: Time, end: Time, progress: PROGRESS_CALLBACK = None
) -> List[BabylonianDay]:
    assert start.tt < end.tt
    position = data.timescale.tt_jd(start.tt - 2)
    end = data.timescale.tt_jd(end.tt + 1)
    prev_altitude = float("inf")
    results: List[BabylonianDay] = []

    while position.tt < end.tt:
        # Sunset for this day
        cal_date = compute_calendar_date(int(position.tt), GREGORIAN_START)
        ss = sunset_and_rise_for_date(data, *cal_date)
        alt = altitude_of_moon(data, ss[0])
        # If first visibility
        if prev_altitude < LUNAR_VISIBILITY <= alt.degrees:
            first_visibility = True
        else:
            first_visibility = False
        # Next day
        results.append(BabylonianDay(ss[0], ss[1], first_visibility))
        position = data.timescale.tt_jd(int(position.tt + 1))
        prev_altitude = alt.degrees
        if progress is not None:
            progress((position.tt - start.tt) / (end.tt - start.tt))

    results = list(
        filter(lambda x: x.sunset.tt >= start.tt and x.sunrise.tt <= end.tt, results)
    )
    if progress is not None:
        progress(1.0)
    return results
