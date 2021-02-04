from skyfield import eclipselib
from skyfield.timelib import Time

from data import AstroData
from util import TimeValue


def lunar_eclipses_in_range(data: AstroData, start: Time, end: Time):
    t, y, details = eclipselib.lunar_eclipses(start, end, data.ephemeris)
    for ti, yi in zip(t, y):
        print(TimeValue(ti.tt).string(data.timescale),
              'y={}'.format(yi),
              eclipselib.LUNAR_ECLIPSES[yi])

