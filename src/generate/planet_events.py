from collections import namedtuple
from enum import unique, Enum
from typing import *

from skyfield import almanac
from skyfield.timelib import Time
from skyfield.units import Angle

from constants import InnerPlanetArcusVisionis, OuterPlanetArcusVisionis, Planet
from data import AstroData, SUN, EARTH
from util import same_sign, change_in_longitude
from generate import OPTIONAL_PROGRESS


@unique
class InnerPlanetPhenomena(Enum):
    EF = "evening_first"  # Appear in the west
    ES = "evening_station"  # Stationary in the west
    EL = "evening_last"  # Set in the west
    MF = "morning_first"  # Appear in the east
    MS = "morning_station"  # Stationary in the east
    ML = "morning_last"  # Set in the east


@unique
class OuterPlanetPhenomena(Enum):
    FA = "first_appearance"  # To appear
    AR = "acronychal_rising"  # To rise to daylight
    LA = "last_appearance"  # To set
    ST = "stationary"  # Either stationary point


SynodicEvent = namedtuple('SynodicEvent', 'time type')


def _apparent_altitude_of_sun(data: AstroData, t0: Time) -> Angle:
    sun = data.get_body(SUN)
    apparent = data.get_babylon().at(t0).observe(sun).apparent()
    alt, az, distance = apparent.altaz()
    return alt


def planet_events(data: AstroData, planet: Planet, t0: Time, t1: Time, progress: OPTIONAL_PROGRESS = None
                  ) -> List[SynodicEvent]:
    if planet.is_inner:
        return __inner_planet_events(data, data.get_body(planet.name), t0, t1, planet.arcus_visionis, progress)
    else:
        return __outer_planet_events(data, data.get_body(planet.name), t0, t1, planet.arcus_visionis, progress)



def __inner_planet_events(data: AstroData, body: str, t0: Time, t1: Time, ac: InnerPlanetArcusVisionis,
                          progress: OPTIONAL_PROGRESS = None) -> List[SynodicEvent]:
    """
    Returns a list of synodic events for an inner planet
    Evening/Morning Last is the night of last visibility (not first invisible)
    Note stations are not precise, but at the time of nearest/rise set
    """
    assert t0.tt < t1.tt
    if progress is not None:
        progress(0)
    f = almanac.risings_and_settings(data.ephemeris, body, data.babylon_topos)
    times, types = almanac.find_discrete(data.timescale.tt_jd(t0.tt - 2), data.timescale.tt_jd(t1.tt + 2), f)

    zipped = list(zip(times, types))
    events = []  # type: List[SynodicEvent]

    morning_rise = None
    morning_set = None
    evening_rise = None
    evening_set = None
    yesterday_set = None
    yesterday_rise = None
    previous_eclon = None
    previous_eclon_change = None

    for idx, (time, planet_rise) in enumerate(zipped):
        solar_alt = _apparent_altitude_of_sun(data, time).degrees

        # https://astronomy.stackexchange.com/a/18833/34119
        # retrograde motion of a planet as seen from Earth means that its ecliptic longitude is decreasing
        _, eclon, _ = data.get_body(EARTH).at(time).observe(body).ecliptic_latlon()
        if previous_eclon is not None:
            change = change_in_longitude(previous_eclon, eclon.degrees)
            if previous_eclon_change is not None and not same_sign(previous_eclon_change, change):
                if change < 0:
                    events.append(SynodicEvent(time, InnerPlanetPhenomena.ES))
                else:
                    events.append(SynodicEvent(time, InnerPlanetPhenomena.MS))
            previous_eclon_change = change
        previous_eclon = eclon.degrees

        if planet_rise:

            if solar_alt > -ac.mf:
                morning_rise = False

            if solar_alt < -ac.mf:
                if morning_rise is False:
                    events.append(SynodicEvent(time, InnerPlanetPhenomena.MF))
                morning_rise = True

            # Sun below horizon therefore visible at time of rise
            if solar_alt < -ac.ml:
                evening_rise = True

            # Sun is close/above horizon therefore invisible at time of rise
            if solar_alt > -ac.ml:
                if evening_rise is True:
                    events.append(SynodicEvent(yesterday_rise, InnerPlanetPhenomena.ML))
                evening_rise = False

            yesterday_rise = time

        else: # planet set

            if solar_alt > -ac.ef:
                morning_set = False

            if solar_alt < -ac.ef:
                if morning_set is False:
                    events.append(SynodicEvent(time, InnerPlanetPhenomena.EF))
                morning_set = True

            if solar_alt < -ac.el:
                evening_set = True

            if solar_alt > -ac.el:
                if evening_set is True:
                    events.append(SynodicEvent(yesterday_set, InnerPlanetPhenomena.EL))
                evening_set = False

            yesterday_set = time

        if progress is not None:
            progress(idx / len(zipped))

    events = list(filter(lambda x: t0.tt <= x.time.tt <= t1.tt, events))
    return events


def __outer_planet_events(data: AstroData, body: str, t0: Time, t1: Time, ac: OuterPlanetArcusVisionis,
                          progress: OPTIONAL_PROGRESS = None) -> List[SynodicEvent]:
    """
    Returns a list of synodic events for an outer planet
    Note stations are not precise, but at the time of nearest/rise set
    """
    assert t0.tt < t1.tt
    if progress is not None:
        progress(0)
    f = almanac.risings_and_settings(data.ephemeris, body, data.babylon_topos)
    times, types = almanac.find_discrete(data.timescale.tt_jd(t0.tt - 2), data.timescale.tt_jd(t1.tt + 2), f)

    zipped = list(zip(times, types))
    events = []  # type: List[SynodicEvent]

    morning_rise = None
    evening_set = None
    evening_rise = None
    yesterday_set = None
    yesterday_rise = None
    previous_eclon = None
    previous_eclon_change = None

    for idx, (time, planet_rise) in enumerate(zipped):
        solar_alt = _apparent_altitude_of_sun(data, time).degrees

        # https://astronomy.stackexchange.com/a/18833/34119
        # retrograde motion of a planet as seen from Earth means that its ecliptic longitude is decreasing
        _, eclon, _ = data.get_body(EARTH).at(time).observe(body).ecliptic_latlon()
        if previous_eclon is not None:
            change = change_in_longitude(previous_eclon, eclon.degrees)
            if previous_eclon_change is not None and not same_sign(previous_eclon_change, change):
                events.append(SynodicEvent(time, OuterPlanetPhenomena.ST))
            previous_eclon_change = change
        previous_eclon = eclon.degrees

        if planet_rise:

            if solar_alt > -ac.hr:
                morning_rise = False

            if solar_alt < -ac.hr:
                if morning_rise is False:
                    events.append(SynodicEvent(time, OuterPlanetPhenomena.FA))
                morning_rise = True

            # Sun below horizon therefore visible at time of rise
            if solar_alt < -ac.ar:
                evening_rise = True

            # Sun is close/above horizon therefore invisible at time of rise
            if solar_alt > -ac.ar:
                if evening_rise is True:
                    events.append(SynodicEvent(yesterday_rise, OuterPlanetPhenomena.AR))
                evening_rise = False

            yesterday_rise = time

        else: # planet set

            if solar_alt < -ac.hs:
                evening_set = True

            if solar_alt > -ac.hs:
                if evening_set is True:
                    events.append(SynodicEvent(yesterday_set, OuterPlanetPhenomena.LA))
                evening_set = False

            yesterday_set = time

        if progress is not None:
            progress(idx / len(zipped))

    events = list(filter(lambda x: t0.tt <= x.time.tt <= t1.tt, events))
    return events

