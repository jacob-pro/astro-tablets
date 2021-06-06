import math
from enum import unique, Enum

from constants import *
from data import MOON
from generate.risings_settings import RiseSetType
from query.abstract_query import AbstractQuery, SearchRange
from query.database import Database, BabylonianDay
from util import TimeValue


@unique
class LunarSix(Enum):
    NA1 = "sunset to moonset"
    SU2 = "moonset to sunrise"
    NA = "sunrise to moonset"
    ME = "moonrise to sunset"
    GI6 = "sunset to moonrise"
    KUR = "moonrise to sunrise"

    def contains_sunset(self):
        return self == LunarSix.NA1 or self == LunarSix.ME or self == LunarSix.GI6

    def lunar_set(self):
        return self == LunarSix.NA1 or self == LunarSix.SU2 or self == LunarSix.NA

    def sun_first(self):
        return self == LunarSix.NA1 or self == LunarSix.NA or self == LunarSix.GI6


class LunarSixQuery(AbstractQuery):


    def __init__(self, db: Database, month: List[BabylonianDay], day_number: int, six: LunarSix, predicted: bool,
                 value_us: float):
        assert value_us >= 0
        assert 1 <= day_number <= 30


        sun_time = month[day_number - 1].sunset if six.contains_sunset() else month[day_number - 1].sunrise
        day_str = INFLECT_ENGINE.ordinal(day_number)
        comment = "Sunset of the {}".format(day_str) if six.contains_sunset() else "Sunrise of the {}".format(day_str)
        self.search_range = SearchRange(sun_time, sun_time, comment)

        self.moon_query = RiseSetType.SET if six.lunar_set() else RiseSetType.RISE

        moon_time = db.nearest_rising_setting(MOON, self.moon_query, sun_time)
        actual = moon_time - sun_time if six.sun_first() else sun_time - moon_time
        self.actual_us = actual * 360
        self.moon_time = moon_time

        tolerance = HIGH_TIME_TOLERANCE if predicted else REGULAR_TIME_TOLERANCE
        self.score = self.lunar_six_score(self.actual_us, value_us, tolerance)


    @staticmethod
    def lunar_six_score(actual_us: float, tablet_us: float, tolerance: float) -> float:
        if actual_us < 0:
            score = 0
        else:
            err = abs(tablet_us - actual_us)
            percent_err = err / abs(actual_us)
            score = math.pow(tolerance, -percent_err)
        assert 0 <= score <= 1
        return score

    def output(self) -> dict:
        return {
            'moon_time': TimeValue(self.moon_time),
            'moon_query': self.moon_query.value,
            'time_us': self.actual_us,
        }

    def get_search_range(self) -> SearchRange:
        return self.search_range

    def quality_score(self) -> float:
        return self.score
