import os
import subprocess

from skyfield.timelib import Time


def diff_mins(t1: Time, t2: Time) -> float:
    jdiff = abs(t1 - t2)
    mins_in_day = 60 * 24
    return jdiff * mins_in_day


def diff_hours(t1: Time, t2: Time) -> float:
    jdiff = abs(t1 - t2)
    return jdiff * 24


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
    except subprocess.CalledProcessError as e:
        return True
