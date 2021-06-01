import numpy as np
from matplotlib import pyplot as plt

from generate.angular_separation import EclipticPosition
from query.angular_separation_query import AngularSeparationQuery


def plot_separation_score(angle: float, tolerance: float, dest: str):

    range = (angle + tolerance) * 1.5
    xs = np.arange(0, range, 0.01)
    ys = list(map(lambda x: AngularSeparationQuery.separation_score(target_angle=angle, tolerance=tolerance,
                                                                    target_position=None, actual=x,
                                                                    actual_position=EclipticPosition.BEHIND.value, ),
                  xs))

    f, ax1 = plt.subplots()
    ax1.set_xlabel('Angular Separation°')
    ax1.set_ylabel('Score')
    ax1.plot(xs, ys)
    if angle != 0:
        ax1.axvline(x=angle, color='r', label="Target Angle")

    ax1.axvline(x=angle+tolerance, color='g', label="Upper Bound")
    if angle - tolerance > 0:
        ax1.axvline(x=angle - tolerance, color='b', label="Lower Bound")

    ax1.legend()

    plt.savefig(dest)
