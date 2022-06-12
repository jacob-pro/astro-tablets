import numpy as np
from matplotlib import pyplot as plt

from astro_tablets.constants import MARS, MERCURY, SATURN
from astro_tablets.query.planetary_event_query import PlanetaryEventQuery


def plot_planetary_event_score(dest: str):

    range = 30
    xs = np.arange(-range, range, range / 100)
    f, ax1 = plt.subplots()
    ax1.set_xlabel("Days from Event")
    ax1.set_ylabel("Score")

    ys = list(
        map(
            lambda x: PlanetaryEventQuery.calculate_score(
                time=x,
                expected_start=0,
                expected_end=0,
                event_frequency=MARS.event_frequency,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Mars", color="r")

    ys = list(
        map(
            lambda x: PlanetaryEventQuery.calculate_score(
                time=x,
                expected_start=0,
                expected_end=0,
                event_frequency=MERCURY.event_frequency,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Mercury", color="g")

    ys = list(
        map(
            lambda x: PlanetaryEventQuery.calculate_score(
                time=x,
                expected_start=0,
                expected_end=0,
                event_frequency=SATURN.event_frequency,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Saturn", color="y")

    ax1.axvline(x=0, color="b", label="Event")

    ax1.legend()

    plt.savefig(dest)
