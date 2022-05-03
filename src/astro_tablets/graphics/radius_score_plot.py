import numpy as np
from matplotlib import pyplot as plt

from astro_tablets.constants import HALO
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.query.radius_query import WithinRadiusQuery


def plot_radius_score(dest: str):

    range = HALO * 3
    xs = np.arange(0, range, 0.01)
    ys = list(
        map(
            lambda x: WithinRadiusQuery.score(
                radius=HALO,
                actual_angle=x,
                tablet_position=None,
                actual_position=EclipticPosition.BEHIND.value,
            ),
            xs,
        )
    )

    f, ax1 = plt.subplots()
    ax1.set_xlabel("Angular Separation (°)")
    ax1.set_ylabel("Score")
    ax1.plot(xs, ys)
    ax1.axvline(x=HALO, color="g", label="Within Radius")

    ax1.legend()

    plt.savefig(dest)
