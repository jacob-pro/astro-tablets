import numpy as np
from matplotlib import pyplot as plt

from astro_tablets.constants import HALO, Precision
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.query.radius_query import WithinRadiusQuery


def plot_radius_score(dest: str):

    range = HALO * 3
    xs = np.arange(0, range, 0.01)
    f, ax1 = plt.subplots()
    ax1.set_xlabel("Angular Separation (°)")
    ax1.set_ylabel("Score")

    ys = list(
        map(
            lambda x: WithinRadiusQuery.calculate_score(
                radius=HALO,
                actual_angle=x,
                tablet_position=None,
                actual_position=EclipticPosition.BEHIND.value,
                precision=Precision.REGULAR,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Regular Precision", color="b")

    ys = list(
        map(
            lambda x: WithinRadiusQuery.calculate_score(
                radius=HALO,
                actual_angle=x,
                tablet_position=None,
                actual_position=EclipticPosition.BEHIND.value,
                precision=Precision.LOW,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Low Precision", color="g")

    ax1.axvline(x=HALO, color="r", label="Within Radius")
    ax1.legend()
    plt.savefig(dest)
