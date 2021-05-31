import numpy as np
from matplotlib import pyplot as plt

from query.lunar_eclipse_query import LunarEclipseQuery, FirstContactRelative, FirstContactTime
from util import diff_time_degrees_signed


def plot_eclipse_timing_score(dest: str):
    eclipse = {'sunrise': 1458133.8958227257, 'partial_eclipse_begin': 1458133.9258227257}
    actual = diff_time_degrees_signed(eclipse['partial_eclipse_begin'], eclipse['sunrise'])
    print(actual)
    xs = np.arange(-15, 25, 0.01)
    ys = list(map(lambda x: LunarEclipseQuery.eclipse_timing_score(eclipse, FirstContactTime(x,
                                                                                             FirstContactRelative.AFTER_SUNRISE)),
                  xs))

    f, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [5, 1]})
    ax1.set_xlabel('Observed Time After Sunrise (UŠ)')
    ax1.set_ylabel('Score')
    ax1.plot(xs, ys)
    ax1.axvline(x=actual, color='r', label="Correct Time")

    ax2.axis('off')
    t = "The correct time was {:.2f} UŠ after sunrise, the closer to\n the correct time" \
        " then the closer the score will be to 1.0".format(actual)
    ax2.text(0, 0, t, fontsize=11)
    plt.savefig(dest)
