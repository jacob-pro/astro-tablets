import numpy as np
from matplotlib import pyplot as plt

from query.lunar_eclipse_query import LunarEclipseQuery, FirstContactRelative, FirstContactTime, CompositePhaseTiming
from util import diff_time_degrees_signed


def plot_eclipse_time_of_day_score(dest: str):
    eclipse = {'sunrise': 1458133.8958227257, 'partial_eclipse_begin': 1458133.9258227257}
    actual = diff_time_degrees_signed(eclipse['partial_eclipse_begin'], eclipse['sunrise'])
    xs = np.arange(-15, 25, 0.01)
    ys = list(map(lambda x: LunarEclipseQuery.eclipse_time_of_day_score(eclipse, FirstContactTime(x,
                                                                                                  FirstContactRelative.AFTER_SUNRISE)),
                  xs))

    f, ax1 = plt.subplots()
    ax1.set_xlabel('Observed Time After Sunrise (UŠ)')
    ax1.set_ylabel('Score')
    ax1.plot(xs, ys)
    ax1.axvline(x=actual, color='r', label="Correct Time")
    ax1.legend()

    plt.savefig(dest)


def plot_eclipse_phase_length_score(dest: str):
    eclipse = {'sum_us': 62.75}
    xs = np.arange(40, 80, 0.01)
    ys = list(map(lambda x: LunarEclipseQuery.eclipse_phase_length_score(eclipse, CompositePhaseTiming(x)), xs))

    f, ax1 = plt.subplots()
    ax1.set_xlabel('Observed Eclipse Total Length (UŠ)')
    ax1.set_ylabel('Score')
    ax1.plot(xs, ys)
    ax1.axvline(x=eclipse['sum_us'], color='r', label="Correct Time")
    ax1.legend()

    plt.savefig(dest)
