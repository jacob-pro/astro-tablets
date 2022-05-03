import numpy as np
from matplotlib import pyplot as plt

from astro_tablets.constants import Precision
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.query.angular_separation_query import AngularSeparationQuery


def plot_separation_score(angle: float, dest: str):

    range = angle * 4
    xs = np.arange(0, range, angle / 1000)
    f, ax1 = plt.subplots()
    ax1.set_xlabel("Angular Separation (°)")
    ax1.set_ylabel("Score")

    ys = list(
        map(
            lambda x: AngularSeparationQuery.score(
                tablet_angle=angle,
                tablet_position=None,
                actual=x,
                actual_position=EclipticPosition.BEHIND.value,
                precision=Precision.REGULAR,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Regular Precision", color="b")

    ys = list(
        map(
            lambda x: AngularSeparationQuery.score(
                tablet_angle=angle,
                tablet_position=None,
                actual=x,
                actual_position=EclipticPosition.BEHIND.value,
                precision=Precision.LOW,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Low Precision", color="g")

    ax1.axvline(x=angle, color="r", label="Expected Separation")

    ax1.legend()

    plt.savefig(dest)
