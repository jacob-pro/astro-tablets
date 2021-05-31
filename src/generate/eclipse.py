from dataclasses import dataclass
from enum import unique, Enum
from typing import *

from numpy.ma import arcsin
from skyfield import eclipselib
from skyfield.constants import ERAD
from skyfield.functions import length_of, angle_between
from skyfield.searchlib import find_discrete
from skyfield.timelib import Time

from data import AstroData
from generate.lunar_calendar import altitude_of_moon
from util import diff_mins


## https://github.com/skyfielders/python-skyfield/issues/545

class EclipseTool:

    def __init__(self, data: AstroData):
        sdict = dict(((s.center, s.target), s.spk_segment) for s in data.ephemeris.segments)
        self.sun = sdict[0, 10]
        self.earth_barycenter = sdict[0, 3]
        self.earth = sdict[3, 399]
        self.moon = sdict[3, 301]

    def angle_between(self, t: Time):
        jd, fr = t.whole, t.tdb_fraction
        b = self.earth_barycenter.compute(jd, fr)
        e = self.earth.compute(jd, fr)
        m = self.moon.compute(jd, fr)
        s = self.sun.compute(jd, fr)
        earth_to_sun = s - b - e
        moon_to_earth = e - m
        angle = angle_between(earth_to_sun, moon_to_earth)
        return angle

    def umbra_radius(self, t: Time) -> float:
        jd, fr = t.whole, t.tdb_fraction
        b = self.earth_barycenter.compute(jd, fr)
        e = self.earth.compute(jd, fr)
        m = self.moon.compute(jd, fr)
        s = self.sun.compute(jd, fr)
        earth_to_sun = s - b - e
        moon_to_earth = e - m
        solar_radius_km = 696340.0
        pi_m = ERAD / 1e3 / length_of(moon_to_earth)
        pi_s = ERAD / 1e3 / length_of(earth_to_sun)
        s_s = solar_radius_km / length_of(earth_to_sun)
        atmosphere_blur = 1.02
        pi_1 = 0.998340 * pi_m
        umbra_radius = atmosphere_blur * (pi_1 + pi_s - s_s)
        return umbra_radius

    def moon_radius(self, t: Time) -> float:
        jd, fr = t.whole, t.tdb_fraction
        e = self.earth.compute(jd, fr)
        m = self.moon.compute(jd, fr)
        moon_to_earth = e - m
        moon_radius_km = 1737.1
        moon_radius = arcsin(moon_radius_km / length_of(moon_to_earth))
        return moon_radius


@unique
class TimeUnit(Enum):
    MINUTE = 0
    DEGREE = 1


@dataclass
class EclipsePhases:
    onset: float
    maximal: float
    clearing: float
    sum: float
    unit: TimeUnit


class Eclipse:

    def __init__(self,
                 data: AstroData,
                 time: Time,
                 type: int,
                 closest_approach_radians: float,
                 moon_radius_radians: float,
                 penumbra_radius_radians: float,
                 umbra_radius_radians: float):
        self.data = data
        self.closest_approach_time = time
        self.type = eclipselib.LUNAR_ECLIPSES[type]
        self.closest_approach_radians = closest_approach_radians
        self.moon_radius_radians = moon_radius_radians
        self.penumbra_radius_radians = penumbra_radius_radians
        self.umbra_radius_radians = umbra_radius_radians

        calc = EclipseTool(data)

        f = lambda t: calc.angle_between(t) < calc.umbra_radius(t) + calc.moon_radius(t)
        f.step_days = 0.01
        times, values = find_discrete(data.timescale.tt_jd(time.tt - 1), data.timescale.tt_jd(time.tt + 1), f)
        if self.type != 'Penumbral':
            assert len(times) == 2
            assert (values == [1, 0]).all()
            assert times[0].tt < time.tt
            assert times[1].tt > time.tt
            self.partial_eclipse_begin = times[0]
            self.partial_eclipse_end = times[1]

        f = lambda t: calc.angle_between(t) < calc.umbra_radius(t) - calc.moon_radius(t)
        f.step_days = 0.01
        times, values = find_discrete(data.timescale.tt_jd(time.tt - 0.5), data.timescale.tt_jd(time.tt + 0.5), f)
        if self.type == 'Total':
            assert len(times) == 2
            assert (values == [1, 0]).all()
            assert times[0].tt < time.tt
            assert times[1].tt > time.tt
            self.total_eclipse_begin = times[0]
            self.total_eclipse_end = times[1]

    def phases(self, unit=TimeUnit.MINUTE) -> EclipsePhases:
        phases = EclipsePhases(0, 0, 0, 0, unit)
        if self.type == 'Partial':
            phases.onset = diff_mins(self.partial_eclipse_begin, self.closest_approach_time)
            phases.clearing = diff_mins(self.closest_approach_time, self.partial_eclipse_end)
            phases.sum = diff_mins(self.partial_eclipse_begin, self.partial_eclipse_end)
        if self.type == 'Total':
            phases.onset = diff_mins(self.partial_eclipse_begin, self.total_eclipse_begin)
            phases.maximal = diff_mins(self.total_eclipse_begin, self.total_eclipse_end)
            phases.clearing = diff_mins(self.total_eclipse_end, self.partial_eclipse_end)
            phases.sum = diff_mins(self.partial_eclipse_begin, self.partial_eclipse_end)
        if unit == TimeUnit.MINUTE:
            pass
        elif unit == TimeUnit.DEGREE:
            phases.onset = phases.onset / 4.0
            phases.maximal = phases.maximal / 4.0
            phases.clearing = phases.clearing / 4.0
            phases.sum = phases.sum / 4.0
        else:
            raise RuntimeError("Invalid TimeUnit")
        return phases

    def visibility_in_babylon(self) -> bool:
        from constants import LUNAR_VISIBILITY
        if self.type == 'Penumbral':
            return False
        alt1 = altitude_of_moon(self.data, self.partial_eclipse_begin).degrees
        alt2 = altitude_of_moon(self.data, self.partial_eclipse_end).degrees
        if alt1 > LUNAR_VISIBILITY:
            return True
        if alt2 > LUNAR_VISIBILITY:
            return True
        return False


def lunar_eclipses_in_range(data: AstroData, start: Time, end: Time) -> List[Eclipse]:
    times, types, details = eclipselib.lunar_eclipses(start, end, data.ephemeris)
    list = []  # type: List[Eclipse]
    for idx, _ in enumerate(times):
        list.append(Eclipse(data=data,
                            time=times[idx],
                            type=types[idx],
                            closest_approach_radians=details['closest_approach_radians'][idx],
                            moon_radius_radians=details['moon_radius_radians'][idx],
                            penumbra_radius_radians=details['penumbra_radius_radians'][idx],
                            umbra_radius_radians=details['umbra_radius_radians'][idx]))
    return list


def lunar_eclipse_on_date(data: AstroData, t0: Time) -> Eclipse:
    search_start = data.timescale.tt_jd(t0.tt - 1.5)
    search_end = data.timescale.tt_jd(t0.tt + 1.5)
    eclipses = lunar_eclipses_in_range(data, search_start, search_end)
    assert len(eclipses) == 1
    return eclipses[0]
