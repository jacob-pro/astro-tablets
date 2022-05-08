import sys
from typing import Callable, Optional

from skyfield.timelib import Time, Timescale

PROGRESS_CALLBACK = Optional[Callable[[float], None]]


def diff_mins(t1: Time, t2: Time) -> float:
    jdiff = abs(t1 - t2)
    mins_in_day = 60 * 24
    return jdiff * mins_in_day


def diff_hours(t1: Time, t2: Time) -> float:
    jdiff = abs(t1 - t2)
    return jdiff * 24


def diff_time_degrees_signed(t1: float, t2: float) -> float:
    jdiff = t1 - t2
    degrees_in_day = 360
    return jdiff * degrees_in_day


def same_sign(num1, num2) -> bool:
    return (num1 >= 0 and num2 >= 0) or (num1 < 0 and num2 < 0)


def print_progress(prefix: str, progress: float):
    sys.stdout.write(f"\r{prefix}{progress * 100:05.2f}%")
    sys.stdout.flush()
    # Add a line break after reaching 100%
    if progress == 1:
        print("")


def change_in_longitude(old: float, new: float) -> float:
    """
    For longitudes that wraps around 360 degrees.
    Find the smallest signed difference
    """
    assert 0 <= old <= 360
    assert 0 <= new <= 360
    a = new - old
    b = (360 - old) + new if old > new else -old - (360 - new)
    if abs(a) < abs(b):
        return a
    else:
        return b


class TimeValue:
    def __init__(self, inner: float):
        self.inner = inner

    def string(self, timescale: Timescale):
        t = timescale.tt_jd(self.inner + 3 / 24)
        return "{}-{:02d}-{:02d} {:02d}:{:02d}".format(*t.ut1_calendar())

    def __eq__(self, other):
        if isinstance(other, TimeValue):
            return self.inner == other.inner
        return False
