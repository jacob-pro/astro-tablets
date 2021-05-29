from generate.eclipse import *
from matplotlib import pyplot as plt

from util import TimeValue

data = AstroData()
t0 = data.timescale.ut1(-423, 9, 28)
times, types, details = eclipselib.lunar_eclipses(data.timescale.tt_jd(t0.tt - 1), data.timescale.tt_jd(t0.tt + 1), data.ephemeris)

assert len(times) == 1
print(TimeValue(times[0].tt).string(data.timescale))
print(eclipselib.LUNAR_ECLIPSES[types[0]])

calc = AngleBetweenCalculator(data)

one_hour = 1.0 / 24
one_min = 1.0 / 24 / 60
start_time = data.timescale.tt_jd(times[0].tt - 4 * one_hour)
end_time = data.timescale.tt_jd(times[0].tt + 4 * one_hour)
moon_radius = details['moon_radius_radians'][0]

points = []
while start_time.tt < end_time.tt:
    angle = calc.impl(start_time)
    diff = times[0].tt - start_time.tt
    diff = diff * 1440 / 4
    points.append((diff, angle))
    start_time = data.timescale.tt_jd(start_time.tt + one_min)

fig, ax = plt.subplots()
ax.set(xlabel='time', ylabel='separation (rad)')

plt.plot(*zip(*points))
plt.axhline(y=details['penumbra_radius_radians'][0] + moon_radius, color='g', label="penumbral")
plt.axhline(y=details['umbra_radius_radians'][0] + moon_radius, color='y', label="partial")
plt.axhline(y=details['umbra_radius_radians'][0] - moon_radius, color='r', label="total")

plt.legend()
plt.show()
