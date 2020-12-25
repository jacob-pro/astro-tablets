import pathlib

from skyfield import almanac
from skyfield.iokit import Loader
from skyfield.timelib import GREGORIAN_START
from skyfield.toposlib import Topos

path = pathlib.Path(__file__).parent.parent.absolute() / 'skyfield-data'
load = Loader(path.as_posix())
ts = load.timescale()
ts.julian_calendar_cutoff = GREGORIAN_START
eph = load('de431t.bsp')
babylon = Topos("32.55 N", "44.42 E")

def altitude_of_sun(t0):
    b = eph['earth'] + babylon
    apparent = b.at(t0).observe(eph['sun']).apparent()
    alt, az, distance = apparent.altaz()
    return alt

def sunset_for_day(t0, expected):
    t1 = ts.tt_jd(t0.tt + 1)
    t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, babylon))
    for ti, yi in zip(t, y):
        if yi == 0:
            diff_mins = int(abs(ti.tt - expected.tt) * 60 * 24)
            print("Got {}, expected {}, diff mins {}, alt {:.2f}"
                  .format(ti.utc_iso(), expected.utc_iso(), diff_mins, altitude_of_sun(ti).degrees))

if __name__ == "__main__":
    sunset_for_day(ts.utc(2020, 6, 1), ts.utc(2020, 6, 1, 16, 5))
    sunset_for_day(ts.utc(1800, 6, 1), ts.utc(1800, 6, 1, 16, 4))
    sunset_for_day(ts.utc(1000, 6, 1), ts.utc(1000, 6, 1, 16, 5))
    sunset_for_day(ts.utc(200, 6, 1), ts.utc(200, 6, 1, 16, 0))
    sunset_for_day(ts.utc(-400, 6, 1), ts.utc(-400, 6, 1, 15, 56))
    sunset_for_day(ts.utc(-800, 6, 1), ts.utc(-800, 6, 1, 15, 53))



