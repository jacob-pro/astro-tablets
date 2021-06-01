import math
from abc import ABC
from dataclasses import dataclass
from enum import unique, Enum
from typing import *

import numpy as np

from generate.angular_separation import EclipticPosition
from query.angular_separation_query import AngularSeparationQuery
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
    UNKNOWN = 0  # A prediction or uncertain if it was a prediction
    PARTIAL_OR_TOTAL = 1  # An observation, of uncertain type
    PARTIAL = 2  # An observation of a partial eclipse
    TOTAL = 3  # An observations of a total eclipse


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
        results = list(map(lambda x: (x, self.score_eclipse(x, first_contact, type, phase_timing, position)),
                     matched_eclipses))
        results.sort(key=lambda x: x[1], reverse=True)
        if len(results) > 0:
            self.best = results[0][0]
            self.score = results[0][1]
        else:
            self.best = None
            self.score = 0.0

    @staticmethod
    def score_eclipse(eclipse: Dict, first_contact: Union[None, FirstContactTime],
                      type: ExpectedEclipseType, phase_timing: Union[None, PhaseTiming],
                      location: Union[None, EclipsePosition]) -> float:
        scores = [LunarEclipseQuery.eclipse_core_score(eclipse, type)]
        weights = [0.5]
        if location is not None:
            assert eclipse['angle'] is not None
            scores.append(AngularSeparationQuery.separation_score(location.target_angle, location.tolerance,
                                                            location.target_position, eclipse['angle'],
                                                            eclipse['position']))
            weights.append(0.25)
        if first_contact is not None:
            scores.append(LunarEclipseQuery.eclipse_time_of_day_score(eclipse, first_contact))
            weights.append(0.25)
        if phase_timing is not None:
            scores.append(LunarEclipseQuery.eclipse_phase_length_score(eclipse, phase_timing))
            weights.append(0.25)
        score = np.average(scores, weights=weights)
        assert 0 <= score <= 1
        return score

    @staticmethod
    def eclipse_core_score(eclipse: Dict, type: ExpectedEclipseType) -> float:
        score = 0
        if type == ExpectedEclipseType.UNKNOWN:
            score = 1.0
        elif type == ExpectedEclipseType.TOTAL and eclipse['visible']:
            if eclipse['e_type'] == 'Total':
                score = 1.0
            elif eclipse['e_type' == 'Partial']:
                score = 0.5
        elif type == ExpectedEclipseType.PARTIAL and eclipse['visible']:
            if eclipse['e_type'] == 'Total':
                score = 0.5
            elif eclipse['e_type'] == 'Partial':
                score = 1.0
        elif type == ExpectedEclipseType.PARTIAL_OR_TOTAL and eclipse['visible']:
            score = 1.0
        assert 0 <= score <= 1
        return score

    @staticmethod
    def eclipse_time_of_day_score(eclipse: Dict, first_contact: FirstContactTime) -> float:
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
        assert 0 <= score <= 1
        return score

    @staticmethod
    def eclipse_phase_length_score(eclipse: Dict, timings: PhaseTiming) -> float:
        if eclipse['sum_us'] == 0:
            return 0
        diffs = []
        if isinstance(timings, CompositePhaseTiming):
            diffs.append((timings.sum, eclipse['sum_us']))
        elif isinstance(timings, SeparatePhaseTimings):
            if timings.onset is not None:
                diffs.append((timings.onset, eclipse['onset_us']))
            if timings.maximal is not None:
                diffs.append((timings.maximal, eclipse['maximal_us']))
            if timings.clearing is not None:
                diffs.append((timings.clearing, eclipse['clearing_us']))
        else:
            raise RuntimeError
        score = 0
        for (observed, actual) in diffs:
            percent_err = abs(actual - observed) / abs(actual)
            score = score + math.pow(50, -percent_err)
        score = score / len(diffs)
        assert 0 <= score <= 1
        return score

    def output(self) -> dict:
        return {}

    def get_search_range(self) -> SearchRange:
        return self.target_time

    def quality_score(self) -> float:
        return self.score
