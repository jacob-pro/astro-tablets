import os
import subprocess
from collections import OrderedDict
from typing import *

from skyfield.timelib import Time, Timescale


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


def get_git_hash() -> str:
    hash = os.getenv('GIT_HASH')
    if hash is not None and len(hash) > 0:
        return hash
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode("utf-8").partition('\n')[0]
    except subprocess.CalledProcessError as e:
        return "unknown"


def get_git_changes() -> bool:
    modified = os.getenv('GIT_MODIFIED')
    if modified is not None:
        return modified == "1"
    try:
        subprocess.check_output(['git', 'diff', '--exit-code'], stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return True
    return False


def array_group_by(input: List, key_fn: Callable) -> OrderedDict:
    res: OrderedDict = OrderedDict()
    for item in input:
        key = key_fn(item)
        if key in res:
            res[key].append(item)
        else:
            res[key] = [item]
    return res





class TimeValue:

    def __init__(self, inner):
        self.inner = inner

    def string(self, timescale: Timescale):
        if self.inner is None:
            return ""
        t = timescale.tt_jd(self.inner + 3 / 24)
        return "{}-{:02d}-{:02d} {:02d}:{:02d}".format(*t.ut1_calendar())

    def __eq__(self, other):
        if isinstance(other, TimeValue):
            return self.inner == other.inner
        return False
