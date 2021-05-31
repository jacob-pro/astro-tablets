import math
from abc import ABC
from dataclasses import dataclass
from enum import unique, Enum
from typing import *

from generate.angular_separation import EclipticPosition
from query.database import Database
from query.abstract_query import AbstractQuery, SearchRange
from util import diff_time_degrees_signed


@unique
class FirstContactRelative(Enum):
    BEFORE_SUNRISE = 0
    AFTER_SUNRISE = 1
    BEFORE_SUNSET = 2
    AFTER_SUNSET = 3


@dataclass
class FirstContactTime:
    time_degrees: float
    relative: FirstContactRelative


@unique
class ExpectedEclipseType(Enum):
    UNKNOWN = 0           # A prediction or uncertain if it was a prediction
    PARTIAL_OR_TOTAL = 1  # An observation, of uncertain type
    PARTIAL = 2           # An observation of a partial eclipse
    TOTAL = 3             # An observations of a total eclipse


class PhaseTiming(ABC):
    pass


@dataclass
class SeparatePhaseTimings(PhaseTiming):
    onset: [None, float]
    maximal: [None, float]
    clearing: [None, float]


@dataclass
class CompositePhaseTiming(PhaseTiming):
    sum: [None, float]


# Position of the moon relative to a Normal Star
@dataclass
class EclipsePosition:
    body: str
    target_angle: float
    tolerance: float
    target_position: Union[EclipticPosition, None]


class LunarEclipseQuery(AbstractQuery):

    def __init__(self, db: Database, first_contact: Union[None, FirstContactTime],
                 type: ExpectedEclipseType, phase_timing: Union[None, PhaseTiming],
                 position: Union[None, EclipsePosition], target_time: SearchRange):
        self.target_time = target_time
        position_body = position.body if position is not None else None
        matched_eclipses = db.lunar_eclipses_in_range(target_time.start, target_time.end, position_body)
        scores = map(lambda x: (x, self.score_eclipse(x, first_contact, type, phase_timing, position)), matched_eclipses)
        pass

    @staticmethod
    def score_eclipse(eclipse: Dict, first_contact: Union[None, FirstContactTime],
                      type: ExpectedEclipseType, phase_timing: Union[None, PhaseTiming],
                      location: Union[None, EclipsePosition]) -> float:
        if location is not None:
            assert eclipse['angle'] is not None # Check that positions were computed
        pass

    @staticmethod
    def eclipse_timing_score(eclipse: Dict, first_contact: FirstContactTime) -> float:
        if eclipse['partial_eclipse_begin'] is None:
            return 0
        if first_contact.relative == FirstContactRelative.BEFORE_SUNRISE:
            actual = diff_time_degrees_signed(eclipse['sunrise'], eclipse['partial_eclipse_begin'])
        elif first_contact.relative == FirstContactRelative.AFTER_SUNRISE:
            actual = diff_time_degrees_signed(eclipse['partial_eclipse_begin'], eclipse['sunrise'])
        elif first_contact.relative == FirstContactRelative.BEFORE_SUNSET:
            actual = diff_time_degrees_signed(eclipse['sunset'], eclipse['partial_eclipse_begin'])
        elif first_contact.relative == FirstContactRelative.AFTER_SUNSET:
            actual = diff_time_degrees_signed(eclipse['partial_eclipse_begin'], eclipse['sunrise'])
        else:
            raise RuntimeError("Invalid FirstContactRelative")
        err = abs(first_contact.time_degrees - actual)
        percent_err = err / abs(actual)
        score = math.pow(50, -percent_err)
        return score

    def output(self) -> dict:
        pass

    def get_search_range(self) -> SearchRange:
        return self.target_time

    def quality_score(self) -> float:
        pass
