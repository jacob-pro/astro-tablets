from matplotlib import pyplot as plt

from generate.eclipse import *
from util import TimeValue


def plot_eclipse(data: AstroData, t0: Time, dest: str):
    times, types, details = eclipselib.lunar_eclipses(data.timescale.tt_jd(t0.tt - 1), data.timescale.tt_jd(t0.tt + 1),
                                                      data.ephemeris)

    assert len(times) == 1
    calc = EclipseTool(data)

    one_hour = 1.0 / 24
    one_min = 1.0 / 24 / 60
    start_time = data.timescale.tt_jd(times[0].tt - 4 * one_hour)
    end_time = data.timescale.tt_jd(times[0].tt + 4 * one_hour)
    moon_radius = details['moon_radius_radians'][0]

    points = []
    while start_time.tt < end_time.tt:
        angle = calc.angle_between(start_time)
        diff = times[0].tt - start_time.tt
        diff = diff * 1440 / 4
        points.append((diff, angle))
        start_time = data.timescale.tt_jd(start_time.tt + one_min)

    f, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [5, 1]})
    ax1.set_xlabel('Time (UŠ)')
    ax1.set_ylabel('Separation (° rad)')
    ax1.set_title(
        "{} (UTC+3) - {}".format(TimeValue(times[0].tt).string(data.timescale), eclipselib.LUNAR_ECLIPSES[types[0]]))

    ax1.plot(*zip(*points))
    ax1.axhline(y=details['penumbra_radius_radians'][0] + moon_radius, color='g', label="Penumbral")
    ax1.axhline(y=details['umbra_radius_radians'][0] + moon_radius, color='y', label="Partial")
    ax1.axhline(y=details['umbra_radius_radians'][0] - moon_radius, color='r', label="Total")
    ax1.legend()

    ax2.axis('off')
    again = lunar_eclipse_on_date(data, t0)
    phases = again.phases(TimeUnit.DEGREE)

    if again.type == "Total":
        t = "1:2 = {:.2f} UŠ   2:3 = {:.2f} UŠ   3:4 = {:.2f} UŠ   (1:4 = {:.2f} UŠ)" \
            .format(phases.onset, phases.maximal, phases.clearing, phases.sum)
        ax2.text(0, 0, t, fontsize=11)
    elif again.type == "Partial":
        t = "1:M = {:.2f} UŠ   M:4 = {:.2f} UŠ   (1:4 = {:.2f} UŠ)" \
            .format(phases.onset, phases.clearing, phases.sum)
        ax2.text(0, 0, t, fontsize=11)

    plt.savefig(dest)
