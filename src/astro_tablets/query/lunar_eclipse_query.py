import math
from abc import ABC
from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from astro_tablets.constants import Body, TimePrecision
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.query.abstract_query import AbstractQuery, SearchRange
from astro_tablets.query.angular_separation_query import AngularSeparationQuery
from astro_tablets.query.database import Database, LunarEclipse
from astro_tablets.util import TimeValue, diff_time_degrees_signed


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
    onset: Optional[float]
    maximal: Optional[float]
    clearing: Optional[float]


@dataclass
class CompositePhaseTiming(PhaseTiming):
    sum: Optional[float]


# Position of the moon relative to a Normal Star
@dataclass
class EclipsePosition:
    body: Body
    target_angle: float
    tolerance: float
    target_position: Optional[EclipticPosition]


class LunarEclipseQuery(AbstractQuery):
    ECLIPSE_SEARCH_TOLERANCE = 6 / 24

    best: Optional[LunarEclipse]
    score: float

    def __init__(
        self,
        db: Database,
        first_contact: Optional[FirstContactTime],
        type: ExpectedEclipseType,
        phase_timing: Optional[PhaseTiming],
        position: Optional[EclipsePosition],
        target_time: SearchRange,
    ):
        self.target_time = target_time
        self.position = position
        self.phase_timing = phase_timing

        # Extend the search a little bit on either end, because closest_approach_time is only the midpoint
        start_wider = target_time.start - self.ECLIPSE_SEARCH_TOLERANCE
        end_wider = target_time.end + self.ECLIPSE_SEARCH_TOLERANCE

        matched_eclipses = db.lunar_eclipses_in_range(
            start_wider, end_wider, position.body if position is not None else None
        )
        results = list(
            map(
                lambda x: (
                    x,
                    self.score_eclipse(x, first_contact, type, phase_timing, position),
                ),
                matched_eclipses,
            )
        )
        results.sort(key=lambda x: x[1], reverse=True)
        if len(results) > 0:
            self.best = results[0][0]
            self.score = results[0][1]
        else:
            self.best = None
            self.score = 0.0

    @staticmethod
    def score_eclipse(
        eclipse: LunarEclipse,
        first_contact: Optional[FirstContactTime],
        type: ExpectedEclipseType,
        phase_timing: Optional[PhaseTiming],
        location: Optional[EclipsePosition],
    ) -> float:
        scores = [LunarEclipseQuery.eclipse_core_score(eclipse, type)]
        weights = [0.5]
        if location is not None:
            assert eclipse.angle is not None
            assert eclipse.position is not None
            scores.append(
                AngularSeparationQuery.separation_score(
                    location.target_angle,
                    location.tolerance,
                    location.target_position,
                    eclipse.angle,
                    eclipse.position,
                )
            )
            weights.append(0.25)
        if first_contact is not None:
            if type == ExpectedEclipseType.UNKNOWN:
                # If the eclipse is a prediction then assume low time precision
                scores.append(
                    LunarEclipseQuery.eclipse_time_of_day_score(
                        eclipse, first_contact, TimePrecision.LOW.value
                    )
                )
            else:
                scores.append(
                    LunarEclipseQuery.eclipse_time_of_day_score(
                        eclipse, first_contact, TimePrecision.REGULAR.value
                    )
                )
            weights.append(0.25)
        if phase_timing is not None:
            scores.append(
                LunarEclipseQuery.eclipse_phase_length_score(eclipse, phase_timing)
            )
            weights.append(0.25)
        score = np.average(scores, weights=weights)
        assert 0 <= score <= 1
        return float(score)

    @staticmethod
    def eclipse_core_score(eclipse: LunarEclipse, type: ExpectedEclipseType) -> float:
        score = 0.0
        if type == ExpectedEclipseType.UNKNOWN:
            score = 1.0
            if (
                eclipse.e_type == "Penumbral"
            ):  # Tie breaker, when two predicted eclipses, favour non penumbral
                score -= 0.001
        elif type == ExpectedEclipseType.TOTAL and eclipse.visible:
            if eclipse.e_type == "Total":
                score = 1.0
            elif eclipse.e_type == "Partial":
                score = 0.5
        elif type == ExpectedEclipseType.PARTIAL and eclipse.visible:
            if eclipse.e_type == "Total":
                score = 0.5
            elif eclipse.e_type == "Partial":
                score = 1.0
        elif type == ExpectedEclipseType.PARTIAL_OR_TOTAL and eclipse.visible:
            score = 1.0
        assert 0 <= score <= 1
        return score

    @staticmethod
    def eclipse_time_of_day_score(
        eclipse: LunarEclipse, first_contact: FirstContactTime, tolerance: float
    ) -> float:
        assert tolerance > 1
        if eclipse.partial_eclipse_begin is None:
            return 0
        if first_contact.relative == FirstContactRelative.BEFORE_SUNRISE:
            actual = diff_time_degrees_signed(
                eclipse.sunrise, eclipse.partial_eclipse_begin
            )
        elif first_contact.relative == FirstContactRelative.AFTER_SUNRISE:
            actual = diff_time_degrees_signed(
                eclipse.partial_eclipse_begin, eclipse.sunrise
            )
        elif first_contact.relative == FirstContactRelative.BEFORE_SUNSET:
            actual = diff_time_degrees_signed(
                eclipse.sunset, eclipse.partial_eclipse_begin
            )
        elif first_contact.relative == FirstContactRelative.AFTER_SUNSET:
            actual = diff_time_degrees_signed(
                eclipse.partial_eclipse_begin, eclipse.sunset
            )
        else:
            raise RuntimeError("Invalid FirstContactRelative")
        err = abs(first_contact.time_degrees - actual)
        percent_err = err / abs(actual)
        score = math.pow(tolerance, -percent_err)
        assert 0 <= score <= 1
        return score

    @staticmethod
    def eclipse_phase_length_score(
        eclipse: LunarEclipse, timings: PhaseTiming
    ) -> float:
        if eclipse.sum_us == 0:
            return 0
        diffs: List[Tuple[float, float]] = []
        if isinstance(timings, CompositePhaseTiming):
            assert timings.sum is not None
            diffs.append((timings.sum, eclipse.sum_us))
        elif isinstance(timings, SeparatePhaseTimings):
            if timings.onset is not None:
                diffs.append((timings.onset, eclipse.onset_us))
            if timings.maximal is not None:
                diffs.append((timings.maximal, eclipse.maximal_us))
            if timings.clearing is not None:
                diffs.append((timings.clearing, eclipse.clearing_us))
        else:
            raise RuntimeError
        score = 0.0
        for (observed, actual) in diffs:
            if actual != 0:
                percent_err = abs(actual - observed) / abs(actual)
                score = score + math.pow(TimePrecision.REGULAR.value, -percent_err)
        score = score / len(diffs)
        assert 0 <= score <= 1
        return score

    def output(self) -> dict:
        out: Dict[str, Any] = {}
        if self.best is not None:
            out["closest_approach_time"] = TimeValue(self.best.closest_approach_time)
            out["visible"] = self.best.visible
            out["type"] = self.best.e_type
            out["onset_us"] = self.best.onset_us
            out["maximal_us"] = self.best.maximal_us
            out["clearing_us"] = self.best.clearing_us
            out["sum_us"] = self.best.sum_us
            if self.best.e_type != "Penumbral":
                assert self.best.partial_eclipse_begin is not None
                out["after_sunrise_us"] = diff_time_degrees_signed(
                    self.best.partial_eclipse_begin, self.best.sunrise
                )
                out["after_sunset_us"] = diff_time_degrees_signed(
                    self.best.partial_eclipse_begin, self.best.sunset
                )
            if self.position is not None:
                out["position_body"] = self.position.body.name
                out["position_actual_angle"] = self.best.angle
                out["position_actual_position"] = self.best.position
        return out

    def get_search_range(self) -> SearchRange:
        return self.target_time

    def quality_score(self) -> float:
        return self.score
