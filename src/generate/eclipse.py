from dataclasses import dataclass
from typing import *

from skyfield import eclipselib
from skyfield.searchlib import find_discrete
from skyfield.timelib import Time

from data import AstroData


## https://github.com/skyfielders/python-skyfield/issues/545


class AngleBetweenCalculator:

    def __init__(self, data: AstroData):
        sdict = dict(((s.center, s.target), s.spk_segment) for s in data.ephemeris.segments)
        self.sun = sdict[0, 10]
        self.earth_barycenter = sdict[0, 3]
        self.earth = sdict[3, 399]
        self.moon = sdict[3, 301]

    def impl(self, t: Time):
        from skyfield.functions import angle_between

        jd, fr = t.whole, t.tdb_fraction
        b = self.earth_barycenter.compute(jd, fr)
        e = self.earth.compute(jd, fr)
        m = self.moon.compute(jd, fr)
        s = self.sun.compute(jd, fr)

        earth_to_sun = s - b - e
        moon_to_earth = e - m

        angle = angle_between(earth_to_sun, moon_to_earth)
        return angle


@dataclass
class SkyfieldEclipse:
    time: Time
    type: str
    closest_approach_radians: float
    moon_radius_radians: float
    penumbra_radius_radians: float
    umbra_radius_radians: float

    def upgrade(self, data: AstroData):
        sdict = dict(((s.center, s.target), s.spk_segment) for s in data.ephemeris.segments)
        sun = sdict[0, 10]
        earth_barycenter = sdict[0, 3]
        earth = sdict[3, 399]
        moon = sdict[3, 301]

        def f(t):
            from skyfield.functions import angle_between

            jd, fr = t.whole, t.tdb_fraction
            b = earth_barycenter.compute(jd, fr)
            e = earth.compute(jd, fr)
            m = moon.compute(jd, fr)
            s = sun.compute(jd, fr)

            earth_to_sun = s - b - e
            moon_to_earth = e - m

            angle = angle_between(earth_to_sun, moon_to_earth)
            return angle < self.penumbra_radius_radians + self.moon_radius_radians

        f.step_days = 0.01
        times, values = find_discrete(data.timescale.tt_jd(self.time.tt - 1), data.timescale.tt_jd(self.time.tt + 1), f)
        assert len(times) == 2
        assert (values == [1, 0]).all()
        assert times[0].tt < self.time.tt
        assert times[1].tt > self.time.tt

        return Eclipse(start_time=times[0], end_time=times[1], base=self)


@dataclass
class Eclipse:
    start_time: Time
    end_time: Time
    base: SkyfieldEclipse


def lunar_eclipses_in_range(data: AstroData, start: Time, end: Time) -> List[Eclipse]:
    times, types, details = eclipselib.lunar_eclipses(start, end, data.ephemeris)
    bases = []  # type: List[SkyfieldEclipse]
    for idx, _ in enumerate(times):
        bases.append(SkyfieldEclipse(time=times[idx],
                                     type=eclipselib.LUNAR_ECLIPSES[types[idx]],
                                     closest_approach_radians=details['closest_approach_radians'][idx],
                                     moon_radius_radians=details['moon_radius_radians'][idx],
                                     penumbra_radius_radians=details['penumbra_radius_radians'][idx],
                                     umbra_radius_radians=details['umbra_radius_radians'][idx]))
    return list(map(lambda x: x.upgrade(data), bases))
