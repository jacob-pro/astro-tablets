from enum import Enum, unique
from typing import Any, Dict, List

from astro_tablets.constants import INFLECT_ENGINE, Confidence
from astro_tablets.data import MOON
from astro_tablets.generate.risings_settings import RiseSetType
from astro_tablets.query.abstract_query import AbstractQuery, SearchRange
from astro_tablets.query.database import BabylonianDay, Database
from astro_tablets.query.scorer import Scorer
from astro_tablets.util import TimeValue


@unique
class LunarSix(Enum):
    NA1 = "sunset to moonset"
    SU2 = "moonset to sunrise"
    NA = "sunrise to moonset"
    ME = "moonrise to sunset"
    GI6 = "sunset to moonrise"
    KUR = "moonrise to sunrise"

    def contains_sunset(self) -> bool:
        return self == LunarSix.NA1 or self == LunarSix.ME or self == LunarSix.GI6

    def lunar_set(self) -> bool:
        return self == LunarSix.NA1 or self == LunarSix.SU2 or self == LunarSix.NA

    def sun_first(self) -> bool:
        return self == LunarSix.NA1 or self == LunarSix.NA or self == LunarSix.GI6


class LunarSixQuery(AbstractQuery):
    def __init__(
        self,
        db: Database,
        month: List[BabylonianDay],
        day_number: int,
        six: LunarSix,
        value_us: float,
        time_confidence: Confidence = Confidence.REGULAR,
    ):
        assert value_us >= 0
        assert 1 <= day_number <= 30
        self.six = six

        sun_time = (
            month[day_number - 1].sunset
            if six.contains_sunset()
            else month[day_number - 1].sunrise
        )
        day_str = INFLECT_ENGINE.ordinal(day_number)
        comment = (
            "Sunset of the {}".format(day_str)
            if six.contains_sunset()
            else "Sunrise of the {}".format(day_str)
        )
        self.search_range = SearchRange(sun_time, sun_time, comment)

        moon_query = RiseSetType.SET if six.lunar_set() else RiseSetType.RISE

        moon_time = db.nearest_rising_setting(MOON, moon_query, sun_time)
        actual = moon_time - sun_time if six.sun_first() else sun_time - moon_time
        self.actual_us = actual * 360
        self.moon_time = moon_time

        self.score = self.calculate_score(self.actual_us, value_us, time_confidence)

    @staticmethod
    def calculate_score(
        actual_us: float, tablet_us: float, confidence: Confidence
    ) -> float:
        """
        Calculates score based on the actual time between the two events, compared to the expected time according
        to the tablet.
        The expected position (if specified) and actual position are also compared, giving an additional 0.2 to the
        score if they match.
        @param actual_us: The actual time difference in UŠ (can be negative if the events happen in the wrong order).
        @param tablet_us: The expected time difference in UŠ (should always be positive).
        @param confidence: How confident we are in reading the tablet's text.
        @return: A score value (between 0 and 1).
        """
        score = Scorer.score_time(actual_us, tablet_us, confidence)
        if actual_us < 0:
            # Reduce score when they are in the wrong order, proportional to how close the expected is to 0
            score *= 1 / tablet_us
        assert 0 <= score <= 1
        return score

    def quality_score(self) -> float:
        return self.score

    def output(self) -> dict:
        out: Dict[str, Any] = {"time_us": self.actual_us, "six": self.six.value}
        if self.six.lunar_set():
            out["moonset"] = TimeValue(self.moon_time)
        else:
            out["moonrise"] = TimeValue(self.moon_time)
        return out

    def get_search_range(self) -> SearchRange:
        return self.search_range
