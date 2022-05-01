import numpy as np
from matplotlib import pyplot as plt

from astro_tablets.constants import HIGH_TIME_TOLERANCE, REGULAR_TIME_TOLERANCE
from astro_tablets.query.lunar_eclipse_query import (
    CompositePhaseTiming,
    FirstContactRelative,
    FirstContactTime,
    LunarEclipseQuery,
)
from astro_tablets.util import diff_time_degrees_signed


def plot_eclipse_time_of_day_score(dest: str):
    eclipse = {
        "sunrise": 1458133.8958227257,
        "partial_eclipse_begin": 1458133.9258227257,
    }
    actual = diff_time_degrees_signed(
        eclipse["partial_eclipse_begin"], eclipse["sunrise"]
    )

    f, ax1 = plt.subplots()
    ax1.set_xlabel("Observed Time After Sunrise (UŠ)")
    ax1.set_ylabel("Score")

    xs = np.arange(-15, 25, 0.01)
    ys = list(
        map(
            lambda x: LunarEclipseQuery.eclipse_time_of_day_score(
                eclipse,
                FirstContactTime(x, FirstContactRelative.AFTER_SUNRISE),
                REGULAR_TIME_TOLERANCE,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Regular (λ = {})".format(REGULAR_TIME_TOLERANCE), color="g")

    xs = np.arange(-15, 25, 0.01)
    ys = list(
        map(
            lambda x: LunarEclipseQuery.eclipse_time_of_day_score(
                eclipse,
                FirstContactTime(x, FirstContactRelative.AFTER_SUNRISE),
                HIGH_TIME_TOLERANCE,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="High (λ = {})".format(HIGH_TIME_TOLERANCE), color="b")

    ax1.axvline(x=actual, color="r", label="Correct Time")
    ax1.legend()

    plt.savefig(dest)


def plot_eclipse_phase_length_score(dest: str):
    eclipse = {"sum_us": 62.75}
    xs = np.arange(40, 80, 0.01)
    ys = list(
        map(
            lambda x: LunarEclipseQuery.eclipse_phase_length_score(
                eclipse, CompositePhaseTiming(x)
            ),
            xs,
        )
    )

    f, ax1 = plt.subplots()
    ax1.set_xlabel("Observed Eclipse Total Length (UŠ)")
    ax1.set_ylabel("Score")
    ax1.plot(xs, ys)
    ax1.axvline(x=eclipse["sum_us"], color="r", label="Correct Time")
    ax1.legend()

    plt.savefig(dest)
