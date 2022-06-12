import numpy as np
from matplotlib import pyplot as plt

from astro_tablets.constants import Confidence
from astro_tablets.query.database import LunarEclipse
from astro_tablets.query.lunar_eclipse_query import (
    CompositePhaseTiming,
    FirstContactRelative,
    FirstContactTime,
    LunarEclipseQuery,
)


def plot_eclipse_time_of_day_score(dest: str):
    first_contact = FirstContactTime(11, FirstContactRelative.AFTER_SUNRISE)

    f, ax1 = plt.subplots()
    ax1.set_xlabel("Observed Time After Sunrise (UŠ)")
    ax1.set_ylabel("Score")

    xs = np.arange(-15, 25, 0.01)
    ys = list(
        map(
            lambda x: LunarEclipseQuery.eclipse_time_of_day_score(
                LunarEclipse(
                    sunrise=0,
                    partial_eclipse_begin=x / 360,
                    e_type="",
                    closest_approach_time=0,
                    onset_us=0,
                    maximal_us=0,
                    clearing_us=0,
                    sum_us=0,
                    visible=False,
                    angle=0,
                    position=None,
                    sunset=0,
                ),
                first_contact,
                Confidence.REGULAR,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Regular Confidence", color="b")

    ys = list(
        map(
            lambda x: LunarEclipseQuery.eclipse_time_of_day_score(
                LunarEclipse(
                    sunrise=0,
                    partial_eclipse_begin=x / 360,
                    e_type="",
                    closest_approach_time=0,
                    onset_us=0,
                    maximal_us=0,
                    clearing_us=0,
                    sum_us=0,
                    visible=False,
                    angle=0,
                    position=None,
                    sunset=0,
                ),
                first_contact,
                Confidence.LOW,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Low Confidence", color="g")

    ax1.axvline(x=first_contact.time_degrees, color="r", label="Expected Time")
    ax1.legend()

    plt.savefig(dest)


def plot_eclipse_phase_length_score(dest: str):
    val = 62.75
    xs = np.arange(val - 30, val + 30, 0.01)
    ys = list(
        map(
            lambda x: LunarEclipseQuery.eclipse_phase_length_score(
                LunarEclipse(
                    sunrise=0,
                    partial_eclipse_begin=0,
                    e_type="",
                    closest_approach_time=0,
                    onset_us=0,
                    maximal_us=0,
                    clearing_us=0,
                    sum_us=x,
                    visible=False,
                    angle=0,
                    position=None,
                    sunset=0,
                ),
                CompositePhaseTiming(val),
            ),
            xs,
        )
    )

    f, ax1 = plt.subplots()
    ax1.set_xlabel("Observed Eclipse Total Length (UŠ)")
    ax1.set_ylabel("Score")
    ax1.plot(xs, ys)
    ax1.axvline(x=val, color="r", label="Expected Length")
    ax1.legend()

    plt.savefig(dest)
