import numpy as np
from matplotlib import pyplot as plt

from astro_tablets.constants import HALO
from astro_tablets.query.halo_query import HaloQuery


def plot_halo_score(dest: str):

    range = HALO * 3
    xs = np.arange(0, range, 0.01)
    ys = list(
        map(
            lambda x: HaloQuery.score(halo_size=HALO, actual_angle=x),
            xs,
        )
    )

    f, ax1 = plt.subplots()
    ax1.set_xlabel("Angular Separation from Moon (°)")
    ax1.set_ylabel("Score")
    ax1.plot(xs, ys)
    ax1.axvline(x=HALO, color="g", label="Within Halo")

    ax1.legend()

    plt.savefig(dest)
